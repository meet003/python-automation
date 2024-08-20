import requests
import smtplib
import os
import paramiko
import warnings
import boto3
import time
import schedule
from dotenv import load_dotenv
from cryptography.utils import CryptographyDeprecationWarning
load_dotenv()

# Suppress specific warnings
warnings.filterwarnings(action='ignore', category=CryptographyDeprecationWarning)

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
PASSWORD = os.getenv('PASSWORD')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
INSTANCE_ID = os.getenv('INSTANCE_ID')
EC2_REGION = os.getenv('EC2_REGION')
IP_ADDRESS = os.getenv('IP_ADDRESS')
KEY_FILE_PATH = os.getenv('KEY_FILE_PATH')


def send_notification(email_msg):
    with smtplib.SMTP('smtp.gmail.com' , 587) as smtp:
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_ADDRESS ,PASSWORD)
            message = f"Subject: SITE DOWN\n\n{email_msg}"
            smtp.sendmail(EMAIL_ADDRESS ,EMAIL_ADDRESS ,message)

def restart_application():
    # restart the application
    print("Attempting to restart the application")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=IP_ADDRESS, username='ubuntu', key_filename=KEY_FILE_PATH, timeout=30)
        stdin,stdout,stderr = ssh.exec_command('sudo docker restart d27097e7f43d')
        print(stdout.readlines())
    except Exception as e:
        print(f"Failed to connect or execute command: {e}")
    finally:
        ssh.close()

def restart_server_and_container():
    print('Rebooting the server...')
    ec2 = boto3.client('ec2', region_name=EC2_REGION, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    ec2.reboot_instances(InstanceIds=[INSTANCE_ID])

    # Wait for the instance to be running
    ec2_resource = boto3.resource('ec2', region_name=EC2_REGION, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    instance = ec2_resource.Instance(INSTANCE_ID)
    instance.wait_until_running()

    # restart the application
    while True:
        instance.reload()
        if instance.state['Name'] == 'running':
            time.sleep(8)
            restart_application()
            break

# def monitor_application():
try:
    url = f'http://{IP_ADDRESS}:8080/'
    response = requests.get(url)
    
    # print(response.text)
    if response.status_code == 200:
        print('Application is running successfully!')
    else:
        print('Application down')
        #send email to me 
        msg = f'Application is down '
        send_notification(msg)
        restart_application()
      
except Exception as ex:
    print(f'connection  error  happened: {ex}')
    msg = f'Application is accessible to all'
    send_notification(msg)
    restart_application()



# schedule.every(5).minutes.do(monitor_application)

# while True:
#     schedule.run_pending()


#send email 
# https://myaccount.google.com/lesssecureapps
# https://myaccount.google.com/u/1/apppasswords
