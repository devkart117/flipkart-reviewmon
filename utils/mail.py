import os
import datetime

import resend
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

target_email_list = [
    'dev.kartikaggarwal117@gmail.com',
    'kartik.aggarwal117@gmail.com',
    'ecom1@novuslifesciences.com',
    'ecom7@novuslifesciences.com',
    'ecom9@novuslifesciences.com',
    'ecom13@novuslifesciences.com',
    'ecom16@novuslifesciences.com'
]


def send_email(sender, to_list, subject, message_text, file_paths=[]):

    attachments = [
        {
            'content': list(open(filepath, 'rb').read()),
            'filename': filepath.split('/')[-1]
        } for filepath in file_paths
    ]

    params: resend.Emails.SendParams = {
        "from": sender,
        "to": to_list,
        "subject": subject,
        "html": message_text,
        "attachments": attachments
    }

    email = resend.Emails.send(params)
    logger.debug(f'Email sent: {email}')


def send_output_mail(sender='Delivery System <dev@kartikcodes.in>'):
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%d %B")
    send_email(sender, 
               target_email_list, 
               f'{formatted_date} - Flipkart Review sheet', 
               'This is an automated delivery.<br/><br/>Please find the Flipkart Review Sheet attached.', 
               ['data/output.xlsx'])


def send_error_mail(error, sender='Error Notification <dev@kartikcodes.in>'):
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%d %B")
    send_email(sender, 
               ['kartik.aggarwal117@gmail.com', 'dev.kartikaggarwal117@gmail.com'],
               f'{formatted_date} - Error while running AMAZON FLIPKART MONITORING script', 
               f'This is an automated message.<br/><br/>A critical error has occured while running the script: "{error}".<br/><br/>', 
               ['logs/script.log'])