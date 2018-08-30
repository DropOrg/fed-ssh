import sys 
import subprocess

from MongoManager import MongoManager
from CertManager import CertManager

mm = MongoManager()
cm = CertManager()

def add_server(user, alias, ssh_string=None, group=None): 
	if ssh_string is None:
		return 

	cert_name = user + '_' + alias
	cm.add_cert(cert_name)
	mm.add_server(user, ssh_string, alias, cert_name)
	cm.upload_cert(cert_name, ssh_string)

	# store .pem cert as bytes in db
	cert_path = cm.get_cert_path(cert_name) 
	mm.store_cert(user, alias, cert_path)

	# remove temporary cert 
	cm.rm_temp_cert(user, alias)

	# download db cert
	mm.download_cert(user, alias)
	
def remove_server(user, alias, group=None):
	mm.rm_server(user, alias)
	mm.rm_cert(user, alias)
	cm.rm_cert((user + '_' + alias))

def tell(user, alias, script_path, group=None):
	# get metadata from db for hostname
	server_meta = mm.get_server(user, alias)
	host_name = server_meta['server_ssh_string']

	# make script executable, pass to server 
	subprocess.run(['chmod', '+x', script_path])
	subprocess.run(['ssh', host_name, '<', script_path])

def sync(user):
	# get all server and cert metadata
	all_servers = mm.get_all_servers(user)
	all_local_certs = cm.get_all_certs()
	dl_list, to_rm = [], []

	# find all certs not locally downloaded
	for serv in all_servers:
		s_user, s_alias = serv['user'], serv['alias']
		cert_name = s_user + '_' + s_alias
		if cert_name not in all_local_certs:
			dl_list.append((s_user, s_alias))

	# TODO: find all certs to remove 

	# download all missing certs
	for cert_meta in dl_list:
		mm.download_cert(*cert_meta)

def __purge_server(user, alias):
	# remove local cert and stored cert data
	mm.rm_cert(user, alias)
	cm.rm_cert(user, alias)

	# remove all server metadata
	mm.rm_server(user, alias)

def purge(user=None, alias=None, all_local=False):
	# delete specific local cert & stored metadata
	if user is not None and alias is not None:
		__purge_server(user, alias)
		return 

	# delete all local certs & all server metadata
	if all_local:
		all_local_certs = cm.get_all_certs()
		for cert_name in all_local_certs:
			# split cert_name into user & alias
			c_user, c_alias = cert_name.split('_')
			__purge_server(c_user, c_alias)

if __name__ == '__main__':
	action, target = sys.argv[1:3]
	fedssh_args = sys.argv[3:]

	# todo: add random sync 

	if action == 'add':
		if target == 'server':
			add_server(*fedssh_args)

	elif action == 'remove':
		if target == 'server':
			rm_server(*fedssh_args)

	elif action == 'tell':
		tell(target, *fedssh_args)

	elif action == 'purge':
		if target == 'all':
			purge(all_local=True)

	elif action == 'sync':
		sync(target)
