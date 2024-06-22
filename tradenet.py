import sqlite3


class TradeNet:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                platformKey TEXT NOT NULL,
                coins INTEGER NOT NULL DEFAULT 0
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY,
                user1_id INTEGER,
                user2_id INTEGER,
                amount INTEGER NOT NULL,
                FOREIGN KEY(user1_id) REFERENCES users(id),
                FOREIGN KEY(user2_id) REFERENCES users(id)
            )
        """)
        self.conn.commit()

    def chec

    def get_user(self, platformKey):
        self.cursor.execute("SELECT id, name, coins FROM users WHERE platformKey = ?", (platformKey,))
        return self.cursor.fetchone()

    def add_user(self, name, platformKey):
        self.cursor.execute("INSERT INTO users (name, platformKey) VALUES (?, ?)", (name, platformKey))
        self.conn.commit()

    # արժույթի թողարկում
    def release_money(self, user, amount):
        self.cursor.execute("UPDATE users SET coins = coins + ? WHERE id = ?", (amount, user))
        self.conn.commit()

    def make_trade(self, user1_id, user2_id, amount):
        self.cursor.execute("SELECT coins FROM users WHERE id = ?", (user1_id,))
        user1_coins = self.cursor.fetchone()[0]
        if user1_coins >= amount:
            self.cursor.execute("begin")
            self.cursor.execute("UPDATE users SET coins = coins - ? WHERE id = ?", (amount, user1_id))
            self.cursor.execute("UPDATE users SET coins = coins + ? WHERE id = ?", (amount, user2_id))
            self.cursor.execute("INSERT INTO trades (user1_id, user2_id, amount) VALUES (?, ?, ?)", (user1_id, user2_id, amount))
            self.cursor.execute("commit")
            self.conn.commit()
        else:
            self.conn.execute("rollback")
            print("User1 does not have enough coins for this trade.")

    def close(self):
        self.conn.close()