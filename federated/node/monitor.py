from containernet.node import Docker
try:
    from containernet.term import makeTerm
except:
    from mininet.term import makeTerm

from .common import *


class Monitor (Docker):
    """Node that represents a docker container of a custom network monitor.
    """

    def __init__(self, name, env, experiment_controller, script, dimage=DEFAULT_IMAGE, volumes=[], **kwargs):
        self.script = script
        self.experiment = experiment_controller
        self.env = env
        Docker.__init__(self, name, dimage=dimage,
                        volumes=volumes, **kwargs)
        self.cmd("ifconfig eth0 down")

    def run(self, broker_addr):
        self.broker_addr = broker_addr
        Docker.start(self)
        self.cmd("route add default gw %s" % self.broker_addr)
        command = f"bash -c 'cd {VOLUME_FOLDER} && . {ENVS_FOLDER}/{self.env}/bin/activate && python3 {self.script} {self.broker_addr} {self.experiment.getFileName(extension='''''')}.net'"
        makeTerm(self, cmd=command)
