import subprocess

class redis_node():
	# implements a redis server node
	
	p = None #server process holder
	capacity = 0
	num_filled = 0;
	
	def __init__(self):
		# does nothing
		print "node started"
	
	def start_server(self, port):
		#starts a server with defined port
		try:
			p = subprocess.Popen(["redis-server","--port", str(port)], stdout = subprocess.PIPE, stderr=subprocess.PIPE)
			print "server at "+str(port)
		except subprocess.CalledProcessError as e:
			print("Oops... returncode: " + e.returncode + ", output:\n" + e.output) 
	
	
	def kill_server(self):
		#kills a server if its reliablity level is 0
		if p is not None:
			p.kill()
		else:
			print "process does not exit"
		
	def put(self, port, key, value):
		#adds a key value to the node
		print "PUT "+str(key)+" value "+str(value)+" at port "+str(port)
		ret = subprocess.check_output(["redis-cli","-p", str(port), "set", str(key), str(value)])
		return ret

	def get(self, port, key):
		#return value associated with the key
		ret = subprocess.check_output(["redis-cli","-p", str(port), "get", str(key)])
		return ret.rstrip('\n')
	
