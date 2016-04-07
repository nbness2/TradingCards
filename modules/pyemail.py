from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText


def send_email(sendTo, text, subject, loginName, loginPass, ServerAddr, debug = False):
    msg = MIMEText(text, 'plain')
    msg['Subject'] = str(subject)
    msg['To'] = str(sendTo)
    try:
        conn = SMTP(str(ServerAddr))
        conn.set_debuglevel(debug)
        conn.login(str(loginName), str(loginPass))
        try:
            conn.sendmail(sendTo, sendTo, msg.as_string())
        finally:
            conn.close()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    sendEmail('sendto@email.domain', 'Test Email Body420', 'Test Email Subject69',
              'name@email.domain', 'password', 'smtp.gmail.com')
