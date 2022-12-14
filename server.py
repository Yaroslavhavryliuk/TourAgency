from agency import Agency
import Pyro4

if __name__ == '__main__':

	daemon = Pyro4.Daemon()
	uri = daemon.register(Agency)
	ns = Pyro4.locateNS()
	ns.register('agency', uri)
	daemon.requestLoop()