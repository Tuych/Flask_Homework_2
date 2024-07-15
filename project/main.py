from flask import Flask, g, render_template, request, flash
import sqlite3
import os
from DataBase import FDataBase

DEBUG = True
SECRET_KEY = '1Q2W3E4R5T66Y7U8I9Odeccc3sdjdbdehcc'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'edu.db')))


def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con


def create_table():
    db = connect_db()
    with app.open_resource('edu_db.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


menu = [
    {'name': 'Католог курсов', 'url': '/index'},
    {'name': 'Добавить курс', 'url': '/add_course'},
    {'name': 'Инвормация', 'url': '/info'}
]


@app.route('/')
@app.route('/index')
def index():
    con = get_db()
    dbase = FDataBase(con)
    information = dbase.get_course()

    return render_template('index.html', menu=menu, title='Католог курсов', info=information)


@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    con = get_db()
    dbase = FDataBase(con)

    if request.method == "POST":
        name = request.form['name']
        price = request.form['price']
        info = request.form['info']
        if len(name) >= 2 and len(info) >= 60:
            res = dbase.add_course(name, price, info)
            if not res:
                flash('Ошибка добавлиния группа ', category='error')

            else:
                flash('Группа добавлиния успешно', category='success')
        else:
            flash('Для правильного добавления данных имя группы должно содержать более 2 символов, а информация должна быть более 40 символов', category='error')

    return render_template('add_course.html', menu=menu, title='Добавить курс')


@app.route('/about/<int:course_id>')
def about(course_id):
    con = get_db()
    dbase = FDataBase(con)

    info = dbase.get_one_course(course_id)
    if info:
        return render_template('about.html', menu=menu, title='О курсе', info=info)
    else:
        return render_template('about.html', menu=menu, title='О курсе')


@app.route('/info')
def info():
    return render_template('info.html', menu=menu, title='Полная информация о курсе')


@app.errorhandler(404)
def page404(error):
    return render_template('page404.html', menu=menu, title='Странитца не найдень')


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == '__main__':
    app.run()
