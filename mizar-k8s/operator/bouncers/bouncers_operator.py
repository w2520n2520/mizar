from bouncers.bouncer import Bouncer
from vpcs.vpcs_store import VpcStore
from droplets.droplets_store import DropletStore
import logging

logger = logging.getLogger()

class BouncerOperator(object):
	_instance = None

	def __new__(cls, **kwargs):
		if cls._instance is None:
			cls._instance = super(BouncerOperator, cls).__new__(cls)
			cls._init(cls, **kwargs)
		return cls._instance

	def _init(self, **kwargs):
		logger.info(kwargs)
		self.ds = DropletStore()
		self.vs = VpcStore()

	def on_delete(self, body, spec, **kwargs):
		name = kwargs['name']
		logger.info("*delete_bouncer {}".format(name))

	def on_update(self, body, spec, **kwargs):
		name = kwargs['name']
		ip = spec['ip']
		droplet = spec['droplet']
		vpc = spec['vpc']
		net = spec['net']
		vpc_obj = self.vs.get(vpc)
		net_obj = vpc_obj.get_network(net)
		droplet_obj = self.ds.get(droplet)
		logger.info("*update_bouncer {}, {}, {}, {}/{}, {}".format(name, ip, vpc, net, net_obj.name, net_obj.bouncers.keys()))
		bouncer = Bouncer(name, vpc, net, ip, droplet, droplet_obj)
		net_obj.update_bouncer(bouncer)

	def on_create(self, body, spec, **kwargs):
		self.on_update(body, spec, **kwargs)

	def on_resume(self, body, spec, **kwargs):
		self.on_update(body, spec, **kwargs)
