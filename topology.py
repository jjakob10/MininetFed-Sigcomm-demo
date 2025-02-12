import os
import sys
from pathlib import Path
from time import sleep

from containernet.node import DockerP4Sensor, DockerSensor
from containernet.cli import CLI
from mininet.log import info, setLogLevel
from mn_wifi.sixLoWPAN.link import LoWPAN
from mininet.term import makeTerm
from containernet.energy import Energy
from mn_wifi.energy import BitZigBeeEnergy
# from mn_wifi.bitEnergy import BitEnergy

from federated.net import MininetFed
from federated.node import ClientSensor, ServerSensor


volume = "/flw"
volumes = [f"{Path.cwd()}:" + volume, "/tmp/.X11-unix:/tmp/.X11-unix:rw"]

server_args = {}
client_args = {}  

def topology():
    net = MininetFed(ipBase='10.0.0.0/24', iot_module='mac802154_hwsim', controller=[], experiment_name="sbrc_mnist_select_all_iid",
                     experiments_folder="sbrc", date_prefix=False, default_volumes=volumes, topology_file=sys.argv[0])

    t = 5
    if '-10' in sys.argv:
        t = 10
        
    
    if '-case_all' in sys.argv:
        server_args = {"min_trainers": 8, "num_rounds": 20,
               "stop_acc": 0.999, 'client_selector': 'All'}
        client_args = {"mode": 'random same_samples',
               'num_samples': 15000} 
    elif '-case_random' in sys.argv:
        
        server_args = {"min_trainers": 8, "num_rounds": 20,
               "stop_acc": 0.99, 'client_selector': 'Random'}
        client_args = {"mode": 'random same_samples',
                    'num_samples': 15000} 
        
    elif '-case_energy' in sys.argv:
        server_args = {"min_trainers": 8, "num_rounds": 20,
               "stop_acc": 0.99, 'client_selector': 'LeastEnergyConsumption'}
        client_args = {"mode": 'random same_samples',
               'num_samples': 15000}
    else:
        raise Exception("É preciso selecionar um caso para executar (-case_all, -case_random, ou -case_energy)\n")

    path = os.path.dirname(os.path.abspath(__file__))

    json_file = '/root/json/lowpan-storing.json'
    config = path + '/rules/p4_commands.txt'
    args = {'json': json_file, 'switch_config': config}
    mode = 2

    dimage = 'ramonfontes/bmv2:lowpan'

    info('*** Adding Nodes...\n')
    s1 = net.addSwitch("s1", failMode='standalone')
    ap1 = net.addAPSensor('ap1', cls=DockerP4Sensor, ip6='fe80::1/64', panid='0xbeef',
                          dodag_root=True, storing_mode=mode, privileged=True,
                          volumes=[path + "/:/root",
                                   "/tmp/.X11-unix:/tmp/.X11-unix:rw"],
                          dimage=dimage, cpu_shares=20, netcfg=True, trickle_t=t,
                          environment={"DISPLAY": ":1"}, loglevel="info",
                          thriftport=50001,  IPBASE="172.17.0.0/24", **args)  

    srv1 = net.addFlHost('srv1', cls=ServerSensor, script="server/server.py",  
                         args=server_args, volumes=volumes, 
                       
                         dimage='mininetfed:serversensor',
                         ip6='fe80::2/64', panid='0xbeef', trickle_t=t,
                         environment={"DISPLAY": ":0"}, privileged=True
                         )

    clients = []
    for i in range(8):
        clients.append(net.addSensor(f'sta{i}', privileged=True, environment={"DISPLAY": ":0"},
                                     cls=ClientSensor, script="client/client.py",

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

    net.addLink(ap1, clients[0], cls=LoWPAN)
    net.addLink(ap1, clients[4], cls=LoWPAN)
    net.addLink(clients[0], clients[1], cls=LoWPAN)
    net.addLink(clients[0], clients[2], cls=LoWPAN)
    net.addLink(clients[0], clients[3], cls=LoWPAN)
    net.addLink(clients[4], clients[5], cls=LoWPAN)
    net.addLink(clients[4], clients[6], cls=LoWPAN)
    net.addLink(clients[4], clients[7], cls=LoWPAN)
    net.addLink(ap1, h1)
    net.addLinkAutoStop(ap1)


    h1.cmd('ifconfig h1-eth1 192.168.0.1')

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

    sleep(2)
    broker_addr = 'fd3c:be8a:173f:8e80::1'

    info('*** Server...\n')
    srv1.run(broker_addr=broker_addr,
             experiment_controller=net.experiment_controller, args=server_args)

    sleep(5)

    info('*** Clients...\n')
    for client in clients:
        client.run(broker_addr=broker_addr,
                   experiment_controller=net.experiment_controller, args=client_args)
   

    h1.cmd("ifconfig h1-eth1 down")


    info('*** Running Autostop...\n')

    net.wait_experiment(broker_addr=broker_addr)

    os.system('pkill -9 -f xterm')

    info('*** Stopping network...\n')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
