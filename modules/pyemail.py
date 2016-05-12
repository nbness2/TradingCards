from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText


def send_email(params):
    send_to, message_body, subject, login_name, login_pass, server_addr, debug = params
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
