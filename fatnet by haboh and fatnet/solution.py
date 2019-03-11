from add_news import AddNewsForm
from db import DB
from flask import Flask, redirect, render_template, session
from login_form import LoginForm
from news_model import NewsModel
from users_model import UsersModel
from registration_form import RegistrationForm
from messageModel import MessageModel
from send_form import MessageSendForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = DB()
NewsModel(db.get_connection()).init_table()
UsersModel(db.get_connection()).init_table()
MessageModel(db.get_connection()).init_table()


# http://127.0.0.1:8080/login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(user_name, password)
        if exists[0]:
            session['username'] = user_name
            session['user_id'] = exists[1]
        return redirect("/index")
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/login')
    news = NewsModel(db.get_connection()).get_all(session['user_id'])
    return render_template('index.html', username=session['username'], news=news)


@app.route('/user/<int:user_id>')
def get_user_page(user_id):
    users = UsersModel(db.get_connection())
    if users.exists_only_by_id(user_id):
        news = NewsModel(db.get_connection()).get_all(user_id)
        return render_template('view_page.html', news=news, current_user_id=user_id)
    return "Sorry. User not found."


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if 'username' not in session:
        return redirect('/login')
    form = AddNewsForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        nm = NewsModel(db.get_connection())
        nm.insert(title, content, session['user_id'])
        return redirect("/index")
    return render_template('add_news.html', title='Добавление новости', form=form, username=session['username'])


@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(db.get_connection())
    nm.delete(news_id)
    return redirect("/index")


@app.route('/messages')
def get_messages():
    message_model = MessageModel(db.get_connection())
    users_model = UsersModel(db.get_connection())
    user_id_now = session['user_id']
    messages = message_model.get_all(user_id_now)
    news_messages_list = []
    for message in messages:
        user_sender_name = users_model.get(message[1])[1]
        user_getter_name = users_model.get(message[2])[1]
        text = message[3]
        news_messages_list.append(
            (user_sender_name, user_getter_name, text, message[1], message[2])
        )
    news_messages_list.reverse()
    return render_template('messages_page.html', messages=news_messages_list)


@app.route('/message/<int:user_id>', methods=["GET", "POST"])
def send_message(user_id):
    usersmodel = UsersModel(db.get_connection())
    messageModel = MessageModel(db.get_connection())
    username = usersmodel.get(user_id)[1]
    form = MessageSendForm()
    user_id_now = session['user_id']
    if form.validate_on_submit():
        message = form.content.data
        messageModel.send(user_id_now, user_id, message)
        return redirect('/messages')
    return render_template('send_message.html', form=form, username=username)


@app.route('/registration', methods=["GET", "POST"])
@app.route('/registration/<error>', methods=["GET", "POST"])
def registration(error=False):
    form = RegistrationForm()
    if form.validate_on_submit():
        users = UsersModel(db.get_connection())
        if users.exists_only_by_name(form.username.data):
            return redirect('/registration/exists')
        else:
            users.insert(form.username.data, form.password.data)
            return redirect('/login')
    return render_template('registration.html', form=form, error=error)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
