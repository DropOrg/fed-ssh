
import subprocess

if __name__ == '__main__':
	subprocess.run(['sudo', 'mkdir', '/usr/local/pemstore'])
	subprocess.run(['sudo', 'mkdir', '/usr/local/pemstore/certs'])
	subprocess.run(['chmod', '+x', 'generate_cert.sh'])