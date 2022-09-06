from Scripts.crypto import Crypt
from Scripts.db import DB
import getpass
from pyfiglet import Figlet
from termcolor import colored
from prettytable import PrettyTable

# PS class (basically the menu class)
class PS:

    def __init__(self):
        """ Instance function of the PS class 
        :param:
        :return:
        """
        self.__crypto = Crypt()
        self.__db = DB()
        self.__figlet = Figlet(font='standard')

        

    def run(self, *argv, **kwargs):
        """ run the password manger program 
        :param *argv: non-keyword arguments
        :param **kwargs: keyword arguments
        :return:
        """
        if not self.__crypto.does_master_ps_exist():
            self.create_master_ps_menu()
        else:
            self.validate_master_ps()
    
    def welcome(self):
        """ function to print out welcome 
        :param:
        :return:
        """
        print("\n")
        print(colored(self.__figlet.renderText("Welcome to PSV!"), 'green'))
        print("\n")
    
    def create_master_ps_menu(self):
        """ menu for create master password
        :param:
        :return:
        """
        self.welcome()
        try:
            while True:
                print(colored("To start, you will have to create a master password. Be careful not to lose it as it is unrecoverable.", 'green'))
                m_ps = getpass.getpass(colored("Create a master password for the program:", 'white'))
                verify_m_ps = getpass.getpass(colored("Verify your master password:", 'white'))
                if m_ps == verify_m_ps:
                    self.create_master_ps(mps=m_ps)
                    tick = u'\u2713'
                    print(colored(f"{tick} Thank you! Restart the program and enter your master password to begin.", 'green'))
                    break
                else:
                    print(colored("X Password do not match. Please try agian X", 'red'))
                    continue
        except KeyboardInterrupt:
            pass

    def create_master_ps(self, **kwargs):
        """ Create master pass if not found 
        :param:
        :return:
        """
        if kwargs["mps"]:
            self.__crypto.generate_master_hash(kwargs["mps"]) 
            self.__crypto.generate_key()

    def validate_master_ps(self):
        """ validating master password 
        :param:
        :return:
        """
        self.welcome()
        try:
            while True:
                m_ps = getpass.getpass(colored("Enter Your Master Password:"))
                if self.__crypto.check_master_hash(m_ps):
                    tick = u'\u2713'
                    print(colored(f"{tick} Thank you! Choose an option below", 'green'))
                    break
                else:
                    print(colored("X Master password is incorrect X", 'red'))
                    continue
        except Exception as e:
            print(e)
        else:
            self.menu()

    def menu(self):
        """ Menu for the psv 
        :param:
        :return:
        """
        while True:
            print(colored("\n\t*Enter 'exit' at any point to exit.*\n", 'magenta'))
            print(colored("1) Add a password", 'cyan'))
            print(colored("2) Update a password", 'cyan'))
            print(colored("3) Retrieve a password", 'cyan'))
            print(colored("4) Delete a password", 'cyan'))
            print(colored("5) Erase all passwords", 'red'))
            print(colored("6) Delete all data including master password", 'red'))
            choice = input(colored("Enter a choice: ", 'white'))

            match choice:
                case '1':
                    self.add_ps()
                case '2':
                    self.update_ps_menu()
                case '3':
                    self.get_pass()
                case '4':
                    self.delete_pass()
                case '5':
                    self.delete_all_pass()
                case '6':
                    self.delete_all()
                case 'exit':
                    break
                case _:
                    print(colored("X Command not recognized X", 'red'))
    
        
    def add_ps(self):
        """ Add a password to the db 
        :param:
        :return:
        """
        service_name = None
        username = None
        password = None
        print("\n")
        while True:
            print(colored("\n\t*Enter 'exit' at any point to exit.*\n", 'magenta'))
            if service_name is None:
                try:
                    service_name = input("Enter name of service: ")
                    if service_name == "":
                        service_name = None
                    if service_name == "exit":
                        break
                except:
                    continue
            elif username is None:
                try:
                    username = input("Enter username for service (optional)[enter to continue]: ")
                    if username == "exit":
                        break
                except:
                    continue
            elif password is None:
                try:
                    password = getpass.getpass("Enter password for the service: ")
                    if password == "":
                        password = None
                    if password == "exit":
                        break
                except:
                    continue
            elif password is not None and password != "exit":
                try:
                    validation = self.ps_validation(mps=password)
                    if validation == True:
                        break
                    elif validation == "exit":
                        password = None
                        break
                except:
                    continue
            else:
                break
        
        if service_name is not None and password is not None and password != "exit":
            self.__db.insertVarIntoTable(serviceName=service_name, username=username, password=self.__crypto.encrypt(password))

    
    def ps_validation(self, **kwargs):
        """ Password validation for add password function
        :param **kwargs: keyword arguments
        :return bool: return bool if password validation is true
        """
        if kwargs["mps"] and kwargs is not None:
            verify_ps = getpass.getpass("Verify password: ")
            if kwargs['mps'] == verify_ps:
                print(colored("Thank you! The password is now saved into the vault.", 'green'))
                return True
            elif verify_ps == "exit":
                return verify_ps
            else:
                print(colored("X Password does not match X", 'red'))
                return False
    
    def display_all_service(self, **kwargs):
        """ display all service from database
        :param **kwargs: keyword arguments
        :return:
        """
        if kwargs["data"]:
            datas = kwargs["data"]
            datas = [data[:-1] for data in datas]
            p_table = PrettyTable()
            p_table.field_names = ["Id", "Service Name", "Username"]
            p_table.add_rows(datas)
            print("\n")
            print(p_table)
    
    def display_service(self, **kwargs):
        """ display service from database from id
        :param **kwargs: keyword arguments
        :return:
        """
        if kwargs['data']:
            datas = kwargs["data"]
            datas = list(datas[0])
            datas[-1] = self.__crypto.decrypt(datas[-1])
            p_table = PrettyTable()
            p_table.field_names = ["Id", "Service Name", "Username", "Password"]
            p_table.add_rows([datas])
            print(p_table)
    
    def check_db(self):
        """ Check database if there is any data
        :param:
        :return bool: return bool if data exist
        """
        datas = self.__db.get_all_data()
        if not datas:
            return False
        else:
            return True
                
    # update choice redo 
    def update_ps_menu(self):
        """ Update password menu
        :param:
        :return:
        """
        if self.check_db():
            while True:
                print(colored("\n\t*Enter 'exit' at any point to exit.*", 'magenta'))
                self.display_all_service(data=self.__db.get_all_data())
                try:
                    choice = input("Enter id of service name to update password: ")
                    if choice == "exit":
                        break
                    if choice.isdigit():
                        self.display_service(data=self.__db.get_data_by_id(int(choice)))
                        self.update_ps(data=self.__db.get_data_by_id(int(choice)))
                        break
                except:
                    continue
        else:
            print(colored("\nError no data in database", 'red'))
    def update_ps(self, **kwargs):
        """ Update password data from database
        :param kwargs: keyword arguments
        :return:
        """
        print("test")
        if kwargs['data']:
            datas = kwargs["data"]
            datas = list(datas[0])
            service_name = datas[1]
            username = datas[2]
            ps = datas[3]
        while True:
            print(colored("\n\t*Enter 'exit' at any point to exit.*", 'magenta'))
            print("1) Service Name")
            print("2) Username")
            print("3) Password")
            print("4) Confirm to update")
            try:
                choice = input("Enter a choice: ")
            except:
                print(colored("An error occured. Please try again", 'red'))
                continue
            
            match choice:
                case '1':
                    service_name = input("Enter Service Name to change: ")
                case '2':
                    username = input("Enter Username to change: ")
                case '3':
                    ps = input("Enter Password to change: ")
                    ps = self.__crypto.encrypt(ps)
                case '4':
                    datas = [datas[0], service_name, username, ps]
                    print(datas)
                    self.__db.update_data(data=datas)
                    break
                case 'exit':
                    break
                case _:
                    print(colored("X Command not recognized X", 'red'))


    def get_pass(self):
        """ Retrieve password 
        :param:
        :return:
        """
        if self.check_db():
            while True:
                    print(colored("\n\t*Enter 'exit' at any point to exit.*", 'magenta'))
                    self.display_all_service(data=self.__db.get_all_data())
                    try:
                        choice = input("Enter id of service name to get password: ")
                        if choice == "exit":
                            break
                        if choice.isdigit():
                            self.display_service(data=self.__db.get_data_by_id(int(choice)))
                            break
                    except:
                        continue
        else:
            print(colored("\nError no data in database", 'red'))
    
    def delete_pass(self):
        """ Delete password
        :param:
        :return:
        """
        if self.check_db():
            while True:
                print(colored("\n\t*Enter 'exit' at any point to exit.*", 'magenta'))
                self.display_all_service(data=self.__db.get_all_data())
                try:
                    choice = input("Enter id of service name to delete password: ")
                    if choice == "exit":
                        break
                    if choice.isdigit():
                        # create delete by id on db.py
                        # self.__db.delete_by_id(id=int(choice))
                        try:
                            self.__db.delete_by_id(id=int(choice))
                        except Exception as e:
                            print("An error has occured.", e)
                        break
                except:
                    continue
        else:
            print(colored("\nError no data in database", 'red'))
    
    def delete_all_pass(self):
        """ delete all data from db
        :param:
        :return:
        """
        if self.check_db():
            choice= input(colored("\nAre you sure you want to delete all password datas? [y/n]: ", 'red'))
            if choice.lower() == 'y':
                self.__db.delete_all()
            if choice.lower() == 'n':
                pass
        else:
            print(colored("\nError no data in database", 'red'))

        
    def delete_all(self):
        """ Delete all
        :param:
        :return:
        """
        choice = input(colored("\nAre you sure you want to delete all data including master password? [y/n]: ", 'red'))
        if choice.lower() == 'y':
            self.__db.delete_all()
            self.__crypto.clear_dotenv()
            print(colored("\nThank you for using our services. Goodbye", 'magenta'))
            exit()
        if choice.lower() == 'n':
            pass

if __name__ == "__main__":
    program = PS()
    program.run()