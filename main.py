import argparse
import re
from datetime import datetime, timedelta

from flask import Flask, render_template, redirect, make_response, session, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api

from data import db_session
from data.attendance import Attendance
from data.groups import Group
from data.lessons import Lessons
from data.payment import Payment
from data.users import User
from for_db import add_payment, add_attendances
from forms.attendance import AttendanceForm
from forms.lesson import AddNewLessonForm
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
                               form=form, title='Авторизация')
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
        if current_user.type == 1:  # Проверка принадлежит ли группа учителю
            groups = db_sess.query(Group.id).filter(Group.teacher_id == current_user.id).all
            if lesson_id not in groups:
                return abort(404)  # выгоняем со странички, если нет

        lesson = db_sess.query(Lessons).filter(Lessons.id == lesson_id).first()
        attendance = db_sess.query(Attendance).filter(Attendance.lesson_id == lesson_id).all()
        if not attendance:
            add_attendances(lesson_id)
        attendance = db_sess.query(Attendance).filter(Attendance.lesson_id == lesson_id).all()

        attendance.sort(key=lambda x: x.lesson_number)

        data = [[]]
        prev = attendance[0].lesson_number
        for elem in attendance:
            if elem.lesson_number != prev:
                prev = elem.lesson_number
                data.append([])
            data[-1].append(elem)

        data = tuple(zip(*data[::-1]))

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

        if form.validate_on_submit():  # обработка формы (получение даг=ныых)
            # print(form.all.data)
            new_id = request.form.get('student_id')
            if new_id:
                student = db_sess.query(User).filter(User.id == new_id).first()
                if not student:
                    return render_template('attendance_table.html', data=data, students=students, dates=dates,
                                           form=form,
                                           title='Посещаемость', message='Такого пользователя не существует')
            return redirect('/')

        # adder_form = AddPaymentForm()
        # if adder_form.validate_on_submit():
        #     new_id = request.form.get('student_id')
        #     student = db_sess.query(User).filter(User.id == new_id).first()
        #     if not student:
        #         return render_template('attendance_table.html', data=data, students=students, dates=dates, form=form,
        #                                title='Посещаемость', message='Такого пользователя не существует')
        #     db_sess.add()

        return render_template('attendance_table.html', data=data, students=students, dates=dates, form=form,
                               title='Посещаемость')
    elif current_user.type == 2:
        return abort(404)


