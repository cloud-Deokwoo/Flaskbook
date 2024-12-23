# db를 import
from flask import Blueprint, redirect, render_template, url_for

# login_required을 import
from flask_login import login_required  # type: ignore

from apps.app import db

# 만들둔 Form 클래스를 import
from apps.crud.forms import UserForm

# User 클래스를 import
from apps.crud.models import User

# Blueprint 객체 생성
crud = Blueprint(
    "crud",
    __name__,
    static_folder="static",
    template_folder="templates",
)


# 맵핑 정보 생성
@crud.route("/")
def index():
    return render_template("crud/index.html")


# 사용자 신규 등록을 위한 엔드포인트 작성
@crud.route("/users/new", methods=["GET", "POST"])
@login_required
def create_user():
    # UserForm 클래스를 인스턴스화
    form = UserForm()
    if form.validate_on_submit():  # submit 클릭시 검증에 문제가 없는 경우.
        # 사용자 정보 생성
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        # DB작업으로 사용자를 추가하고 커밋
        db.session.add(user)
        db.session.commit()

        # 사용자 일람 화면으로 리다이렉트
        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)


# 사용자 일람을 위한 엔드포인트 작업
@crud.route("/users")
@login_required
def users():
    """사용자 일람을 얻는 함수"""
    # uesrs = db.session.query(User).all()
    users = User.query.all()
    return render_template("crud/index.html", users=users)


# 사용자 편집을 위한 엔드포인트 작업
@crud.route("/users/<user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    form = UserForm()

    # User 모델을 이용하여 사용자를 취득
    user = User.query.filter_by(id=user_id).first()

    # form으로부터 제출된 경우는 사용자를 갱신하여 사용자의 일람 화면으로 리다이렉트
    if form.validate_on_submit():  # post 메서드로 수정 정보가 들어온 경우
        # 수정 내용을 적용
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        # DB에 적용
        db.session.add(user)  # primary_key의 값이 있는 경우 수정, 없으면 생성
        db.session.commit()
        return redirect(url_for("crud.users"))  # 수정 완료. 일람으로 이동

    # GET으로 접근한 경우 HTML을 반환
    return render_template("crud/edit.html", user=user, form=form)


# 사용자 삭제를 위한 엔드포인트 작성
@crud.route("/users/<user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    # 삭제할 정보를 불러오기
    user = User.query.filter_by(id=user_id).first()
    # 삭제 처리
    db.session.delete(user)
    # db에 반영
    db.session.commit()
    return redirect(url_for("crud.users"))


# SQL 테스트를 위한 endpoint 작성!
@crud.route("/sql")
def sql():
    # group by('컬럼명') : 컬럼의 내용을 그룹의 묶어줌
    # print(db.session.query(User).group_by("username").all())
    # order by('컬럼명') : 정렬하기...
    # print(db.session.query(User).order_by("id").all())
    # offset(값) : 값의 위치로 이동
    # print(db.session.query(User).limit(5).offset(5).all())
    # limit(값) : 가져올 레코드 수를 결정
    # print(db.session.query(User).limit(5).all())
    # where 구(filter) : 인수에 "모델명.속성 == 값"
    # print(
    #     db.session.query(User).filter(User.id == 2, User.username == "사용자명").all()
    # )
    # where 구(fiter_by) : SQL에서 조건이 들어가는 부분
    # print(db.session.query(User).filter_by(id=2, username="사용자명").all())
    # 페이지네이션 객체 가져오기 : 페이지네이션은 많은 레코드를 특정 갯수로 구분하여 출력.
    # paginate(page=None, per_page=None, error_out=True, max_per_page=None)
    #  page : 페이지 번호, per_page : 페이지당 레코드 갯수, max_per_page : 페이지 출력할 수 있는 최대 레코드
    # print(db.session.query(User).paginate(page=2, per_page=10, error_out=False))
    print(User.query.paginate(page=3, per_page=5, error_out=False))
    users = db.session.query(User).paginate(page=3, per_page=5, error_out=False)
    print(type(users))
    for user in users:
        print(user)
    # 레코드는 갯수 알아오기 : count
    # print(db.session.query(User).count())
    # 기본키 번호을 이용해서 가져오기 : id=3
    # print(db.session.query(User).get(3))
    # 하나만 가져오기
    # print(db.session.query(User).first())
    # 전체
    # print(db.session.query(User).all())   # User.query.all() 같은 결과...

    # db에 Insert 하기...(데이터 추가)
    # user = User(username="사용자명", email="flaskEx14@example.com", password="password")
    # db.session.add(user)  # sql을 실행
    # db.session.commit()  # db에 적용.(**)
    # db.session.add_all()

    # db에 데이터 수정하기 (update)
    # # 1) 데이터베이스에서 수정하려는 레코드를 불러옴.
    # user = db.session.query(User).filter_by(id=2).first()
    # # 2) 수정 작업
    # user.username = "사용자이름수정"
    # user.email = "flaskEx2-modify@example.com"
    # user.password = "비밀번호2"
    # # 3) 저장 및 적용
    # db.session.add(user)  # 수정 내용을 추가...
    # db.session.commit()

    # # 삭제 (delete)
    # # 1) 삭제할 데이터를 불러온다. 그리고, 삭제
    # user = db.session.query(User).filter_by(id=4).delete()
    # # 2) 적용
    # db.session.commit()
    # print(user)  # 성공시 1, 실패시 0

    return "콘솔에서 확인해 주세요."
