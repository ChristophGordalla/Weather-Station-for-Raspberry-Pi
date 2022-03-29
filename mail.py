import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os.path




"""
Class to send mails from a gmail account by Python.

On the following webpage, you will find detailed instructions on the code
and on how to setup your gmail account for script base mail sending:

https://stackabuse.com/how-to-send-emails-with-gmail-using-python/

Please note that this approach requires your password
to be passed in plaintext. So, you might want to create 
a separate gmail account.

Members:
    files       string list, files to be attached to the mail
    sender      string, email address of the sender
    password    string, password of the sender's mail account (in plaintext)
    recipents   string list, email addresses of the recipents
    subject     string, subject of the mail
    message     string, message of the mail
    is_bcc      boolean, if True, recipents are put into blind copy
"""
class MailSender:
    
    """
    Constructor, sets the files to be send (through their absolute paths),  
    the mail's sender, password, recipents, subject, and message (all as strings), 
    and whether the recipents should be put into blind copy 
    (through the boolean is_bcc, True by default).
    """
    def __init__(self, files, sender, password, recipents, subject, message, is_bcc=True):
        self.files = files
        self.sender = sender
        self.password = password
        self.recipents = recipents
        self.subject = subject
        self.message = message
        self.is_bcc = is_bcc
        

    
    """
    Sends the mail. 
    """
    def send_gmail(self):
        msg = MIMEMultipart()
        msg['From'] = self.sender
        # for sending bcc messages, leave the following line outcommented
        if not self.is_bcc:
            msg['To'] = self.recipents
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.message, 'html'))
                
        for my_file in self.files:
            my_type = my_file.split('.')[-1]
            with open(my_file, 'rb') as fp:
                fle = MIMEImage(fp.read(), _subtype=my_type)
            fle.add_header('Content-Disposition', 'attachment; filename= %s' % os.path.split(my_file)[-1])
            msg.attach(fle)
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(msg['From'], self.password)
        server.sendmail(msg['From'], self.recipents, msg.as_string())
        server.quit()


