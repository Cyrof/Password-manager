from cryptography.fernet import Fernet
from dotenv import load_dotenv, find_dotenv, set_key, unset_key
import os
import hashlib

# cryptography class
class Crypt:

    """ Instance function to run when class called
    :self.checkenv: check if dotenv file exist if not create it 
    :var self.donenv_file: get the .env file from the same folder
    :load_dotenv(self.dotenv_file): load the dotenv file 
    """
    def __init__(self):
        self.check_env()
        self.__filepath = os.path.abspath("ps.env")
        load_dotenv(self.__filepath)
        

    def check_env(self):
        """ Create dotenv file is not exist
        :param:
        :return:
        """
        with open("ps.env", "a") as f:
            f.close()
    
    def does_key_exist(self):
        """ Check if key exist
        :param:
        :return bool: return bool if key exist 
        """
        try:
            if os.environ["key"]:
                return True
        except:
            return False
    
    def generate_key(self):
        """ Generate key if key does not exist
        :param:
        :return:
        """
        if not self.does_key_exist():
            key = Fernet.generate_key()
            key_str = str(key, "utf-8")
            os.environ['key'] = key_str
            set_key(self.dotenv_file, "key", os.environ['key'])

    def does_master_ps_exist(self):
        """ Check if master password hash 
        :param:
        :return bool: return bool if master hash exist 
        """
        try:
            if os.environ["master"]:
                return True
        except:
            return False
    
    def generate_master_hash(self, password):
        """ Generate master password hash
        :param password: password from user input 
        :return:
        """
        if not self.does_master_ps_exist(): 
            sha256_master = hashlib.sha256(password.encode()).hexdigest()
            os.environ["master"] = sha256_master
            set_key(self.dotenv_file, "master", os.environ["master"])
    
    def check_master_hash(self, password):
        """ Check is master password and master hash is the same
        :param password: password for user input
        :return bool: return bool if master password match master hash
        """
        hash = os.environ["master"]
        ps_hash = hashlib.sha256(password.encode()).hexdigest()
        if ps_hash == hash:
            return True
        else:
            return False
    
    def clear_dotenv(self):
        """ Clear the dotenv file (mainly for testing)
        :param:
        :return:
        """
        try:
            os.unsetenv("key")
            os.unsetenv("master")
            unset_key(self.dotenv_file, "key")
            unset_key(self.dotenv_file, "master")
            print("Dotenv cleared")
        except Exception as e:
            print(e)
    
    def get_key(self):
        """ Get key from dotenv file
        :param:
        :return key: return key in bytes
        """
        key = bytes(os.environ["key"], "utf-8")
        return key
        
    def encrypt(self, text):
        """ Encryption function to encrypt password
        :param text: text to encrypt (mainly for password)
        :return encrypt_text: return encrypted text
        """
        key = self.get_key()
        fernet = Fernet(key)
        encode_text = text.encode()
        encrypt_text = fernet.encrypt(encode_text)
        return encrypt_text
    
    def decrypt(self, encrypt_text):
        """ Decryption function to decrypt password
        :param encrypt_text: get encrypted text from database to decrypt
        :return text: return decrypted text
        """
        key = self.get_key()
        fernet = Fernet(key)
        decrypt_text = fernet.decrypt(encrypt_text)
        text = decrypt_text.decode()
        return text
    


if __name__ == "__main__":
    c = Crypt()
    # ps = "hello"
    # e_ps = c.encrypt(ps)
    # print(ps)
    # print(e_ps)
    # print(c.decrypt(e_ps))
    c.clear_dotenv()