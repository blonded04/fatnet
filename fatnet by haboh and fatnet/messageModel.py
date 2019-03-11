import hashlib
import sqlite3
from db import DB
from re import search
import random
from users_model import UsersModel
from db import DB

db = DB()


class MessageModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages 
                                (
                                 message_number INTEGER PRIMARY KEY AUTOINCREMENT,
                                 sender_id INTEGER,
                                 recipient_id INTEGER,
                                 message VARCHAR(10000)
                                 )''')
        cursor.close()
        self.connection.commit()

    def send(self, sender_id, recipient_id, message):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO messages 
                          (sender_id, recipient_id,  message) 
                          VALUES (?,?,?)''', (
            str(sender_id), str(recipient_id), message))
        cursor.close()
        self.connection.commit()

    def get_all_between_pair(self, sender_id, recipient_id):  # опять мак
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM messages WHERE sender_id = ? AND recipient_id = ? OR sender_id = ? AND recipient_id = ?",
            (str(sender_id), str(recipient_id), str(recipient_id), str(
                sender_id)))  # тут я не уверен, сработает ли ? AND ?, вдруг там можно .format делать только когда (?,?)
        rows = cursor.fetchall()
        return rows

    def get_all(self, sender_id):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM messages WHERE sender_id = ? OR recipient_id = ?",
            (str(sender_id), str(sender_id))
        )
        rows = cursor.fetchall()
        return rows

    def get_table(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM messages")
        rows = cursor.fetchall()
        return rows


