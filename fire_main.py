import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--area", help="minimum area size")
args = vars(ap.parse_args())

#print args["video"]
#print args["area"]
# if the video argument is None, then we are reading from webcam

if args.get("video", None) is None:
	if args.get("area",None) is None:
		python_str = 'sudo python fire_det.py'
	else:
		python_str = 'sudo python fire_det.py -a {}'.format(args["area"])

# otherwise, we are reading from a video file
else:
	if args.get("area",None) is None:
                python_str = 'sudo python fire_det_v.py -v {}'.format(args["video"]) 
        else:
                python_str = 'sudo python fire_det_v.py -v {} -a {}'.format(args["video"],args["area"])
print python_str
#execfile(python_str)
os.system(python_str)

