import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_confirmation_code(email, userName, code):
    sender_email = 'kemetekem@gmail.com'
    password = "mynf otow bhlv aqpi"
    smtp = "smtp.gmail.com"

    reciver_email = email
    subject = "Doğrulama Koodu"
    content = f"""
    <p style='font-size: 18px; color: #333; font-family: Arial, sans-serif;'>Sayın {userName},</p> 
    <p style='font-size: 16px; color: #555; font-family: Arial, sans-serif;'>"🎉 Uygulamamıza Hoşgeldiniz ! 🛍️"</p>
    <div style='background-color: #f5f5f5; padding: 15px; border-radius: 8px; margin: 15px 0;'>
        <p style='font-size: 16px; color: #333; font-family: Arial, sans-serif;'>Eğlenmeye Başalamak Üzeresiniz!</p>
        <p style='font-size: 24px; color: #ff6600; font-family: Arial, sans-serif; font-weight: bold;'>Doğrulama Koodunuz: {code}</p>
    </div>
    <p style='font-size: 16px; color: #555; font-family: Arial, sans-serif;'>Kayıt olduğunuz için teşekkür ederiz.</p>
    <p style='font-size: 16px; color: #555; font-family: Arial, sans-serif;'>Hayırlı Olsun 🥰</p>
    """

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = reciver_email
    msg['Subject'] = subject

    # Attach HTML message
    msg.attach(MIMEText(content, 'html'))

    # Send the email
    server = smtplib.SMTP(smtp, 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, reciver_email, msg.as_string())
    server.quit()

    print(f"Email has been sent to {reciver_email}")
