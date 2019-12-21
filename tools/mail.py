from lg.credential_email import EMAIL_USE_TLS, EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT, \
    EMAIL_FROM
import smtplib
from email.message import EmailMessage


def send_mail_smtp(subject, to, reply_to, text, html, attachments):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    if not isinstance(to, basestring):
        msg['To'] = ', '.join(to)
    else:
        msg['To'] = to
    # if reply_to :
    #    msg.add_header('reply-to', reply_to)
    # msg.attach(MIMEText(text, 'plain'))
    msg.set_content(text)
    msg.add_alternative(html, subtype='html')
    for path in attachments:
        if not os.path.isfile(path):
            continue
        ctype, encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        with open(path, 'rb') as fp:
            msg.add_attachment(fp.read(),
                               maintype=maintype,
                               subtype=subtype,
                               filename=filename)

    s = smtplib.SMTP()
    s.connect(EMAIL_HOST, EMAIL_PORT)
    if EMAIL_USE_TLS:
        s.starttls()
    s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    s.send_message(msg)
    s.quit()
