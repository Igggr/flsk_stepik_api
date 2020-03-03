class DebugConfig:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestConfig:
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductConfig:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
