import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'U2Kl7#oE3CbCxwQ1Fxqt1Ukt3Ha%243&'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgres://diaryuser:diarypassword@localhost:5432/diary'

    SQLALCHEMY_TRACK_MODIFICATIONS = False