# snapshot.py
# Michael Snider
#
# Main script for running the application
import sys
from twython import Twython
import os
from os import path
import picamera
import time
import subprocess

CONSUMER_KEY = ""
CONSUMER_SECRET = ""



def main():
	""" Main function for application """
	global CONSUMER_KEY
	global CONSUMER_SECRET

	# Handle command line parameters
	if len(sys.argv) > 2:
		print "Incorrect number of command line parameters, expecting <= 1 additional, received %d" % (len(sys.argv), )
		sys.exit(1)
	elif len(sys.argv) == 2:
		# From file
		with open(sys.argv[1], 'r') as input_file:
			lines = input_file.read().splitlines()

			if len(lines) < 4:
				print "Not enough lines in input file for necessary authorization."
				sys.exit(2)

			CONSUMER_KEY = lines[0]
			CONSUMER_SECRET = lines[1]
			key = lines[2]
			secret = lines[3]

	else:
		# From input
		CONSUMER_KEY = raw_input("Consumer Key: ")
		CONSUMER_SECRET = raw_input("Consumer Secret: ")
		key = raw_input("Access Token Key: ")
		secret = raw_input("Access Token Secret: ")


	twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, key, secret)

	#test_img_upload(twitter)
	#raspi_pic(twitter)
	raspi_usb_camera_pic(twitter)



def upload_img(twitter, img, status_msg):
	""" Upload an image to twitter """
	media_response = twitter.upload_media(media=img)
	response = twitter.update_status(status=status_msg, media_ids=[media_response['media_id']], display_coordinates=True)
	
	return response['entities']['media'][0]['media_url_https']


def raspi_pic(twitter):
	""" Capture a picture with the raspberry pi's camera and upload """

	with picamera.PiCamera() as camera:
		camera.resolution = (1280, 720)
		camera.start_preview()
		time.sleep(2)
	
		camera.capture('temp.jpg')
		status = raw_input("Enter status: ")
		print upload_img(twitter, open('temp.jpg', 'rb'), status)
		os.remove('temp.jpg')

def raspi_usb_camera_pic(twitter):
	""" Capture a picture with usb camera on raspberry pi with fswebcam """

	if subprocess.call(["fswebcam", "-r", "1280x720", "-D", "2", "--no-banner", "temp.jpg"]) != 0:
		print "An error occurred while taking image using fswebcam!"
		return

	status = raw_input("Enter status: ")
	print upload_img(twitter, open('temp.jpg', 'rb'), status)
	os.remove('temp.jpg')





def test_img_upload(twitter):
	""" A test function to attempt uploading a user-enter image and status """
	img_loc = raw_input("Enter path to image: ")

	if not path.isfile(img_loc):
		print "Invalid image path %s" % (img_loc, )
		return

	status = raw_input("Enter status: ")
	print upload_img(twitter, open(img_loc, 'rb'), status)


def print_info(key, secret):
	""" Print collected command line parameter info """
	print "Consumer Key:", CONSUMER_KEY
	print "Consumer Secret:", CONSUMER_SECRET
	print "Access Token Key:", key
	print "Access Token Secret:", secret


if __name__ == "__main__":
	main()
