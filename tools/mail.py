from lg.credential_email import EMAIL_USE_TLS, EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT, EMAIL_USE_SSL
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage


def send_mail_smtp(subject, from_email, to, reply_to, text, html):
    print(subject)
    print(from_email)
    print(to)
    print(text)
    print(html)
    # msg = MIMEMultipart('alternative')
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to
    #if reply_to :
    #    msg.add_header('reply-to', reply_to)
    #msg.attach(MIMEText(text, 'plain'))
    #msg.attach(MIMEText(html, 'html'))
    msg.set_content(text)
    s = smtplib.SMTP()
    s.connect( EMAIL_HOST, EMAIL_PORT)
    s.starttls()
    s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    # print(msg)
    #s.sendmail(from_email, to, msg.as_string())
    s.send_message(msg)
    s.quit()
