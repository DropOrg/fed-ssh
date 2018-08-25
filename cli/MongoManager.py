### IMPORTS ###
import time

### MAIN ###

class MongoManager:
	def __init__(self, mongo_client):
		self.mongo_client = mongo_client
		self.db = self.mongo_client.db['fedssh']
		self.servers = self.db['servers']
		self.certs = self.db['certs']
		self.perm_certs_path = '/usr/local/fedssh/perm_certs'

	### GETTERS ###
	def get_server(self, alias):
		return self.servers.find_one({'alias': alias})

	def get_all_servers(self):
		all_servers = []
		for serv in self.servers.find({}):
			serv.pop('_id')
			all_servers.append(serv)
		return tuple(all_servers)

	def __get_cert_as_str(self, user, alias):
		user_alias = self.certs.find_one(
			{'user':user, 'alias':alias})
		return user_alias['cert_bytes'].decode('utf-8')

	def store_cert(self, user, alias, cert_path):
		with open(cert_path, 'rb') as cert_file:
			cert_bytes = cert_file.read()
			new_cert = {'user': user, 'alias': alias, 'cert_bytes': cert_bytes}
			self.certs.insert_one(new_cert)

		return {'result': 'STORED CERT {}_{} IN CERTS'.format(user, alias)}

	def download_cert(self, user, alias):
		cert_name = user + '_' + alias + '.pem'
		dl_path = self.perm_certs_path + '/' + cert_name 
		with open(dl_path, 'w') as cert_copy:
			cert_copy.write(self.__get_cert_as_str(user, alias))
		return dl_path

	def rm_cert(self, user, alias):
		self.certs.remove_one({'alias': alias, 'user': user})

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

	def rm_server(user, alias):
		self.servers.remove_one({'alias': alias, 'user':user})

