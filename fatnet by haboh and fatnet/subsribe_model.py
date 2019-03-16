class SubscribeModel:
    def __init__(self, connection):  # connecting to db
        self.connection = connection

    def init_table(self):  # create table if not exists
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS subscribes 
                                (user_subscriber_id INTEGER,
                                user_poster_id INTEGER
                                 )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_subscriber, user_poster):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO subscribes 
                          (user_subscriber_id, user_poster_id) 
                          VALUES (?,?)''', (str(user_subscriber), str(
            user_poster)))  # when sub to smb, only your id and user you want to sub id needed
        cursor.close()
        self.connection.commit()

    def check_subscription(self, user_subscriber, user_poster):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM subscribes WHERE user_subscriber_id = ? AND user_poster_id = ?",
            (str(user_subscriber),
             str(user_poster)))  # check if you are a sub of a user
        row = cursor.fetchone()
        return bool(row)

    def get_all(self, user_subscriber=None):
        cursor = self.connection.cursor()
        if user_subscriber:
            cursor.execute(
                "SELECT * FROM subscribes WHERE user_subscriber_id = ?",
                (str(
                    user_subscriber),))  # get all the users on who user you need is subbed
        else:
            cursor.execute("SELECT * FROM subscribes")
        rows = cursor.fetchall()
        return rows

    def delete(self, user_subscriber, user_poster):
        cursor = self.connection.cursor()
        cursor.execute(
            '''DELETE FROM subscribes WHERE user_subscriber_id = ? AND user_poster_id = ?''',
            (str(user_subscriber), str(user_poster)))  # unsubscribe
        cursor.close()
        self.connection.commit()
