from utils.dbconfig import dbconfig 
from config import *
import argparse
from getpass import getpass
import hashlib
import pyperclip
from termcolor import colored

from rich import print as printc
import sys
import utils.add
import utils.retrieve
import utils.generate


def inputAndValidateMasterPassword():
    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        mp = getpass("MASTER PASSWORD: ")
        hashed_mp = hashlib.sha256(mp.encode()).hexdigest()

        db = dbconfig()  # Assuming db is your database connection
        cursor = db.cursor()
        query = "SELECT * FROM pm.secrets"
        cursor.execute(query)
        result = cursor.fetchone()

        if hashed_mp == result[0]:
            return [mp, result[1]]  # Password is correct, return the data

        printc("[red][!] WRONG! [/red]")
        attempts += 1
        remaining_attempts = max_attempts - attempts
        if remaining_attempts > 0:
            print(f"Remaining attempts: {remaining_attempts}")
        else:
            printc("[green][Max attempts reached. Exiting program][/green].")
            sys.exit()

    print("Max attempts reached. Exiting program.")
    sys.exit()

def menu_prompt():
        """Asks user for a choice from Menu
        
        Raises:
            UserExits: User exits on choice prompt
        
        Returns:
            str -- Users choice
        """

        print(colored("\n\t*Enter 'exit' at any point to exit.*\n", "magenta"))
        print(colored("1) Add/Update a password", "blue"))
        print(colored("2) Look up a stored password", "blue"))
        print(colored("3) Delete a password", "blue"))
        print(colored("4) Exit program", "blue"))
        print(colored("5) Erase all passwords", "red"))
        print(colored("6) Delete all data including Master Password", "red"))

        choice = input("Enter a choice: ")

        if choice == "":
            return menu_prompt() # recursive call
        elif choice == "exit":
            raise UserExits
        else:
            return int(choice.strip())


def main():
    db = dbconfig()
    cur = db.cursor()
    db__init__()
    query = "SELECT * FROM pm.secrets "
    cur.execute(query)
    result = cur.fetchone()
    if result is None:
        config()

    else:
        res = inputAndValidateMasterPassword()
        if res == None:
            exit
        option = menu_prompt()
        if option == 1:
            sitename = input('Sitename: ')
            siteurl =  input('SiteURL: ')
            email = input('Email: ')
            username = input('Username ')
            utils.add.addEntry(res[0],res[1],sitename,siteurl,email,username)
        
        if option == 2:
            printc("[blue][1][/blue][green]To show all passwords saved[/green]")
            printc("[blue][2][/blue][green]To retrive a particular password [/green]")
            
            field = input()
            field = field.title()
            if field =='1':
                search = {}
                utils.retrieve.retrieveEntries(res[0],res[1],search)
            else:
                printc("[green]Enter the search field (U can skip some search fields)[/green]")
                search = {'sitename': '', 'siteurl': '', 'email': '', 'username': ''}
                keys = ['sitename', 'siteurl', 'email', 'username']

                for key in keys:
                    value = input(f"{key.capitalize()}: ")
                    if len(value) == 0:
                        del search[key]
                    else:
                        search[key] = value

                utils.retrieve.retrieveEntries(res[0],res[1],search)
        
        if option == 3:
            printc("[blue][Yes/No ][/blue][red]Do you really wnat to delete all the passwords[/red]")
                        
            field = input()
            field = field.title()
            if field =='No':
                sys.exit()
            else:
                printc("[green]Enter the search field (U can skip some search fields)[/green]")
                search = {'sitename': '', 'siteurl': '', 'email': '', 'username': ''}
                keys = ['sitename', 'siteurl', 'email', 'username']

                for key in keys:
                    value = input(f"{key.capitalize()}: ")
                    if len(value) == 0:
                        del search[key]
                    else:
                        search[key] = value

                del_pass(search)
        
        if option == 4:
            sys.exit()

        if option == 5:
            printc('[blue] [Yes/No] [/blue][red][!!!] Are you sure you want to delete all the passwords[/red]')
            response = input()
            response = response.title()
            if response == 'Yes':
                del_all()
            else:
                printc('[green]=>[/green][blue] [Yes/No] [/blue] Do you wnat to go towards the previous menu?')
                menu_res = input()
                menu_res = menu_res.title()
                if menu_res == 'Yes':
                    menu_prompt()
                else:
                    sys.exit()

        if option == 6:
            printc("[red][-] Deleting a config clears the device secret and all your entries from the database. This means you will loose access to all your passwords that you have added into the password manager until now. Only do this if you truly want to 'destroy' all your entries. This action cannot be undone. [/red]")

            op = input("So are you sure you want to continue? (y/N): ")
                    
            if op.upper() == "N" or op.upper == "" or op == "Y":
                sys.exit(0)
            else:
                delete()
                
            

                    

                
        
            



    



        

main()