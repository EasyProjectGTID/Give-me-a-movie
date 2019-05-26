import huey

from PTUT import HUEY


@HUEY.task()
def write_post(quality):
	for i in range(100):
		print('toto')
	return True
