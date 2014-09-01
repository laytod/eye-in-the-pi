import io
import time
import picamera
import subprocess

camera = picamera.PiCamera()

# camera default settings
camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.ISO = 0
camera.video_stabilization = False
camera.exposure_compensation = 0
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 0
camera.hflip = False
camera.vflip = False
camera.crop = (0.0, 0.0, 1.0, 1.0)


# changes
camera.vflip = True
camera.hflip = True

if __name__ == '__main__':
	# path = '/home/pi/flask/cameraPi/static/camera'

	# write to shared memory (RAM) so we don't wear out the SD card
	path = '/run/shm/'
	count = 0

	print 'Taking pictures and saving them to {path}/image.jpg'.format(path=path)
	print 'press ^C to quit.'

	cmd = """convert -font helvetica -pointsize 20 -fill black -draw "text 430,470 '$(date)'" {path}tmp.jpg {path}image.jpg
	""".format(path=path)
	# loop forever taking pictures
	while True:
		# try:
		print 'taking picture {num}'.format(num=count)
		camera.capture('{path}/tmp.jpg'.format(path=path))
		


		subprocess.call(cmd, shell=True)

		# subprocess.call('cp {path}/tmp.jpg {path}/image.jpg'.format(path=path), shell=True)
		count += 1
		# except Exception:
		# 	camera.close()


