@app.route('/lesson/pay/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
def payment(lesson_id):
    if current_user.type != 3:
        return abort(404)

    if current_user.type == 3:

        db_sess = db_session.create_session()
        data = db_sess.query(Payment).filter(Payment.lesson_id == lesson_id).all()
        if not data:
            add_payment(lesson_id)
            data = db_sess.query(Payment).filter(Payment.lesson_id == lesson_id).all()

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

        students = []
        for elem in data:
            user = db_sess.query(User).filter(elem[0].student_id == User.id).first()
            students.append(user)

        today = datetime.now()
        first = datetime(today.year, 1, int(lesson.date[:1]))
        dtime = timedelta(days=7)
        dates = [(str((first + dtime * j).date().day) + '.' + str((first + dtime * j).date().month))
                 for j in range(max([len(i) for i in payment]))]

        return render_template('payment_table.html', data=data, dates=dates, students=students, lesson_id=lesson_id)


@app.route('/lesson/pay/add/<int:lesson_id>/<int:student_id>', methods=['GET', 'POST'])
@login_required
def payment_one_student(lesson_id, student_id):
    if current_user.type != 3:
        return abort(404)
    form = AddPaymentForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        days_number = int(request.form.get('days_number'))
        payment = db_sess.query(Payment).filter(Payment.student_id == student_id, Payment.is_payed == 0,
                                                Payment.lesson_id == lesson_id).all()
        payment.sort(key=lambda x: x.lesson_number)
        if len(payment) < days_number:
            for _ in range(days_number - len(payment)):  # Если нет платежей, то добавляем
                add_payment(lesson_id)
        payment = db_sess.query(Payment).filter(Payment.student_id == student_id, Payment.is_payed == 0,
                                                Payment.lesson_id == lesson_id).all()
        payment.sort(key=lambda x: x.lesson_number)
        for i in range(days_number):  # оплачиваем
            payment[i].is_payed = True
        db_sess.commit()

        # return redirect(f'/lesson/pay/{lesson_id}/{student_id}')
    db_sess = db_session.create_session()
    student = db_sess.query(User).filter(User.id == student_id).first()
    lesson = db_sess.query(Lessons).filter(Lessons.id == lesson_id).first()

    payment = db_sess.query(Payment).filter(Payment.student_id == student_id, Payment.lesson_id == lesson_id).all()
    payment.sort(key=lambda x: x.lesson_number)
    all_data = [[]]
    counter = 0
    for elem in payment:  # офигеть как лень нормально сделать простити
        if counter == 8:
            counter = 0
            all_data.append([])
        all_data[-1].append(elem)
        counter += 1

    today = datetime.now()
    first = datetime(today.year, 1, int(lesson.date[:1]))
    dtime = timedelta(days=7)
    sth = [(str((first + dtime * j).date().day) + '.' + str((first + dtime * j).date().month)) for j in
           range(len(payment))]  # max([len(i) for i in all_data]))]

    dates = [[]]
    counter = 0
    for elem in sth:
        if counter == 8:
            counter = 0
            dates.append([])
        dates[-1].append(elem)
        counter += 1

    return render_template('payment_one_student.html',
                           title='Оплата', form=form, student=student, all_data=all_data,
                           dates=dates, length=len(all_data), lesson_id=lesson_id)


@app.route('/lesson/pay/add/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
def add_payment_page(lesson_id):
    if current_user.type != 3:
        return abort(404)
    form = AddPaymentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        student_id = int(request.form.get('student_id'))
        days_number = int(request.form.get('days_number'))
        payment = db_sess.query(Payment).filter(Payment.student_id == student_id, Payment.is_payed == 0).all()
        payment.sort(key=lambda x: x.lesson_number)
        if len(payment) < days_number:
            for _ in range(days_number - len(payment)):  # Если нет платежей, то добавляем
                add_payment(lesson_id)
        payment = db_sess.query(Payment).filter(Payment.student_id == student_id, Payment.is_payed == 0).all()
        payment.sort(key=lambda x: x.lesson_number)
        for i in range(days_number):  # оплачиваем
            payment[i].is_payed = True
        db_sess.commit()

        return redirect(f'/lesson/pay/{lesson_id}')
    return render_template('payment_add.html', title='Оплата', form=form, lesson_id=lesson_id)


@app.route('/add_lesson', methods=['GET', 'POST'])
@login_required
def add_lesson():
    if current_user.type != 3:
        return abort(404)
    form = AddNewLessonForm()
    if form.validate_on_submit():
        group_id = request.form.get('group_id')
        teacher_id = request.form.get('teacher_id')
        date = request.form.get('date')
        title = request.form.get('title')
        # \d\d:\d\d-\d{,2}
        db_sess = db_session.create_session()
        if re.match(r'\d\d:\d\d-\d', date).group(0) != date:  # РЕГУЛЯРКИ ААААА ШТО ВЫ СО МНОЙ ДЕЛАЕТЕ А
            print(re.match('\d\d:\d\d-\d', date).group(0))
            return render_template('add_lesson.html', form=form, title='Добавление занятия',
                                   message='Невереный формат даты')
        if not db_sess.query(User).filter(User.id == teacher_id, User.type == 2).first():
            return render_template('add_lesson.html', form=form, title='Добавление занятия',
                                   message='Учителя с таким ID не сущетсвует')
        new_lesson = Lessons(
            group_id=group_id,
            teacher_id=teacher_id,
            date=date,
            title=title
        )
        db_sess = db_session.create_session()
        db_sess.add(new_lesson)
        db_sess.commit()
        return redirect('/')
    return render_template('add_lesson.html', form=form, title='Добавление занятия')


@app.route('/ids')
@login_required
def show_ids():
    if current_user.type != 3:
        return abort(404)
    db_sess = db_session.create_session()
    students = db_sess.query(User).filter(User.type == 2).all()
    teachers = db_sess.query(User).filter(User.type == 1).all()
    admins = db_sess.query(User).filter(User.type == 3).all()
    return render_template('user_table.html', students=students, teachers=teachers, admins=admins,
                           title='Таблица пользователей')   # 49 63 -529    # -205 72 -519


@app.route('/')
def index():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        if current_user.type == 1:  # для преподов
            today = datetime.now().weekday()
            lessons = db_sess.query(Lessons).filter(Lessons.teacher_id == current_user.id,
                                                    Lessons.date.like(f'{today}%')).all()
            # print(lessons)
            # if not lessons:
            #     return render_template('error.html', title='Главная', message='У вас сегодня нет занятий')
            return render_template('index_teacher.html', title='Главная', lessons=lessons)
        elif current_user.type == 2:  # для студента
            try:
                return render_template('index_student.html', title='Главная', lessons=lessons)
            except Exception:
                return render_template('error.html', message='-_-', title='Главная')
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
