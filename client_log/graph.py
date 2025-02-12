import subprocess
import re
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import ScalarFormatter
import glob


def docker_cp(container_name, source_path, destination_path):
    """
    Copia arquivos entre o host e um container Docker usando 'docker cp'.
    Args:
        container_name (str): Nome ou ID do container.
        source_path (str): Caminho do arquivo ou diretório de origem.
        destination_path (str): Caminho de destino (no host ou no container).
    Returns:
        None
    Raises:
        subprocess.CalledProcessError: Se o comando docker cp falhar.
    """
    try:
        # Monta o comando docker cp
        command = ["docker", "cp", f"{source_path}", f"{destination_path}"]

        # Executa o comando
        subprocess.run(command, check=True)
        print(
            f"Arquivo(s) copiado(s) com sucesso: {source_path} -> {destination_path}")

    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando docker cp: {e}")
        # raise


for n in range(0, 8):
    container = f"mn.sta{n}"
    source = f"{container}:/tmp/consumption.log"
    destination = f"./{container[3:]}.log"
    docker_cp(container, source, destination)


def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else float('inf')

# Função para ler dados de um arquivo e extrair as informações


def read_data_from_file(file_path):
    timestamps = []
    values1 = []  # Para armazenar os valores de uso da CPU
    values2 = []  # Para armazenar os valores de consumo de energia

    with open(file_path, 'r') as file:
        for line in file:
            # Split de cada linha
            parts = line.split(',')

            if len(parts) == 3:
                timestamp = parts[0].strip()
                value1 = float(parts[1].strip())
                value2 = float(parts[2].strip())

                # Adicionando os valores diretamente
                timestamps.append(datetime.strptime(
                    timestamp, '%Y-%m-%d %H:%M:%S'))
                values1.append(value1)  # Uso da CPU
                values2.append(value2)  # Consumo de energia

    return timestamps, values1, values2


# Caminho para os arquivos (exemplo: arquivos .log na pasta atual)
file_paths = sorted(glob.glob('*.log'), key=extract_number)

# Configurando layout com GridSpec (linhas dinâmicas e 2 colunas)
num_files = len(file_paths)
num_rows = (num_files + 1) // 2  # Determina o número de linhas necessárias
fig = plt.figure(figsize=(14, 6 * num_rows))
gs = GridSpec(num_rows, 2, figure=fig)

# Iterando sobre os arquivos e criando subplots
for i, file_path in enumerate(file_paths):
    timestamps, values1, values2 = read_data_from_file(file_path)

    # Gerando o label para cada arquivo
    label_name = file_path.split('/')[-1]

    # Subplot na posição adequada
    row, col = divmod(i, 2)  # Calcula a posição na grade
    ax = fig.add_subplot(gs[row, col])

    # Plotando o uso da CPU e consumo de energia
    # ax.plot(timestamps, values1, linestyle='-',
    #         label='Uso da CPU', color='tab:blue')
    ax2 = ax
    ax2.plot(timestamps, values2,
             label='Consumo de Energia', color='tab:blue')

    # Configurando os eixos
    ax.set_title(f'{label_name[:-4]}', fontsize=14)
    ax.set_xlabel('Tempo', fontsize=12)
    # ax.set_ylabel('Uso de CPU (%)', color='tab:blue', fontsize=8)
    # ax.tick_params(axis='y', labelcolor='tab:blue')
    # ax.set_ylim(top=350, bottom=0)

    ax2.set_ylabel('Consumo de \nEnergia (Wh)', fontsize=12)
    ax2.tick_params(axis='y', labelsize=12)
    ax2.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax2.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    ax2.set_ylim(top=0.025, bottom=0)

    # Formatando o eixo X para mostrar horas:minutos:segundos
    ax.set_xticks(timestamps[::len(timestamps) // 6])  # Máximo de 6 rótulos
    ax.set_xticklabels([ts.strftime('%H:%M:%S')
                       for ts in timestamps[::len(timestamps) // 6]])
    ax.set_xticklabels([])

    # Adicionando legendas
    # ax.legend(loc='upper left')
    # ax2.legend(loc='upper right')

fig.subplots_adjust(hspace=0.5, wspace=0.2, right=0.95,
                    left=0.06, top=0.95, bottom=0.03)
# plt.suptitle("Consumo de Energia no Tempo", fontsize=14)
# plt.savefig("all.eps",
#             bbox_inches='tight')
plt.show()
