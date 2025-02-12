from containernet.node import Docker
try:
    from containernet.term import makeTerm
except:
    from mininet.term import makeTerm

import json


from .common import *


class Client (Docker):
    """Node that represents a docker container of a MininerFed client.
    """

    def __init__(self, name, script,  env,  numeric_id,  args={}, dimage=None, cpu_quota=None, volumes=[], mem_limit=None, **kwargs):
        self.name = name
        # self.trainer_mode = trainer_mode
        self.numeric_id = numeric_id
        self.script = script
        self.args = args
        self.env = env

        if cpu_quota is not None:
            kwargs["cpu_period"] = CPU_PERIOD
            kwargs["cpu_quota"] = cpu_quota

        Docker.__init__(self, name, dimage=dimage,
                        volumes=volumes, mem_limit=mem_limit, **kwargs)

        self.cmd("ifconfig eth0 down")

    def run(self, broker_addr, experiment_controller, args={}):
        self.experiment = experiment_controller
        self.broker_addr = broker_addr
        # Docker.start(self) {self.trainer_mode}
        cmd = f"""bash -c "cd {VOLUME_FOLDER} && . {ENVS_FOLDER}/{self.env}/bin/activate && python3 {self.script} {self.broker_addr} {self.name} {self.numeric_id} 2> client_log/{self.name}.txt """

        if self.args != None and len(self.args) != 0:
            json_str = json.dumps(self.args).replace('"', '\\"')
            cmd += f"'{json_str}'"
        cmd += '" ;'
        self.cmd("route add default gw %s" %
                 self.broker_addr)

        makeTerm(self, cmd=cmd)
