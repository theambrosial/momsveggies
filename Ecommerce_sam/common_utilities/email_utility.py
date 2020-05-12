import threading
from django.core.mail import EmailMessage, send_mail


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content,sender, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.sender = sender
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, self.sender, self.recipient_list)
        msg.content_subtype = 'html'
        msg.send()


def send_html_mail(subject, html_content,sender, recipient_list ):
    EmailThread(subject, html_content,sender, recipient_list).start()

class Email_text_Thread(threading.Thread):
    def __init__(self, subject, message, sender,recipient):
        self.subject = subject
        self.recipient = recipient
        self.message = message
        self.sender = sender
        threading.Thread.__init__(self)

    def run(self):
        try:

            send_mail(self.subject, self.message, self.sender, self.recipient)
            print('email sent')
        except:
            print('exception occured email not sent')
            pass


def send_text_mail(subject, message, sender, recipient):
    Email_text_Thread(subject, message, sender, recipient).start()


class Email_Attach_Thread(threading.Thread):
    def __init__(self, subject, message, sender,recipient, attachment_name, file, attachment_type):
        self.subject = subject
        self.recipient = recipient
        self.message = message
        self.sender = sender
        self.attachment_name = attachment_name
        self.file = file
        self.attachment_type = attachment_type
        threading.Thread.__init__(self)

    def run(self):
        try:
            email_send = EmailMessage(self.subject, self.message, self.sender, self.recipient)
            email_send.attach(self.attachment_name, self.file, self.attachment_type)
            email_send.send()

        except:
            print('exception occured email not sent')
            pass


def send_attach_mail(subject, message, sender, recipient):
    Email_Attach_Thread(subject, message, sender, recipient, attachment_name, file, attachment_type).start()
    '''
    Usage:
    recipient = ['vikas.pandey@gmail.com','xyz@gmail.com',]
    attachment_name = 'Invoicex.pdf'
    file = 'attach.pdf'
    attachment_type = 'application/pdf'
    '''