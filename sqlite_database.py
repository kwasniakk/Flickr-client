import sqlite3
from sqlite3 import Error
from errors import IncorrectFormat
from utils import reconstruct_from_bytes, evaluate_img_red

class ImageDatabase:

    def __init__(self, db_file):
        self.conn = self.create_connection(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def insert(self, data_row):
        url, image = data_row
        with self.conn:
            self.cursor.execute("INSERT OR IGNORE INTO images VALUES (?, ?)", (url ,image))

    def select(self, mode = "all", image_url = None):
        """[Select data from database. If mode is not "all" then select data by url]

        Args:
            mode (str): [searching mode]. Defaults to "all".
            image_url ([str], optional): [description]. Defaults to None.

        Returns:
            [list]: [selected data]
        """
        if mode == "all":
            query = "SELECT * FROM images"
            self.cursor.execute(query)
        else:
            query =  "SELECT * FROM images WHERE id=:id"
            self.cursor.execute(query, {"url", image_url})

        return self.cursor.fetchall()

    def find_the_most_red_colored(self):
        """[Search for the most colored image in the database]

        Returns:
            [str]: [URL to most red colored image]
        """
        data = self.select(mode = "all")
        max_red = 0
        best_img = None
        for row in data:
            url = row[0]
            img = reconstruct_from_bytes(row[1])
            red_value = evaluate_img_red(img)
            if (red_value > max_red):
                max_red = red_value
                best_img = url
        return best_img

    def create_connection(self, db_file):
        """[Connect with SQLite database]

        Args:
            db_file ([str]): [path to database]

        Raises:
            IncorrectFormat: [Raise this error if database format is not .db]

        Returns:
            [Connection object]: [Connection to the database]
        """
        conn = None
        if not db_file.endswith(".db"):
            raise IncorrectFormat(db_file)
        else:
            try:
                conn = sqlite3.connect(db_file)
                print("Connection with Database estabilished")
            except Error:
                print(Error)
            finally:
                return conn

    def create_table(self):
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS images(
                        url TEXT PRIMARY KEY,
                        image BLOB
                )""")
