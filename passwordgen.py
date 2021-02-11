# Password Generator for Touchportal with Keepass and Vault syncronisation.

import os
import getopt, sys
import string
import random
import clipboard
import configparser
from pykeepass import PyKeePass
import hvac
import datetime
import getpass


LETTERS = string.ascii_letters
NUMBERS = string.digits
SPECIALCHAR = '#.:,;!"§$%&/()=?'



### config file
if  not os.path.exists("./.passwordgen"):
    print("config file not found...")
    print()
    config = configparser.ConfigParser()
    print("Setup started...")
    print()
    #print(r'example D:\DATA\Nextcloud\INFOBOX\PRIVAT\DD.kdbx')
    KEEPASSFILE= input(r'enter the path for you KeePass File (example D:\DATA\Nextcloud\INFOBOX\PRIVAT\DD.kdbx): ')
    print("enter Password for KeePass File")
    KEEPASSPWD=getpass.getpass()

    KEEPASSGROUP= input("enter default KEEPASSGROUP (must exists, ex. DDKEYGEN): ")
    VAULTENABLE= input("vault enabled and activated? (Y/N) ")
    VAULTURL= input("enter you vault url (ex. http://192.168.0.1:8200): ")
    VAULTKV= input("enter your default KV (ex. dd/): ")
    config['DEFAULT'] = {'KEEPASSFILE': KEEPASSFILE, 
                         'KEEPASSPWD': KEEPASSPWD,
                         'KEEPASSGROUP': KEEPASSGROUP,
                         'VAULTENABLE': VAULTENABLE.upper(),
                         'VAULTURL': VAULTURL,
                         'VAULTKV': VAULTKV
    }
    with open('.passwordgen', 'w') as configfile:
      config.write(configfile)
    quit()


config = configparser.ConfigParser()
config.sections()
config.read('.passwordgen')



### KEEPASS
kp = PyKeePass(config['DEFAULT']['KEEPASSFILE'], password=config['DEFAULT']['KEEPASSPWD'])
KEEPASSDEFAULTGRP = config['DEFAULT']['KEEPASSGROUP']

### VAULT
if (config['DEFAULT']['VAULTENABLE']== 'Y'):
    client = hvac.Client(url=config['DEFAULT']['VAULTURL'])
    client.token = os.environ['VAULT_TOKEN']
    if (client.is_authenticated() == False or client.sys.is_sealed() == True):
        print('Vault Probleme...')
        quit()

def password_generator(length=8):
  
        printable = NUMBERS + LETTERS + SPECIALCHAR

        # convert string to list and shuffle
        printable = list(printable)
        random.shuffle(printable)

        # generate random password
        random_password = random.choices(printable, k=length)

        # convert to string
        random_password = ''.join(random_password)
        return random_password


if __name__ == '__main__':
        argument_list = sys.argv

        pwdlength = 18   # default password length

        DISPLAYPWD = True
        CREATE = False
        KEEPASSWRITE = True
        KEEPASSTITEL = datetime.datetime.now()
        KEEPASSUSERNAME = ""

        for idx, arg in enumerate(sys.argv):

            if arg == '--help' or (len(sys.argv)==1):
                print()
                print("Password Generator (c) 2021 by Dirk Derichsweiler")
                print("usage: passwordgen <parameters>")
                print()
                print("parameter: ")
                print()
                print("--create  generates an random password")
                print("--title <value>   tile for Keepass entry")
                print("--username <value> username for Keepass entry")
                print("--count  amount of characters")
                print("--hide   hide password")
                print("--temp   do not write to keepassfile")
                print("")
                print("--getuser <searchstring>   get username")
                print("--getpassword <search string>  get password")
    

            if arg == '--getuser':
                all = kp.entries
                result = kp.find_entries(title=sys.argv[idx+1], first=True)
                clipboard.copy(result.username)

            if arg == '--getpassword':
                all = kp.entries
                result = kp.find_entries(title=sys.argv[idx+1], first=True)
                clipboard.copy(result.password)

            if arg == '--hide':
                DISPLAYPWD = False

            if arg == '--temp':
                KEEPASSWRITE = False

            if arg == '--create':
                CREATE = True

            if arg == '--title':
                KEEPASSTITEL = sys.argv[idx+1]
            
            if arg == '--username':
                KEEPASSUSERNAME = sys.argv[idx+1]

            if arg == "--count":
                if (len(sys.argv) > idx+1):
                  pwdlength = sys.argv[idx+1]
                else:
                    print(f"ERROR: count value is missing using default value: {pwdlength}")


        if (CREATE):
          password = password_generator(int(pwdlength))
          if (DISPLAYPWD):
            print(password)          
          clipboard.copy(password)
          if (KEEPASSWRITE):
              group = kp.find_groups(name=KEEPASSDEFAULTGRP, first=True)
              kp.add_entry(group, str(KEEPASSTITEL), str(KEEPASSUSERNAME), str(password))
              kp.save()
              if (config['DEFAULT']['VAULTENABLE']== 'Y'):
                client.write(str(config['DEFAULT']['VAULTKV'] + KEEPASSTITEL),
                    username = KEEPASSUSERNAME,
                    password = password,
                    )