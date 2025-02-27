import time
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# TRACKING_URL = "https://127.0.0.1:5000/track?email=" # This site can’t provide a secure connection
# TRACKING_URL = "http://127.0.0.1:5000/track?email="           # flask runs on HTTP not HTTPS

# or use local IP address You can access this address from any device on the same Wi-Fi/network.
# TRACKING_URL = "http://<local IP>:5000/track?email="

# for production : i am using live url no need to start server manually 
TRACKING_URL = "https://emailtest.pythonanywhere.com/track?email="


sender_email = os.getenv("MY_EMAIL")
app_password = os.getenv("MY_PASSWORD")

df = pd.read_csv('sample_emails.csv')
# df = pd.read_excel('sample_emails.xlsx')

def test_job():
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)

        for _ , row in df.iterrows():
            receiver_email = row.get('Email') or row.get('email')
            receiver_name = row.get('Name') or row.get('name') or row.get('Username') or row.get('username')

            if not receiver_email:
                print("Email not found")
                continue

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = "Test Email"

            email_body = f"""
                            <html>
                            <body>
                                <p>Hello, this is a test email with tracking.</p>
                                <img src="{TRACKING_URL}{receiver_email}" width="1" height="1" style="display:none;" />
                            </body>
                            </html>
                        """

            message.attach(MIMEText(email_body, "html"))
            # print(TRACKING_URL+receiver_email)       # for developmet checks
            try:
                server.sendmail(sender_email, receiver_email, message.as_string())
            except Exception as e:
                print(f"Error : {str(e)}")
            else:
                print("Email sent successfully!")

scheduler = BackgroundScheduler()
# job = scheduler.add_job(test_job, 'interval', seconds=2 , max_instances=3)
# job = scheduler.add_job(test_job , 'cron' , hour="15" , minute="8") # this is from production purpose just add time
job = scheduler.add_job(test_job) # ths is for development purposse
scheduler.start()


# try:
#     while True:
#         time.sleep(1)
# except (KeyboardInterrupt, SystemExit):
#     scheduler.shutdown()
#     print("Stopped")