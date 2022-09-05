import sqlite3

# the create table query for sqlite
create_table_sql = """ CREATE TABLE IF NOT EXISTS password_manager (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name VARCHAR NOT NULL,
    username VARCHAR,
    password VARCHAR NOT NULL
    );"""

# Database class 
class DB:
    """ Instance function to run when class is called
    :var self.__path: path of db
    :self.__conn: create connection to db
    :if else: check if self.__conn exist then create table
    """
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
    
    def delete_all(self):
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
            print("All items deleted")
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
    
    def get_all_data(self):
        """ Get all data from db
        :param:
        :return data as a 2d list:
        """
        try:
            sql = 'SELECT * FROM password_manager'
            cur = self.__conn.cursor()
            cur.execute(sql)

            rows = cur.fetchall()

            data = [[d for d in row] for row in rows]
            return data
        except Exception as e:
            print(e)
    
    def get_data_by_id(self, id):
        """ Get date by id
        :param id: id of data 
        :return data:
        """
        try:
            get_by_id = """ SELECT * FROM password_manager WHERE id=?"""

            cur = self.__conn.cursor()
            cur.execute(get_by_id, (id,))
            data = cur.fetchall()
            return data
        except sqlite3.Error as e:
            print("Failed to read data from table", e)
            return None
    
if __name__ == "__main__":
    db = DB()
    # db.delete_table()
    # db.insertVarIntoTable("youtube", "cyrof", "ps")
    # db.delete_all()