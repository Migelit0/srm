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
from forms.user import LoginForm, RegisterForm
from keys.key import SECRET_KEY

# db_session.global_init('db/main.db')
# db_sess = db_session.create_session()
# print(db_sess.query(Payment).all())
