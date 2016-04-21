from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText


def send_email(sendTo, text, subject, loginName, loginPass, ServerAddr, debug = False):
    msg = MIMEText(text, 'plain')
    msg = MIMEText(message_body, 'plain')
    msg['Subject'] = str(subject)
    msg['To'] = str(send_to)
    try:
        conn = SMTP(str(server_addr))
        conn.set_debuglevel(debug)
        conn.login(str(login_name), str(login_pass))
        try:
            conn.sendmail(send_to, send_to, msg.as_string())
        finally:
            conn.close()
    except Exception as e:
        print(e)

    '''
    sendEmail('sendto@email.domain', 'Test Email Body420', 'Test Email Subject69',
              'name@email.domain', 'password', 'smtp.server.com')
    '''
