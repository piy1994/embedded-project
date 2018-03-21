# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
from imutils.video import VideoStream
from picamera.array import PiRGBArray
from picamera import PiCamera
import sending_sms as sms # sms.send_sms()
import sending_email_image as send_email # send_mail()
import RPi.GPIO as GPIO
import gui as gu

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)


from time import sleep
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())
image_filename = 'fire_image.jpg'

gu.main_gui()


camera = PiCamera()
camera.resolution = (320,240)
#camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320,240))


time.sleep(0.1)

# initialize the first frame in the video stream
firstFrame = None
flag_sent = 0
iter = 0


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=False):
        image = frame.array

        rawCapture.truncate(0)
	text = "Normal"

	
	image = imutils.resize(image, width=500)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue

	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	# thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.threshold(frameDelta, 100, 255, cv2.THRESH_BINARY)[1]  # 100

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"]:
			continue

		text = "Fire Detected!"
		iter+=1
                if iter>5 and flag_sent==0:
			cv2.imwrite(image_filename,image)
	                sms.send_sms()
        	        send_email.send_mail(image_filename)
                	flag_sent=1
			iter=0

		
	#cv2.imshow("Status", gray)
	#cv2.moveWindow("Security Feed", 20, 20)
	
	print(text)
	if text == "Fire Detected!":
		GPIO.output(17,GPIO.HIGH)
        else:
        	GPIO.output(17,GPIO.LOW)

	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

	sleep(0.05)


print 'release'
# cleanup the camera and close any open windows
#camera.release()
cv2.destroyAllWindows()
GPIO.cleanup()

