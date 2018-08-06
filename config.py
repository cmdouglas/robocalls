import os
from urllib.parse import urlparse

redis_url = urlparse(os.environ.get('REDISCLOUD_URL'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    ACTION_NETWORK_KEY = os.environ.get('ACTION_NETWORK_KEY')

    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_SECRET = os.environ.get('TWILIO_SECRET')
    TWILIO_FLOW_SID = os.environ.get('TWILIO_FLOW_SID')
    TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')
    PHONE_RECIPIENT_OVERRIDE = os.environ.get('PHONE_RECIPIENT_OVERRIDE')

    REQUESTS_VERIFY = os.environ.get('REQUESTS_VERIFY')

    RQ_REDIS_URL = os.environ.get('REDISCLOUD_URL')
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')

    TESTING = os.environ.get('TESTING')


