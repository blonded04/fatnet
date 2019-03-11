# fatnet
## fatnet social network v0.1
At the moment this version supports only registration, login, posting on your /user/<int:user_id>/ page, getting your message list via /messages/ and sending messages via /message/<int:user_id>/.
###### Follow this repo to get informed about new updates! We will update it regularly.
### Let's take a look at its current functions:
#### 1. Registration window
![alt text](https://pp.userapi.com/c855228/v855228650/41b/PheKDxiPRpY.jpg) <br />
Here you should register an account for you, it will add your account to sqlite .db file, after you write your login, password and click on "Зарегистрироваться" button.
#### 2. Login window
![alt text](https://pp.userapi.com/c855228/v855228650/438/-B1tnkNZuTY.jpg) <br />
After registration you should login to an existing account. I will log into my account by clicking on "Войти".
#### 3. News feed
![alt text](https://pp.userapi.com/c855228/v855228650/44c/LBUdSs7Zung.jpg) <br />
After logging in you will see the news you have posted before this session, also you can post a new blog by clicking on a plus button or you can check all the messages you've got and you've sent by clicking on bubble.
#### 4. News feed of another user
![alt text](https://pp.userapi.com/c855228/v855228650/467/rUckZA9RRZg.jpg) <br />
You can also get to an another user's page via /user/<int:user_id> and you can read his posts. But you also can send him a message by clicking "Написать сообщение".
#### 5. Writing a message to another user
![alt text](https://pp.userapi.com/c855228/v855228650/484/zs-tPK48-40.jpg) <br />
You can write a message into a lineEdit and send it to a user by clicking "Отправить".
#### 6. Reading your messages
![alt text](https://pp.userapi.com/c855228/v855228650/48e/PGb-7SRg77k.jpg) <br />
You can also read the messages you've sent and you've got.
##### That's all that fatnet can do at the moment.
