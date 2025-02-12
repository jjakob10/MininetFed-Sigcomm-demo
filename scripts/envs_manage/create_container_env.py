try:
    from containernet.net import Containernet
    from containernet.term import makeTerm
    from containernet.cli import CLI
except:
    from mininet.net import Containernet
    from mininet.term import makeTerm
    from mininet.cli import CLI
from mininet.node import Controller
from mininet.log import info, setLogLevel
from pathlib import Path
import sys
import os
import subprocess

ENVS_FOLDER = "envs"


def create_container_env(image: str, requirements_path: str, output_path: str) -> None:

    setLogLevel('info')
    net = Containernet(controller=Controller)
    info('*** Adding controller\n')
    net.addController('c0')

    volumes = [f"{Path.cwd()}:/flw"]

    s1 = net.addSwitch('s1')

    info('*** Adicionando Containers\n')
    srv1 = net.addDocker('srv1', dimage=image,
                         volumes=volumes, mem_limit="4096m")
    net.addLink(srv1, s1)

    net.start()
    info('*** Criando env')
    srv1.cmd(
        f"bash -c 'cd flw && python3 -m venv {output_path}' ;", verbose=True)

    info('*** Iniciando instalação')

    srv1.cmd(
        f"bash -c 'cd flw && . {output_path}/bin/activate && pip install -r {requirements_path}' ;", verbose=True)
    info('*** Parando MININET')
    net.stop()


def call_local_script(file, output):
    script_path = os.path.join(
        os.path.dirname(__file__), "create_local_env.sh")
    try:
        subprocess.run([script_path, file, output], check=True)
    except subprocess.CalledProcessError as e:
        print(
            f"Error: Failed to execute script {script_path} with {file} and {output}")
        print(e)


if __name__ == '__main__':
    n = len(sys.argv)
    if n < 4:
        print("correct use: sudo python3 create_container_env.py -c/-l <path/requirements> ... <image>")
        exit()

    mode = sys.argv[1]

    image = ''
    if sys.argv[-1] == '-std':
        image = "mininetfed:container"
    else:
        image = sys.argv[-1]

    if mode not in ['-c', '-l']:
        print("Invalid mode. Use -c for container or -l for local.")
        exit()

    files_to_process = []

    for path in sys.argv[2:-1]:
        if os.path.isdir(path):
            files_to_process.extend([os.path.join(path, f)
                                    for f in os.listdir(path) if f.endswith('.txt')])
        elif os.path.isfile(path):
            files_to_process.append(path)
        else:
            print(
                f"Warning: {path} is neither a file nor a directory. Ignoring it.")

    if not files_to_process:
        print("No valid .txt files found.")
        exit()

    for file in files_to_process:
        file_name = os.path.basename(file).replace('.requirements.txt', '')
        output = os.path.join(ENVS_FOLDER, file_name)

        if mode == '-c':
            create_container_env(image, file, output)
        elif mode == '-l':
            call_local_script(file, output)
