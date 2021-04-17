import argparse
from datetime import datetime, timedelta

from flask import Flask, render_template, redirect, make_response, session, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api

from data import db_session
from data.attendance import Attendance
from data.lessons import Lessons
from data.payment import Payment
from data.users import User
from forms.attendance import AttendanceForm
from forms.payment import AddPaymentForm
from forms.user import LoginForm, RegisterForm
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


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    if current_user.is_authenticated and current_user.type != 3:
        return abort(404)

    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        type = request.form.get('type')
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            login=form.login.data,
            type=type
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


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


@app.route('/lesson/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
def lesson_attendance(lesson_id):  # TODO: ДОДЕЛАТЬ ФОРМУ АТО НЕ РАБОТАЕТ ЫЫЫЫЫ
    db_sess = db_session.create_session()
    if current_user.type in (1, 3):
        lesson = db_sess.query(Lessons).filter(Lessons.id == lesson_id).first()
        attendance = db_sess.query(Attendance).filter(Attendance.lesson_id == lesson_id).all()

        # attendance.sort(key=lambda x: int(db_sess.query(Lessons).filter(Lessons.id == x.lesson_id).first().date[0]))
        # print([db_sess.query(Lessons).filter(Lessons.id == i.lesson_id).first().date for i in attendance])

        attendance.sort(key=lambda x: x.lesson_number)

        data = [[]]
        prev = attendance[0].lesson_number
        for elem in attendance:
            if elem.lesson_number != prev:
                prev = elem.lesson_number
                data.append([])
            # for i in elem:
            #     data[-1]
            data[-1].append(elem)

        data = tuple(zip(*data[::-1]))

        # for row in data:
        #     print(*[i.student_id for i in row])

        students = []
        for elem in data:
            user = db_sess.query(User).filter(elem[0].student_id == User.id).first()
            # students.append(user.name + ' ' + user.surname)
            students.append(user)
        # print(students)

        today = datetime.now()
        first = datetime(today.year, 1, int(lesson.date[:1]))
        dtime = timedelta(days=7)
        dates = [(str((first + dtime * j).date().day) + '.' + str((first + dtime * j).date().month)) for j in
                 range(max([len(i) for i in data]) + 1)]

        form = AttendanceForm()
        for _ in range(len(attendance)):
            form.all.append_entry()

        if form.validate_on_submit():
            print(form.all.data)
            return redirect('/')

        return render_template('attendance_table.html', data=data, students=students, dates=dates, form=form)
    elif current_user.type == 2:
        return abort(404)
    # elif current_user.type == 3:
    #     attendance = db_sess.query(Lessons).filter(Lessons.id == lesson_id).all()
    #     return render_template('attendance_table.html', attendance=attendance)


@app.route('/lesson/pay/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
def payment(lesson_id):
    if current_user.type != 3:
        return abort(404)

    if current_user.type == 3:

        db_sess = db_session.create_session()
        data = db_sess.query(Payment).filter(Payment.lesson_id == lesson_id).all()
        if not data:
            # TODO: ЗДЕСЬ НУЖНО СОЗДАТЬ ОПЛАТУ ДЛЯ УЧЕНИКОВ
            return abort(404)

        lesson = db_sess.query(Lessons).filter(Lessons.id == lesson_id).first()
        data.sort(key=lambda x: x.student_id)

        payment = [[]]
        prev = data[0].student_id
        for elem in data:
            if elem.student_id != prev:
                prev = elem.student_id
                payment.append([])
            payment[-1].append(elem)
        # print(payment)
        # data = tuple(zip(*payment[::-1]))
        data = payment.copy()

        # for row in data:
        #     print(*row)

        students = []
        for elem in data:
            user = db_sess.query(User).filter(elem[0].student_id == User.id).first()
            students.append(user)

        today = datetime.now()
        first = datetime(today.year, 1, int(lesson.date[:1]))
        dtime = timedelta(days=7)
        dates = [(str((first + dtime * j).date().day) + '.' + str((first + dtime * j).date().month))
                 for j in range(max([len(i) for i in payment]))]

        # print(students)

        return render_template('payment_table.html', data=data, dates=dates, students=students, lesson_id=lesson_id)


@app.route('/lesson/pay/add/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
def add_payment(lesson_id):  # TODO: НУ ЭТО ТОЖЕ ДОДЕЛАТЬ
    if current_user.type != 3:
        return abort(404)
    form = AddPaymentForm()
    if form.validate_on_submit():
        if not form.student_id.data.isdigit() or not form.days_number.isdigit():
            return render_template('payment_add.html', title='Оплата', form=form, message='Ошибка в формате данных')
        db_sess = db_session.create_session()
        student_id = request.form.get('student_id')
        payment = db_sess.query(Payment).filter(Payment.student_id == student_id, Payment.is_payed == 0).all()
        payment.sort(key=lambda x: x.lesson_number)
        # TODO: ДОДЕЛАТЬ ДОБАВЛЕНИЕ ПЛАТЕЖЕЙ И КРУТО КОРОЧЕ ПУСТЬ БУДЕТ БЛИНА
    return render_template('payment_add.html', title='Оплата', form=form)


@app.route('/')
def index():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        if current_user.type == 1:  # для преподов
            today = datetime.now().weekday()
            lessons = db_sess.query(Lessons).filter(Lessons.teacher_id == current_user.id,
                                                    Lessons.date.like(f'{today}%')).all()
            # print(lessons)
            return render_template('index_teacher.html', title='Главная', lessons=lessons)
        elif current_user.type == 2:  # для студента
            return render_template('index_student.html', title='Главная', lessons=lessons)
        elif current_user.type == 3:  # для админа
            lessons = db_sess.query(Lessons).all()
            return render_template('index_admin.html', title='Главная', lessons=lessons)
    return redirect('/login')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000)
    parser.add_argument('--host', type=str, default='127.0.0.1')
    args = parser.parse_args()
    port, host = args.port, args.host

    db_session.global_init('db/main.db')
    app.run(debug=True, port=port, host=host)


if __name__ == '__main__':
    main()
