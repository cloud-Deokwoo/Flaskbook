from pathlib import Path

SECRET_KEY = "VXNA6hHwn5sIuPQpZLxK"
SQLALCHEMY_DATABASE_URI = f"sqlite:///{Path(__file__).parent / 'local.sqlite'}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
WTF_CSRF_SECRET_KEY = "El1oD921KMdGKONsydDa"
