import smtplib
from email.message import EmailMessage

def sendStaus(rpidescription, location, IPAddress, value, flag):
    email = "labemail@gmail.com"
    password = "********"
    
    try:
        # starting the smtplib server 
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        server.login(email, password)
        
        #Create an object to fill in information to be used to send and email
        msg = EmailMessage()
        if flag == "temp":
            text = "Temperature: {} \nLocation: {} \nIPAddress: {}".format(value,location,IPAddress)
        else:
            text = "Light: {} \nLocation: {} \nIPAddress: {}".format(value,location,IPAddress)
        
        msg.set_content(text)
        
        if flag == "temp":
            msg['Subject'] = "({}-pi3-{})Abnormalities in temperature".format(rpidescription,location)
        else:
            msg['Subject'] = "({}-pi3-{})Abnormalities in Light".format(rpidescription,location)
        msg['From'] = email
        msg['To'] = []
        
        # send email
        server.send_message(msg)
        
        #closing the connection
        server.quit()
    except Exception as e:
        print("Error: {}".format(e))




