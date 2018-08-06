### IMPORTS ###
import time

### MAIN ###

class MongoManager:
	def __init__(self, mongo_client):
		self.mongo_client = mongo_client
		self.db = self.mongo_client.db['fedssh']
		self.servers = self.db['servers']
		self.certs = self.db['certs']

	### GETTERS ###
	def get_server(self, alias):
		return self.servers.find_one({'alias': alias})

	def get_all_servers(self):
		all_servers = []
		for serv in self.servers.find({}):
			serv.pop('_id')
			all_servers.append(serv)
		return tuple(all_servers)

	def add_cert(self, user, )

	### SETTERS ###
	def add_server(self, user, ssh_string, alias, cert_name):
		# check for already existing server
		all_servers = self.get_all_servers()
		for serv in all_servers:
			if serv['alias'] == alias:
				return {'result': 'ERROR: SERVER {} EXISTS'.format(alias)}

		# insert new server data
		new_server = {
		'user': user,
		'server_ssh_string': ssh_string,
		'alias': alias, 
		'cert_name': cert_name,
		'time_added': time.time()
		}

		self.servers.insert_one(new_server)
		return {'result': 'Created SERVER {} with CERT {}'.format(alias, cert_name)}

	def remove_server(self, alias):
		self.servers.remove_one({'alias': alias})

