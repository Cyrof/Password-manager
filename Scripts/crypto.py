from distutils.sysconfig import get_makefile_filename
from cryptography.fernet import Fernet
from dotenv import load_dotenv, find_dotenv, set_key, unset_key
import os
import hashlib

class Crypt:

    def __init__(self):
        self.dotenv_file = find_dotenv()
        load_dotenv(self.dotenv_file)
        self.check_env()

    def check_env(self):
        with open(".env", "a") as f:
            f.close()
    
    def does_key_exist(self):
        try:
            if os.environ["key"]:
                return True
        except:
            return False
    
    def generate_key(self):
        if not self.does_key_exist():
            key = Fernet.generate_key()
            key_str = str(key, "utf-8")
            os.environ['key'] = key_str
            set_key(self.dotenv_file, "key", os.environ['key'])

    def does_master_ps_exist(self):
        try:
            if os.environ["master"]:
                return True
        except:
            return False
    
    def generate_master_hash(self, password):
        if not self.does_master_ps_exist(): 
            sha256_master = hashlib.sha256(password.encode()).hexdigest()
            os.environ["master"] = sha256_master
            set_key(self.dotenv_file, "master", os.environ["master"])
    
    def check_master_hash(self, password):
        hash = os.environ["master"]
        ps_hash = hashlib.sha256(password.encode()).hexdigest()
        if ps_hash == hash:
            return True
        else:
            return False
    
    def clear_dotenv(self):
        try:
            os.unsetenv("key")
            os.unsetenv("master")
            unset_key(self.dotenv_file, "key")
            unset_key(self.dotenv_file, "master")
            print("Dotenv cleared")
        except Exception as e:
            print(e)
    
    def get_key(self):
        key = bytes(os.environ["key"], "utf-8")
        return key
        
    def encrypt(self, text):
        key = self.get_key()
        fernet = Fernet(key)
        encode_text = text.encode()
        encrypt_text = fernet.encrypt(encode_text)
        return encrypt_text
    
    def decrypt(self, encrypt_text):
        key = self.get_key()
        fernet = Fernet(key)
        decrypt_text = fernet.decrypt(encrypt_text)
        text = decrypt_text.decode()
        return text
    


if __name__ == "__main__":
    c = Crypt()
    ps = "hello"
    e_ps = c.encrypt(ps)
    print(ps)
    print(e_ps)
    print(c.decrypt(e_ps))
