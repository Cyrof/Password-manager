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
                    print('2')
                case '3':
                    print('3')
                case '4':
                    print('4')
                case '5':
                    print('5')
                case '6':
                    print('6')
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
            if service_name is None:
                try:
                    service_name = input("Enter name of service: ")
                    if service_name == "":
                        service_name = None
                except:
                    continue
            elif username is None:
                try:
                    username = input("Enter username for service (optional)[enter to continue]: ")
                except:
                    continue
            elif password is None:
                try:
                    password = getpass.getpass("Enter password for the service: ")
                    if password == "":
                        password = None
                except:
                    continue
            elif password is not None:
                try:
                    if self.ps_validation(mps=password):
                        break
                except:
                    continue
            else:
                break
        
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
            else:
                print(colored("X Password does not match X", 'red'))
                return False
    
    def display_service(self, **kwargs):
        """ display all service from database
        :param **kwargs: keyword arguments
        :return:
        """
        if kwargs["data"]:
            print(kwargs['data'])
                
    def update_ps(self):
        """ Update password data in database
        :param:
        :return:
        """
        self.display_service(data=self.__db.get_all_data())

    
        

if __name__ == "__main__":
    program = PS()
    program.run()