# 경로 작업
# from pathlib import Path

from flask import Flask

# flask-login에 있는 LoginManger를 import
from flask_login import LoginManager  # type: ignore

# 마이그레이션 작업을 위해
from flask_migrate import Migrate  # type: ignore

# SQL작업을 위해
from flask_sqlalchemy import SQLAlchemy

# flask-wtf 모듈의 CSRFProtect import
from flask_wtf.csrf import CSRFProtect  # type: ignore

# config 모듈을 import
from apps.config import config

# SQLAlchemy 객체 생성
db = SQLAlchemy()

# CSRFProtect 객체 생성
csrf = CSRFProtect()

# LoginManager 객체 생성
login_manager = LoginManager()
# login_view 속성에 미로그인시 리다이렉트하는 엔드포인트를 지정
login_manager.login_view = "auth.login"
# login_message 속성 : 로그인시 표시할 메시지를 지정. 현재는 표시할 내용없어서 ""
# login_message는 기본값으로 설정되어 있어요. 영어로 값이 이미 존재함.
login_manager.login_message = ""


# create_app 함수 작성
def create_app(config_key):
    # 플라스크 인스턴스 생성
    app = Flask(__name__)

    # app에 config 설정
    app.config.from_object(config[config_key])
    # app.config.from_envvar("APPLICATION_SETTINGS")
    # app.config.from_pyfile("envconfig.py")
    # app.config.from_mapping(
    #     SECRET_KEY="VXNA6hHwn5sIuPQpZLxK",
    #     SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(__file__).parent / 'local.sqlite'}",
    #     SQLALCHEMY_TRACK_MODIFICATIONS=False,
    #     # SQL 콘솔 로그에 출력
    #     SQLALCHEMY_ECHO=True,
    #     WTF_CSRF_SECRET_KEY="El1oD921KMdGKONsydDa",
    # )

    # csrf 앱 연계
    csrf.init_app(app)

    # SQLAlchemy와 앱 연계
    db.init_app(app)
    # Migrate와 앱 연계
    Migrate(app, db)

    # login_manager를 app과 연계
    login_manager.init_app(app)

    # CRUD패키지로 부터 views 모듈을 import 한다.
    # views.py 모듈은 @app.route()와 같은 맵핑 기능을 가진 모듈
    from apps.crud import views as crud_views  # as 이후 별칭 선언

    # register_blueprint() 사용해 views(crud_views) blueprint에 등록
    # 엔드포인트 앞에 crud가 붙게 됨.
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    # AUTH 패키지로 부터 views 모듈을 import
    from apps.auth import views as auth_views

    # register_blueprint()로 blueprint 등록
    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    return app
