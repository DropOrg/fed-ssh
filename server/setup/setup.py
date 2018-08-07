import subprocess

FED_SSH_PORT = 41738

if __name__ == '__main__':
	# start up mongo server + add username, password 
	subprocess.run(['./init_mongo.sh'])

	# modify mongo.conf to expose server
	subprocess.run(['./configure_mongo.sh'])

	# expose FED_SSH_PORT thru firewall 
	subprocess.run(['./expose_port.sh'])