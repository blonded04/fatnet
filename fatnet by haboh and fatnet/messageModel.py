from db import DB

db = DB()


class MessageModel:
    def __init__(self, connection):  # connecting to db
        self.connection = connection

    def init_table(self):  # create table if not exists
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
            str(sender_id), str(recipient_id),
            message))  # when send message, only sender_id, recipient_id and message required
        cursor.close()
        self.connection.commit()

    def get_all_between_pair(self, sender_id, recipient_id):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM messages WHERE sender_id = ? AND recipient_id = ? OR sender_id = ? AND recipient_id = ?",
            (str(sender_id), str(recipient_id), str(recipient_id), str(
                sender_id)))  # getting all messages between two users, currently unused
        rows = cursor.fetchall()
        return rows

    def get_all(self, sender_id):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM messages WHERE sender_id = ? OR recipient_id = ?",
            (str(sender_id), str(sender_id))
        )  # getting all messages for 1 user
        rows = cursor.fetchall()
        return rows

    def get_table(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM messages")
        rows = cursor.fetchall()
        return rows  # getting all db
