import sys 
import subprocess

from MongoManager import MongoManager
from CertManager import CertManager

mm = MongoManager()
cm = CertManager()

def add_server(user, alias, ssh_string): 
	cert_name = user + '_' + alias
	cm.add_cert(cert_name)
	mm.add_server(user, ssh_string, alias, cert_name)
	cm.upload_cert(cert_name, ssh_string)

	# store .pem cert as bytes in db
	cert_path = cm.get_cert_path(cert_name) 
	mm.store_cert(user, alias, cert_path)

	# remove temporary cert 
	cm.rm_cert(cert_name)
	
def remove_server(user, alias):
	mm.rm_server(user, alias)
	mm.rm_cert(user, alias)
	cm.rm_cert((user + '_' + alias))

def tell(user, alias, script_path):
	server_meta = mm.get_server(user, alias)
	host_name = server_meta['server_ssh_string']

	# make script executable, pass to server 
	subprocess.run(['chmod', '+x', script_path])
	subprocess.run(['ssh', host_name, '<', script_path])

def download_cert(user, alias):

def sync(user, alias):

if __name__ == '__main__':
	action, target = sys.argv[1:3]
	fedssh_args = sys.argv[3:]

	if action == 'add':
		if target == 'server':
			add_server(*fedssh_args)

	elif action == 'remove':
		if target == 'server':
			rm_server(*fedssh_args)

	elif action == 'tell':
		tell(target, *fedssh_args)
