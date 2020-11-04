import os

class Config:

    SECRET_KEY = 'stuxnet993.'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:Access@localhost/blogspot'

   

    #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")



class ProdConfig(Config):

    pass

    # SQLALCHEMY_DATABASE_URI ='postgres://vfgysrcwsqfxal:ad7f3f1e5d3141e4b26d53b01268bd7e9afdadbba5682686aa18a394794e4db2@ec2-34-231-56-78.compute-1.amazonaws.com:5432/dbdd0icu7a7i5v'

class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}