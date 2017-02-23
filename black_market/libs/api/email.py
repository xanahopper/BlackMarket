from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

from black_market.config import EMAIL_PASSWORD

import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_email_to(to_addr, content):
    from_addr = 'mew0629@qq.com'
    password = EMAIL_PASSWORD
    smtp_server = 'smtp.qq.com'

    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr('Black-Market')
    msg['To'] = _format_addr('Black-Marlet-Users')
    msg['Subject'] = Header('Black Market Notification', 'utf-8').encode()
    try:
        server = smtplib.SMTP(smtp_server, 587)
        server.starttls()
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
    except Exception:
        pass
