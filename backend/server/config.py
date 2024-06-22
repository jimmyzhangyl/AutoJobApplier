# config.py


class Config:
    TESTING = False
    DEBUG = False
    # other configurations


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    # other test-specific configurations
