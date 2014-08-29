from fabric.api import env, task, local, run, sudo, hide

env.root_dir = env.real_fabfile.replace('fabfile.py', '')

@task(alias='copy')
def copy_repo():
	with hide('output', 'running'):
		hostname = str(local('hostname', capture=True))

	if hostname == 'TheDude':
		destination = 'pi@192.168.1.102:~/flask/'
	elif hostname == 'pibox':
		destination = 'TheDude:~/pi/flask/'
	else:
		print "unkown host '{hostname}'.".format(hostname=hostname)
		return

	with hide('running'):
		local('scp -r {root_dir}* {dest}'.format(root_dir=env.root_dir, dest=destination))


@task
def show_root_dir():
	print env.root_dir
