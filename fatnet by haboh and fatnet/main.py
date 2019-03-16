import os
from hashlib import md5

from flask import Flask, redirect, render_template, session

from add_news import AddNewsForm
from db import DB
from login_form import LoginForm
from messageModel import MessageModel
from news_model import NewsModel
from pos_news_form import PostForm
from registration_form import RegistrationForm
from send_form import MessageSendForm
from subsribe_model import SubscribeModel
from users_model import UsersModel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'admin'
db = DB()
NewsModel(db.get_connection()).init_table()
UsersModel(db.get_connection()).init_table()
MessageModel(db.get_connection()).init_table()
SubscribeModel(db.get_connection()).init_table()


@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/<error>', methods=['GET', 'POST'])
def login(error=None):
    form = LoginForm()
    if form.validate_on_submit():  # checking if a login form fields are all valid
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(user_name, str(md5(bytes(password,
                                                            encoding='utf-8')).hexdigest()))  # checking if a user with login user_name and password hash md5(password)
        if exists[0]:
            session['username'] = user_name
            session['user_id'] = exists[1]
        else:
            return redirect(
                '/login/notexist')  # if password and login are invalid redirect to /login/
        return redirect("/index")
    return render_template('login.html', title='Авторизация', form=form,
                           error=error)


@app.route('/logout')
def logout():
    session.pop('username', 0)  # deleting user from session on logout
    session.pop('user_id', 0)
    return redirect('/login')


@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
@app.route('/feed', methods=["GET", "POST"])
def index():
    if 'username' not in session:  # if you are not loginned you should login
        return redirect('/login')
    form = PostForm()
    if form.validate_on_submit():  # if news_title is not empty
        title = form.title.data
        content = form.content.data
        nm = NewsModel(db.get_connection())
        nm.insert(title, content, session['user_id'])
        return redirect("/index")
    news = NewsModel(db.get_connection()).get_all(
        session['user_id'])  # add note to news db
    return render_template('index.html', username=session['username'],
                           # update page because of the new note added
                           news=reversed(news),
                           form=form)


@app.route('/user/<int:user_id>')
def get_user_page(user_id):
    users = UsersModel(db.get_connection())
    if users.exists_only_by_id(user_id):
        name = users.get(user_id)[1]
        subscribes = SubscribeModel(db.get_connection())
        news = NewsModel(db.get_connection()).get_all(user_id)
        return render_template('view_page.html', news=reversed(news),
                               current_user_id=user_id,
                               user_name=name,
                               user_photo="/static/avas/" + str(
                                   user_id) + ".jpg",
                               subscribed=subscribes.check_subscription(
                                   session['user_id'],
                                   user_id))  # return user template if user exists
    return "Sorry. User not found."  # if you go on /user/something_not_in_db you will see page with text "Sorry. User not found."


@app.route('/subscribe/<int:user_id>')
def subscribe(user_id):
    subscribes = SubscribeModel(db.get_connection())
    subscribes.insert(session['user_id'],
                      user_id)  # when you subscribe to smb db requires only your db and db of the user you are being subbed
    return redirect('/index')


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if 'username' not in session:  # if you try to get to /add_news without logging in you will be redirected to login page
        return redirect('/login')
    form = AddNewsForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        nm = NewsModel(db.get_connection())
        nm.insert(title, content, session['user_id'])
        return redirect("/index")
    return render_template('add_news.html', title='Добавление новости',
                           form=form,
                           username=session[
                               'username'])  # get all news if something/nothing changed


@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    if 'username' not in session:
        return redirect(
            '/login')  # if user is not logged in, user will get redirected to /login
    nm = NewsModel(db.get_connection())
    nm.delete(news_id)
    return redirect("/index")


@app.route('/messages')
def get_messages():
    message_model = MessageModel(db.get_connection())
    users_model = UsersModel(db.get_connection())
    user_id_now = session['user_id']
    messages = message_model.get_all(
        user_id_now)  # message db has get_all method that returns all the users messages
    news_messages_list = []
    for message in messages:
        user_sender_name = users_model.get(message[1])[1]
        user_getter_name = users_model.get(message[2])[1]
        text = message[3]
        news_messages_list.append(
            (user_sender_name, user_getter_name, text, message[1], message[2])
        )
    news_messages_list.reverse()  # reverse list because newer messages should be upper than older messages
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
        messageModel.send(user_id_now, user_id,
                          message)  # add to message db sender id, recipient id and message(currently unencrypted)
        return redirect('/messages')
    return render_template('send_message.html', form=form, username=username)


@app.route('/registration', methods=["GET", "POST"])
@app.route('/registration/<er>', methods=["GET", "POST"])
def registration(er=None):
    form = RegistrationForm()
    if form.validate_on_submit():  # if password, login, and photo is not empty
        users = UsersModel(db.get_connection())
        if users.exists_only_by_name(form.username.data):
            return redirect(
                '/registration/exists')  # if user is already in db you should do reregistration
        else:
            users.insert(form.username.data, str(md5(bytes(form.password.data,
                                                           encoding='utf-8')).hexdigest()))  # add to db hash of the password for better encryption
            form.fileName.data.save(
                os.path.join(os.path.join('static', 'avas'),
                             str(users.get_table_size()) + ".jpg"))
            return redirect('/login')
    return render_template('registration.html', form=form, error=er)


@app.route('/subscriptions')
def subscriptions():
    subscribes = SubscribeModel(db.get_connection())
    user_subscriptions = subscribes.get_all(session['user_id'])
    user_model = UsersModel(db.get_connection())
    news = NewsModel(db.get_connection())
    for_post = []
    for _, user in user_subscriptions:
        for_post.extend([list(i) + [user_model.get(user)[1]] for i in
                         reversed(news.get_all(user))])
    return render_template('subscriptions.html', news=for_post)


@app.route('/users')
def users():
    users = UsersModel(db.get_connection())
    return render_template('users.html',
                           users=users.get_all())  # users db has get_all method to get list of all the users


if __name__ == '__main__':
    app.run(port=8080,
            host='127.0.0.1')  # using 127.0.0.1:8080 to run server on it
