from containernet.node import DockerSensor
try:
    from containernet.term import makeTerm
except:
    from mininet.term import makeTerm

import json


from .common import *


class AutoStop6 (DockerSensor):
    """Node that represents a docker container of a MininerFed client.
    """

    def __init__(self, name, dimage=DEFAULT_IMAGE_6, volumes=[], **kwargs):
        self.name = name

        DockerSensor.__init__(self, name, dimage=dimage,
                              volumes=volumes, **kwargs)

        self.cmd("ifconfig eth0 down")

    def auto_stop(self, broker_addr, verbose=True):
        self.cmd("route add -A inet6 default gw  %s" %
                 broker_addr)
        try:
            self.cmd(
                f'bash -c "cd {VOLUME_FOLDER} && python3 stop.py {broker_addr}"', verbose=verbose)

        except:
            print(color.BLUE+"\nKeyboard interrupt: manual continue"+color.RESET)
