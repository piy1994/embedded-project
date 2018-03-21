import requests

def send_sms():
	str = 'https://maker.ifttt.com/trigger/Fire/with/key/ch15rck3SXDS0vFL0R6Qec'
	requests.post(str)
	return 0

if __name__ == "__main__": 
	send_sms()
