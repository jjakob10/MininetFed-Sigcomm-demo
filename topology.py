import os
import sys
import threading
from pathlib import Path
from time import sleep

from mininet.log import info, setLogLevel
from mininet.term import makeTerm

from mn_wifi.sixLoWPAN.link import LoWPAN
from mn_wifi.energy import BitZigBeeEnergy

from containernet.node import DockerP4Sensor
from containernet.cli import CLI
from containernet.energy import Energy

from federated.net import MininetFed
from federated.node import ClientSensor, ServerSensor

from battery import iniciar_plot


volume = "/flw"
volumes = [f"{Path.cwd()}:" + volume, "/tmp/.X11-unix:/tmp/.X11-unix:rw"]

experiment_config = {
    "ipBase": "10.0.0.0/24",
    # "iot_module":"mac802154_hwsim",
    "experiments_folder": "sigcomm",
    # "experiment_name": "ipv4_test",
    "date_prefix": False
}

server_args = {}
client_args = {}
experiment_name = ""


def topology():
    # Configurações iniciais
    t = 5
    if '-10' in sys.argv:
        t = 10

    # Executa o caso de uso All
    if '--case_all' in sys.argv or '-a' in sys.argv:
        server_args = {"min_trainers": 11, "num_rounds": 20,
                       "stop_acc": 0.999, 'client_selector': 'All', 'aggregator': "FedAvg"}
        client_args = {"mode": 'random same_samples',
                       'num_samples': 15000, "trainer_class": "TrainerMNIST"}
        experiment_name = 'sbrc_mnist_select_all_iid'
        plot_title = 'Battery Consumption Selection of all clients'
    # Executa o caso de uso Random
    elif '--case_random' in sys.argv or '-r' in sys.argv:
        server_args = {"min_trainers": 8, "num_rounds": 20,
                       "stop_acc": 0.99, 'client_selector': 'Random', 'aggregator': "FedAvg"}
        client_args = {"mode": 'random same_samples',
                       'num_samples': 15000, "trainer_class": "TrainerMNIST"}
        experiment_name = 'sbrc_mnist_select_random_5_iid'
        plot_title = 'Battery Consumption Random Client Selection'
    # Executa o caso de uso Energy
    elif '--case_energy' in sys.argv or '-e' in sys.argv:
        server_args = {"min_trainers": 8, "num_rounds": 20,
                       "stop_acc": 0.99, 'client_selector': 'LeastEnergyConsumption', 'aggregator': "FedAvg"}
        client_args = {"mode": 'random same_samples',
                       'num_samples': 15000, "trainer_class": "TrainerMNIST"}
        experiment_name = 'sbrc_mnist_select_energy_iid'
        plot_title = 'Battery Consumption Energy Consumption Client Selection'
    else:
        raise Exception(
            "É preciso selecionar um caso para executar (--case_all, --case_random, ou --case_energy)\n")

    # Instanciação da rede
    net = MininetFed(**experiment_config, controller=[], experiment_name=experiment_name,
                     default_volumes=volumes, topology_file=sys.argv[0])

    path = os.path.dirname(os.path.abspath(__file__))

    json_file = '/root/json/lowpan-storing.json'
    config = path + '/rules/p4_commands.txt'
    args = {'json': json_file, 'switch_config': config}
    mode = 2

    dimage = 'ramonfontes/bmv2:lowpan'

    info('*** Adding Nodes...\n')
    s1 = net.addSwitch("s1", failMode='standalone# Executa o caso de uso All')
    ap1 = net.addAPSensor('ap1', cls=DockerP4Sensor, ip6='fe80::1/64', panid='0xbeef',
                          voltage=3.7,
                          battery_capacity=10,
                          dodag_root=True, storing_mode=mode, privileged=True,
                          volumes=[path + "/:/root",
                                   "/tmp/.X11-unix:/tmp/.X11-unix:rw"],
                          dimage=dimage, cpu_shares=20, netcfg=True, trickle_t=t,
                          environment={"DISPLAY": ":1"}, loglevel="info",
                          thriftport=50001,  IPBASE="172.17.0.0/24", **args)

    srv1 = net.addFlHost('srv1', cls=ServerSensor, script="server/server.py",
                         voltage=3.7,
                         battery_capacity=10,
                         args=server_args, volumes=volumes,
                         dimage='mininetfed:serversensor',
                         ip6='fe80::2/64', panid='0xbeef', trickle_t=t,
                         environment={"DISPLAY": ":0"}, privileged=True
                         )

    clients = []
    for i in range(11):
        clients.append(net.addSensor(f'sta{i}', privileged=True, environment={"DISPLAY": ":0"},
                                     cls=ClientSensor, script="client/client.py",
                                     voltage=3.7,
                                     battery_capacity=15,
                                     ip6=f'fe80::{i+3}/64',
                                     numeric_id=i-1,
                                     args=client_args, volumes=volumes,
                                     dimage='mininetfed:clientsensor'
                                     ))
    net.addAutoStop6()

    h1 = net.addDocker('h1', volumes=[path + "/:/root", "/tmp/.X11-unix:/tmp/.X11-unix:rw"],
                       dimage="ramonfontes/grafana", port_bindings={3000: 3000}, ip='192.168.210.1',
                       privileged=True, environment={"DISPLAY": ":1"})

    net.configureWifiNodes()

    info('*** Creating links...\n')
    net.addLink(s1, h1)
    net.addLink(ap1, srv1, cls=LoWPAN)
    

    net.addLink(ap1, clients[5], cls=LoWPAN) 
    net.addLink(clients[0], clients[1], cls=LoWPAN)
    net.addLink(clients[1], clients[2], cls=LoWPAN)
    net.addLink(clients[2], clients[4], cls=LoWPAN)
    net.addLink(clients[4], clients[3], cls=LoWPAN)
    net.addLink(clients[4], clients[5], cls=LoWPAN)
    net.addLink(clients[5], clients[6], cls=LoWPAN)
    net.addLink(clients[6], clients[7], cls=LoWPAN)
    net.addLink(clients[6], clients[8], cls=LoWPAN)
    net.addLink(clients[8], clients[9], cls=LoWPAN)
    net.addLink(clients[8], clients[10], cls=LoWPAN)
    net.addLink(ap1, h1)
    net.addLinkAutoStop(ap1)

    h1.cmd('ifconfig h1-eth1 192.168.0.1')

    if '-p' in sys.argv:
        net.plotEnergyMonitor(
            nodes=[clients[0], clients[4]], title=plot_title)
        info('*** Plotting Battery Consumption...\n')

    info('*** Starting network...\n')
    net.build()
    net.addNAT(name='nat0', linkTo='s1', ip='192.168.210.254').configDefault()
    ap1.start([])
    s1.start([])
    net.staticArp()

    info("*** Measuring energy consumption\n")
    Energy(net.sensors)
    BitZigBeeEnergy(net.sensors)

    info('*** Running devices...\n')
    net.configRPLD(net.sensors + net.apsensors)

    info('*** Running broker...\n')
    ap1.cmd("nohup mosquitto -c /etc/mosquitto/mosquitto.conf &")
    makeTerm(
        ap1, cmd="bash -c 'tail -f /var/log/mosquitto/mosquitto.log'")

    net.broker_addr = 'fd3c:be8a:173f:8e80::1'

    sleep(1)
    info('*** Server...\n')
    srv1.run(broker_addr=net.broker_addr,
             experiment_controller=net.experiment_controller)

    sleep(3)

    info('*** Clients...\n')
    for client in clients:
        client.run(broker_addr=net.broker_addr,
                   experiment_controller=net.experiment_controller)

    h1.cmd("ifconfig h1-eth1 down")
    
    # Inicia o gráfico numa thread
    if '-p' not in sys.argv:
        info('*** Starting plot...\n')
        thread_plot = threading.Thread(target=iniciar_plot, args=(clients,plot_title,), daemon=True)
        thread_plot.start()


    info('*** Running Autostop...\n')
    net.wait_experiment()
    os.system('pkill -9 -f xterm')

    info('*** Stopping network...\n')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
