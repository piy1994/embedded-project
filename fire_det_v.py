# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
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

# if the video argument is None, then we are reading from webcam

gu.main_gui()
if args.get("video", None) is None:
	camera = cv2.VideoCapture(0)
	time.sleep(0.25)

# otherwise, we are reading from a video file
else:
	camera = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
firstFrame = None
flag_sent = 0
iter = 0
# loop over the frames of the video

while True:
	# grab the current frame and initialize the occupied/unoccupied
	try:
		(grabbed, frame) = camera.read()
		text = "Normal"
		
	
		# if the frame could not be grabbed, then we have reached the end
		# of the video
		if not grabbed:
			break
	
		# resize the frame, convert it to grayscale, and blur it
		frame = imutils.resize(frame, width=500)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21, 21), 0)
	
		# if the first frame is None, initialize it
		if firstFrame is None:
			firstFrame = gray
			continue

		# compute the absolute difference between the current frame and
		# first frame
		frameDelta = cv2.absdiff(firstFrame, gray)
		thresh = cv2.threshold(frameDelta, 100, 255, cv2.THRESH_BINARY)[1]  # 100
	
		# dilate the thresholded image to fill in holes, then find contours
		# on thresholded image
		thresh = cv2.dilate(thresh, None, iterations=2)
		(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		# loop over the contours
		for c in cnts:
			# if the contour is too small, ignore it
			if cv2.contourArea(c) < args["min_area"]:
				#GPIO.output(17,GPIO.LOW)
				continue

			# compute the bounding box for the contour, draw it on the frame,
			# and update the text
			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			text = "Fire Detected!"

			iter+=1
			if iter>5 and flag_sent==0:
				cv2.imwrite(image_filename,frame)
				sms.send_sms()
				send_email.send_mail(image_filename)
				flag_sent=1
				iter=0
			
			#print(text)
	
		# draw the text and timestamp on the frame
		print(text)
		if text == "Fire Detected!":
			GPIO.output(17,GPIO.HIGH)
		else:
			GPIO.output(17,GPIO.LOW)
	
		cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
			(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

		# show the frame and record if the user presses a key
		cv2.imshow("Status_", frame)
		#cv2.moveWindow("Status", 20, 20)
		
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key is pressed, break from the lop
		if key == ord("q"):
			break
		sleep(0.05)

	except:
		key = raw_input('Enter password')
		if key == '123':
			break
		else:
			pass
	
# cleanup the camera and close any open windows
print('camera release')
cv2.destroyWindow("Status__")
camera.release()
cv2.destroyAllWindows()
GPIO.cleanup()
