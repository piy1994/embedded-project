import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
def send_mail(img_file):
	smtpUser = 'embeddedfire@gmail.com'
	smtpPass = 'firedetection'
	toAdd = 'piyushdugar13@gmail.com'

	
	img_data = open(img_file,'rb').read()
	msg = MIMEMultipart()
 	msg['Subject'] = 'Testing email feature'
	msg['From'] = smtpUser
	msg['To'] = toAdd 


	text = MIMEText('Fire Detected !!!!!!!!!. Take Action.')
	msg.attach(text)
	image = MIMEImage(img_data,name = os.path.basename(img_file))
	msg.attach(image)

	#print header +  '\n' + body

	s = smtplib.SMTP('smtp.gmail.com',587)

	s.ehlo()
	s.starttls()
	s.ehlo()

	s.login(smtpUser, smtpPass)
	#print(msg.as_string())
	s.sendmail(smtpUser, toAdd,msg.as_string())

	s.quit()
	return 0

if __name__ == "__main__":
	img_file = 'Fire_image.jpg'
	send_mail(img_file)
