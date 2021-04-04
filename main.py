from datetime import timedelta

from flask import Flask, render_template, redirect, make_response, session, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api

from data import db_session
from data.groups import Group
from data.users import User
from forms.user import LoginForm
from data.lessons import Lessons
from keys.key import SECRET_KEY

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(
    days=365
)
app.config['JSON_AS_ASCII'] = False
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/')
def index():

    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        if current_user.type == 1:  # для преподов
            lessons = db_sess.query(Lessons).filter(Lessons.teacher_id == current_user.id).all()
            # print(lessons)
            return render_template('index_teacher.html', title='Главная', lessons=lessons)
        elif current_user.type == 2:    # для студента
            return render_template('index_student.html', title='Главная', lessons=lessons)
        elif current_user.type == 2:    # для админа
            lessons = db_sess.query(Lessons).all()
            return render_template('index_admin.html', title='Главная', lessons=lessons)
    return redirect('/login')

def main():
    db_session.global_init('db/main.db')
    # app.register_blueprint(jobs_api.blueprint)
    app.run(debug=True)


if __name__ == '__main__':
    main()
