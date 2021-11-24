# config.py

class Config(object):
    """
    Common configurations
    """

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True
    SITE_NAME = 'Botanic Garden'

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    SITE_NAME = 'Botanic Garden'

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}