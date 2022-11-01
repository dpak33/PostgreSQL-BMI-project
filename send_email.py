from email.mime.text import MIMEText
import smtplib

def send_email(email, height, weight, age, BMI, average_height, average_weight, count, BMI_message):
    from_email= 'd_pakenham@yahoo.co.uk'
    from_password= 'yflmvhqfjxztrmce'
    to_email = email

    subject = 'Collecting information'
# We specify both placeholders after the string below.
    message = 'Your height is <strong> %s </strong> and your weight is <strong> %s </strong>. Your age is <strong> %s </strong> and your BMI is <strong> %s </strong>. ' \
              'The average height of all users to date is %s while the average weight of all users is %s. That is calculated out of %s people. %s'  % (height, weight, age, BMI, average_height, average_weight, count, BMI_message)

    msg = MIMEText(message, 'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email

    yahoo=smtplib.SMTP('smtp.mail.yahoo.com',587)
    yahoo.ehlo()
    yahoo.starttls()
    yahoo.login(from_email, from_password)
    yahoo.send_message(msg)
