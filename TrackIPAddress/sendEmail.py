import smtplib
from email.message import EmailMessage

def sendStaus(currentIP, newIP, custom_message,flag,location,rpidescription):
    email = "TsaiLab.***@gmail.com"
    password = "****************"
    
    try:
        # starting the smtplib server 
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        server.login(email, password)
        
        #Create an object to fill in information to be used to send and email
        msg = EmailMessage()
        
        if flag==0:
            subjectText = "({}-pi3-{})the script/service was restarted".format(rpidescription,location)
        else:
            subjectText = "({}-pi3-{})IP change update".format(rpidescription,location)
        
        
        msg['Subject'] = subjectText
        msg['From'] = email
        msg['To'] = ["TsaiLab.********@gmail.com","******@uga.edu", "********@uga.edu"]
        text = f"""[{rpidescription}-pi3-{location}] The current IP {currentIP} has been updated to {newIP} here is the custom message: {custom_message}
        """
        msg.set_content(text)

        # send email
        server.send_message(msg)
        
        #closing the connection
        server.quit()
    except Exception as e:
        print("Error: {}".format(e))




