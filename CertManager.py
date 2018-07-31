import subprocess 
from constants import CERTS_LOC

class CertManager:
	def __init__(self):
		self.sudo = 'sudo'
		self.gen_cert_exec = './generate_cert.sh'
		self.upl_cert_exec = './upload_cert.sh'

	def get_all_certs(self):
		all_certs = (subprocess.run(['ls', CERTS_LOC], stdout=subprocess.PIPE)).stdout
		raw_certs = all_certs.decode('utf-8').split('\n')
		return raw_certs[:len(raw_certs)-1]

	def get_cert_path(self, cert_name):
		if self.cert_exists(cert_name):
			return CERTS_LOC + '/{}'.format(cert_name)

	def cert_exists(self, cert_name):
		all_certs = self.get_all_certs()
		for cert in all_certs:
			if cert == cert_name:
				return True
		return False

	def upload_cert(self, cert_name, ssh_target):
		cert_path = self.get_cert_path()
		subprocess.run([self.sudo, self.upl_cert_exec, cert_path, cert_name, ssh_target])	

	def add_cert(self, cert_name):
		if self.cert_exists(cert_name) is False:
			subprocess.run([self.sudo, self.gen_cert_exec, cert_name])
			return True
		else: 
			print('ERROR: CERT {} already exists'.format(cert_name))
			return False

	def rm_cert(self, cert_name):
		if self.cert_exists(cert_name):
			to_rm_loc = CERTS_LOC + '/{}'.format(cert_name)
			subprocess.run([self.sudo, 'rm', '-rf', to_rm_loc])
			return True
		else: 
			print('ERROR: CERT {} does not exist'.format(cert_name))
			return False

	def link(self, cert_name, ssh_target):
		if self.add_cert(cert_name):
			self.upload_cert(cert_name, ssh_target)
