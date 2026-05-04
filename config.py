import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
    DATA_DIR = os.environ.get('DATA_DIR', os.path.join(BASE_DIR, 'data'))
    WTF_CSRF_ENABLED = True

    @property
    def UPLOAD_TEMP_DIR(self):
        return os.path.join(self.DATA_DIR, 'tmp')

    @property
    def ANSWER_KEYS_DIR(self):
        return os.path.join(self.DATA_DIR, 'answer_keys')

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"sqlite:///{os.path.join(self.DATA_DIR, 'submissions.db')}"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    WTF_CSRF_ENABLED = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
