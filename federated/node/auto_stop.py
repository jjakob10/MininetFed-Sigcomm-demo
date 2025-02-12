from containernet.node import Docker
try:
    from containernet.term import makeTerm
except:
    from mininet.term import makeTerm

from ..external_broker import ExtBroker

from .common import *


class AutoStop (Docker):
    """Node that represents a docker container of a auto stoper. 
    It stops the excecution of the local machine code waiting for a message from 
    the mqtt topics: 
        'minifed/stopQueue' or 'minifed/autoWaitContinue'
    """

    def __init__(self, name, env, dimage=DEFAULT_IMAGE,  volumes=[], **kwargs):
        self.env = env
        Docker.__init__(self, name, dimage=dimage, volumes=volumes, **kwargs)
        self.cmd("ifconfig eth0 down")

    def run(self, broker_addr):
        self.broker_addr = broker_addr
        # Docker.start(self)
        self.cmd("route add default gw %s" % broker_addr)

    def auto_stop(self, verbose=True):
        try:
            self.cmd(
                f'bash -c "cd {VOLUME_FOLDER} && . {ENVS_FOLDER}/{self.env}/bin/activate && python3 stop.py {self.broker_addr}"', verbose=verbose)

        except:
            print(color.BLUE+"\nKeyboard interrupt: manual continue"+color.RESET)
