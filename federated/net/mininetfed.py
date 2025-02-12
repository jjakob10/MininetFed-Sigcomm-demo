
from containernet.net import Containernet
from containernet.cli import CLI

from ..node import Broker, Monitor, AutoStop, AutoStop6
from ..experiment import Experiment

from mn_wifi.sixLoWPAN.link import LoWPAN


class MininetFed(Containernet):

    def __init__(self, experiment_name,
                 experiments_folder, default_volumes, default_connection='s1', date_prefix=False, broker_mode="internal", ext_broker_ip='127.0.0.1', topology_file=None, **kwargs):

        self.default_connection = default_connection
        self.ext_broker_ip = ext_broker_ip
        self.broker_mode = broker_mode

        self.nodes = {}
        self.priority_nodes = []
        self.default_volumes = default_volumes
        self.experiment_controller = Experiment(experiment_name=experiment_name,
                                                experiments_folder=experiments_folder, create_new=date_prefix)
        if topology_file is not None:
            self.experiment_controller.copyFileToExperimentFolder(
                topology_file)
        super().__init__(**kwargs)

    def addAutoStop6(self):
        self.auto_stop = self.addSensor('auto_stop', privileged=True, environment={"DISPLAY": ":0"},
                                        cls=AutoStop6,
                                        ip6=f'fe80::fffe/64', volumes=self.default_volumes,
                                        dimage='mininetfed:serversensor'

                                        )

    def addLinkAutoStop(self, device2):
        self.addLink(self.auto_stop, device2, cls=LoWPAN)

    def addFlHost(self, name, cls=None, start_priority=0, **params):
        """
        Adiciona um host à estrutura 'nodes' baseada em prioridade.
        Cada prioridade é representada por uma lista que contém os hosts associados.
        """

        # Certifica-se de que a prioridade existe no dicionário
        if start_priority not in self.nodes:
            self.nodes[start_priority] = []

        # Adiciona o host à lista correspondente à prioridade
        # host = super().addHost(name, cls, **params)
        host = super().addSensor(name, cls, **params)
        self.nodes[start_priority].append(host)
        return host

    def addAPSensor(self, name, cls=None, **params):
        self.apsensor = super().addAPSensor(name, cls, **params)
        return self.apsensor

    def configureMininetFed(self):
        self.brk = super().addHost('brk', cls=Broker, mode=self.broker_mode, ext_broker_ip=self.ext_broker_ip, volumes=self.default_volumes,
                                   dimage="mininetfed:broker")

        self.mnt = super().addHost('mnt', cls=Monitor, env='../env', script="network_monitor.py",
                                   experiment_controller=self.experiment_controller, volumes=self.default_volumes)

        self.auto_stop = super().addHost('stop', cls=AutoStop, env='../env',
                                         volumes=self.default_volumes)

        self.addLink(self.default_connection, self.brk)
        self.addLink(self.default_connection, self.mnt)
        self.addLink(self.default_connection, self.auto_stop)

    def runFlDevices(self):
        """
        Executa dispositivos agrupados por prioridade, na ordem crescente de prioridade.
        """
        # Executa o broker e inicializa outros componentes
        self.brk.run()

        # Obtem o endereço do broker
        self.broker_addr = self.brk.IP(intf="brk-eth0")

        # Executa serviços adicionais usando o endereço do broker
        self.auto_stop.run(broker_addr=self.broker_addr)
        self.mnt.run(broker_addr=self.broker_addr)

        # Ordena as prioridades e executa os dispositivos por prioridade
        for priority in sorted(self.nodes.keys()):
            for device in self.nodes[priority]:
                device.run()

    # def start(self):

    #     super().build()
    #     self.addNAT(name='nat0', linkTo='s1',
    #                 ip='10.168.210.254').configDefault()

    #     self.apsensor.start([])
    #     # self.apsensor.start([])

    #     # super().start() # o DockerP4Sensor fala que não tem 'command'
    #     self.brk.start()

    #     self.broker_addr = self.brk.IP(intf="brk-eth0")

    #     self.auto_stop.start(broker_addr=self.broker_addr)
    #     self.mnt.start(broker_addr=self.broker_addr)

    #     # for node in self.priority_nodes:
    #     #     node.start(broker_addr=self.broker_addr,
    #     #                experiment_controller=self.experiment_controller)

    #     # self.auto_stop.auto_stop()

    #     # for node in self.nodes:
    #     #     node.start(broker_addr=self.broker_addr,
    #     #                experiment_controller=self.experiment_controller)

    #     self.staticArp()
    #     self.configRPLD(self.sensors + self.apsensors)

    def wait_experiment(self, broker_addr=None, start_cli=False):
        if start_cli:
            CLI(self)
        else:
            self.auto_stop.auto_stop(broker_addr)
