import redis_server
import argparse

rs = {}  # a dictionary to store redis serevr objects
reliability_lev = 5

def bringUP(N, capacity, reliabilityLevel, port):
	#starts up somenodes with cap, and rel level
	global reliability_lev
	for i in range(0,N):
		redis_s = redis_server.redis_node()
		ret = redis_s.start_server(port)
		print ret
		redis_s.capacity = capacity
		reliability_lev = reliabilityLevel
		rs.update({port : redis_s})
		port += 1   # increment the port number
	

def failNode(port):
	#stops a node if the reliability level has become 0 
	global reliability_lev
	if len(rs) is not 0:
		if rs.has_key(port):
			if reliability_lev == 0:
				rs[port].kill_server
				print "node killed at port "+str(port)
			
			else:
				reliability_lev -= 1
				print "new reliability level "+ str(reliability_lev)
	
	else:
		print "node list is empty or does not have the node"


def put(key, value):
	# check if a key is in some node and update it
	if len(rs) is not 0: 
		for red_p, red_s in rs.iteritems():
			if red_s.get(red_p, key) is not '' :
				ret = red_s.put(red_p, key, value)
				print ret
				red_s.num_filled += 1
				return
		# key is not in any node, insert it in first node if it has capacity, else go to next node
		for red_p, red_s in rs.iteritems():
			if red_s.num_filled < red_s.capacity:
				ret = red_s.put(red_p, key, value)
				print ret
				return
			else:
				 print "checking node capacity. So far FULL"
			 

def get(key):
	#search and find a value of a key
	for red_p, red_s in rs.iteritems():
		if red_s.get(red_p, key) is not '':
			print "Key "+str(key)+" value is "+red_s.get(red_p, key)
			return 
		else:
			print "checking for key "+str(key)+", not found so far"

if __name__=="__main__":
	
	parser = argparse.ArgumentParser("Test redis server")
	parser.add_argument('--N', help="num servers", default = 5)
	parser.add_argument('--C', help="capacity of each server", default = 10)
	parser.add_argument('--R', help="Reliabilityvalue", default = 5)
	parser.add_argument('--port', help="starting port num", type=int, default = 6789)
	parser.add_argument('--start', help="flag to start server",default=False, action="store_true")
	args = parser.parse_args()

	if args.start:
		
		#to check starting the redis service
		bringUP(args.N, args.C, args.R, args.port)
		#to check put command
		put("abc", 123)
		put("foo", 23)
		put("foo2", 345)
		put("foo3", 345)
		put("foo4", 345)
		put("foo5", 345)
		put("foo6", 345)
		
		# to check failnode command and reliability value
		failNode(args.port)
		failNode(args.port+1)
		failNode(args.port+1)
		failNode(args.port+2)
		
		#to check get command and the reliability of the node
		get("abc")
		get("foo")
		
		#to check for the key that does not exit 
		get("foo3")
		
		# finally to kill a node
		failNode(args.port)
		failNode(args.port)
		failNode(args.port+2)
		failNode(args.port+3)
		
		# now check that some keys are dissappeared
		get("abc")
		get("foo2")
		get("foo3")
		get("foo")
		
	
	
