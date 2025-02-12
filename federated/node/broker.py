import time

from containernet.node import Docker
try:
    from containernet.term import makeTerm
except:
    from mininet.term import makeTerm

from ..external_broker import ExtBroker

from .common import *


class Broker (Docker):
    """Node that represents a docker container of a Mosquitto Broker.
    """

    def __init__(self, name, mode="internal", dimage=None, ext_broker_ip=None, volumes=[], **kwargs):
        self.mode = mode

        if mode == "external" and ext_broker_ip == None:
            raise Exception("external broker ip needed to use external mode")
        elif mode != "internal" and mode != "external":
            raise Exception(f"'{mode}' is not a broker mode")

        kwargs["dimage"] = dimage
        kwargs["volumes"] = volumes
        Docker.__init__(self, name, **kwargs)

        self.cmd("iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")

    def run(self):
        # Docker.start(self)

        if self.mode == "internal":
            makeTerm(
                self, cmd=f'bash -c "mosquitto -c {VOLUME_FOLDER}/mosquitto.conf"')
        elif self.mode == "external":
            self.ext = ExtBroker()
            self.ext.run_ext_brk()
        else:
            raise Exception(
                f"Invalid broker type:{self.general.get('broker')}")
        time.sleep(2)

    def terminate(self):
        Docker.terminate(self)
        if self.mode == "external":
            self.ext.stop_ext_brk()
