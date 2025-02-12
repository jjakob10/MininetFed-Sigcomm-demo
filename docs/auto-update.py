import os
import ollama
import json
from datetime import datetime

# Path to the docs folder
docs_path = 'docs'

# Path to store timestamps of last translation
timestamps_file = f'{docs_path}/last_translations.json'

# Mapping of Portuguese to English file paths
file_mapping = {
    "Clientes.md": "Clients.md",
    "Configurações-da-execução.md": "Settings.md",
    "Informações-adicionais.md": "Futher-informations.md",
    "Primeiros-Passos.md": "First-Steps.md",
    "Script-de-análise.md": "Analysis-Script.md",
    "Scripts-de-apoio.md": "Additional-scripts.md",
    "Servidor.md": "Server.md",
    "../readme.md": "../readme(en).md"
}


def load_timestamps():
    """Load the timestamps of the last translations from the file."""
    if os.path.exists(timestamps_file):
        with open(timestamps_file, 'r') as f:
            return json.load(f)
    return {}


def save_timestamps(timestamps):
    """Save the updated timestamps to the file."""
    with open(timestamps_file, 'w') as f:
        json.dump(timestamps, f, indent=4)


def translate_text(text):
    """Translate the given text from Portuguese to English using Ollama with a large context window."""
    # Prompt for translation
    prompt = f"You are a senior technical documentation translator. Answer just with the translated text. Translate the following text from Portuguese to English:\n\n{text}"

    # Sending the prompt with a specified larger context window size (131072 tokens = 2^17)
    response = ollama.chat(
        model="llama3.1",
        messages=[{'role': 'user', 'content': prompt}],
        options={"num_ctx": 131072}  # Setting num_ctx to 2^17 (131072 tokens)
    )

    translation = response['message']['content']  # Extract the translated text

    return translation


def process_translation():
    """Process translation from Portuguese files to English files, only translating modified files."""
    # Load the timestamps of the last translation
    last_timestamps = load_timestamps()
    new_timestamps = {}

    pt_br_path = os.path.join(docs_path, 'pt-br')
    en_path = os.path.join(docs_path, 'en')

    for pt_file, en_file in file_mapping.items():
        pt_file_path = os.path.join(pt_br_path, pt_file)
        en_file_path = os.path.join(en_path, en_file)

        # Get the last modified time of the Portuguese file
        last_modified_time = os.path.getmtime(pt_file_path)
        new_timestamps[pt_file] = last_modified_time

        # Check if the file has been modified since the last translation
        if pt_file not in last_timestamps or last_modified_time > last_timestamps[pt_file]:
            # Read the Portuguese content
            with open(pt_file_path, 'r', encoding='utf-8') as file:
                pt_content = file.read()

            # Translate content
            translated_content = translate_text(pt_content)

            # Write translated content to the corresponding English file
            with open(en_file_path, 'w', encoding='utf-8') as file:
                file.write(translated_content)

            print(f"Translated {pt_file} and updated {en_file}")
        else:
            print(f"{pt_file} has not been modified, skipping translation.")

    # Save the new timestamps after processing
    save_timestamps(new_timestamps)


if __name__ == "__main__":
    process_translation()
