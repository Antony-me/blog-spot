import os

class Config:

    SECRET_KEY = 'stuxnet993.'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")



class ProdConfig(Config):

    # SQLALCHEMY_DATABASE_URI ='postgres://vozpbxssyhgpof:2a079ee85e7338392be8fa3ec6027d4745f5d11d5d0e692cd3b07e7bdc0379c8@ec2-54-156-121-142.compute-1.amazonaws.com:5432/dcugjvtovf241p'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}