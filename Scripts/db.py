import sqlite3

create_table_sql = """ CREATE TABLE IF NOT EXISTS password_manager (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name VARCHAR NOT NULL,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL
    );"""

class DB:
    def __init__(self):
        self.__path = r"password.db"
        self.__conn = self.create_connection(self.__path)
        if self.__conn is not None:
            self.create_table(self.__conn, create_table_sql)
        else:
            print("Error! cannot create a database connection.")

    def create_connection(self, db_path):
        """ create a database connection to the SQLite database
            specified by the db_path
        :param db_path: database file path 
        :return: Connection object or None 
        """

        conn = None
        try:
            conn = sqlite3.connect(db_path)
            return conn
        except Exception as e:
            print(e)
        
        return conn
    def create_table(self, conn, create_sql_table):
        """ create a table from the create_sql_table param
        :param conn: Connection object
        :param create_sql_table: CREATE TABLE statement
        :return:
        """

        try:
            cur = conn.cursor()
            cur.execute(create_sql_table)
        except Exception as e:
            print(e)
    
    def insertVarIntoTable(self, serviceName, username, password):
        """ Insert var into table
        :param serviceName: name of service inputted
        :param password: encrypted password
        :return:
        """
        try:
            cur = self.__conn.cursor()

            insert_query = """ INSERT INTO password_manager (
                service_name, username, password) VALUES (?, ?, ?);"""
            
            data_tuple = (serviceName, username, password)
            cur.execute(insert_query, data_tuple)
            self.__conn.commit()
            print("Data added") 

        except Exception as e:
            print(e)
    
    def delete_all_task(self):
        """
        Delete all tasks in the tasks table
        :return:
        """
        try:
            sql = 'DELETE FROM password_manager'
            sql2 = 'UPDATE sqlite_sequence SET SEQ=0 WHERE NAME="password_manager";'
            cur = self.__conn.cursor()
            cur.execute(sql)
            cur.execute(sql2)
            self.__conn.commit()
            print("All Tasks deleted")
        except Exception as e:
            print(e)

    def delete_table(self):
        """ Delete table from db file
        :return:
        """
        try:
            sql = 'DROP TABLE password_manager;'
            cur = self.__conn.cursor()
            cur.execute(sql)
            self.__conn.commit()
            print("Table deleted")
        except Exception as e:
            print(e)
    
if __name__ == "__main__":
    db = DB()
    # db.delete_table()
    db.insertVarIntoTable("youtube", "cyrof", "ps")