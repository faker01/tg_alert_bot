import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from mailcfg.config import from_email, password
from platform import python_version
from jinja2 import Template


def mail_out(to_email, title, text):
    msg = MIMEMultipart('alternative')
    with open('methods/mailcfg/main.html', 'r', encoding="utf-8") as f:
        html = f.read()
        f.close()
    html = Template(html).render(title=title, text=text)
    message = 'Сообщение сделано при помощи python'
    msg['To'] = to_email
    msg['Subject'] = title
    msg['From'] = f'tgbot <{from_email}>'
    msg['Reply-To'] = from_email
    msg['Return-Path'] = from_email
    msg['X-Mailer'] = 'Python/' + (python_version())


    msg.attach(MIMEText(message, 'plain'))
    msg.attach(MIMEText(html, 'html'))


    server = smtplib.SMTP_SSL('smtp.yandex.ru:465')
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()
    print('Письмо отправленно')