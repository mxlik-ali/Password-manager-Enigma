import os
import sys
import string
import random
import hashlib
import sys

from utils.dbconfig import dbconfig
from rich import print as printc
from rich.console import Console
from getpass import getpass
console = Console()
def generateDeviceSecret(length=10):
    return ''.join(random.choices(string.ascii_uppercase+string.digits, k =length))

def checkConfig():
	db = dbconfig()
	cursor = db.cursor()
	query = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA  WHERE SCHEMA_NAME = 'pm'"
	cursor.execute(query)
	results = cursor.fetchall()
	db.close()
	if len(results)!=0:
		return True
	return False


def config():
    db = dbconfig()
    cur = db.cursor()
    

    while 1:
        mp = getpass('Choose a MASTER PASSWORD')
        if mp ==getpass('Re-type') and mp!="":
            break
        printc('[yellow][.]Please try again[/yellow]')

    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
    printc('[green][+[/green] Generated hash of MASTER PASSWORD]')

    ds = generateDeviceSecret()
    printc("[green][+][/green] Device Secret is Generated")

    query = "INSERT INTO pm.secrets(masterkey_hash, device_secret) VALUES (%s,%s)"
    val=(hashed_mp,ds)
    cur.execute(query,val)
    db.commit()

    printc("[green][+][/green] Added to the database")
    printc("[green][+]Configuration done[/green]")
    db.close()


def db__init__():
    try:
        if not checkConfig():
            db = dbconfig()  # Assuming dbconfig() establishes the database connection
            cur = db.cursor()
            try:
                cur.execute("CREATE DATABASE pm")
            except Exception as e:
                printc("[red][!] An error occured while creating a database")
                console.print_exception(show_locals = True)
                sys.exit(0)
            printc("[green][+][/green] Database 'pm created")

            query = "CREATE TABLE pm.secrets(masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"
            res = cur.execute(query)
            printc("[green][+][/green]Tables secret created")

            query = "CREATE TABLE pm.entries(sitename TEXT NOT NULL, siteurl TEXT NOT NULL,email TEXT, username TEXT, password TEXT NOT NULL )" 
            res = cur.execute(query)
            printc('[green][+][/green] Tables entries created')
            db.commit()
            db.close()

            
            printc('[green]Database initialized successfully[/green]')
        else:
            printc('[yellow]Database already initialized[/yellow]')

    except Exception as e:
        printc(f'[red]Error initializing database: {e}[/red]')

def del_pass(field):
    try:
        db = dbconfig()  # Establish your database connection
        cur = db.cursor()

        # Construct the query dynamically
        query = "DELETE FROM pm.entries WHERE "
        conditions = []

        for key, value in field.items():
            if value:
                conditions.append(f"{key} = '{value}'")

        if conditions:
            query += " AND ".join(conditions)
            cur.execute(query)  # Execute the query
            db.commit()
            db.close()
            printc("[green][-][/green] Password deleted successfully")
        else:
            printc("/n[yellow]No conditions provided for deletion.[/yellow]")

    except Exception as e:
        print(f'Error deleting passwords: {e}')
	
def del_all():
    try:
        db = dbconfig()
        cur = db.cursor()
        query = 'DELETE FROM pm.entries'
        cur.execute(query)
        printc("[green][-][/green] All Passwords deleted successfully")
        db.commit()
        db.close()
    except Exception as e:
        print(f'Error deleting passwords: {e}')

def delete():
    printc("[green][-][/green] Deleting config")

    if not checkConfig():
        printc("[yellow][-][/yellow] No configuration exists to delete!")
        return

    success = True
    try:
        db = dbconfig()
        cursor = db.cursor()
        query = "DROP DATABASE pm"
        cursor.execute(query)
        db.commit()
        db.close()
    except Exception as e:
        print(f"Error deleting config: {e}")
        success = False
    if success:
        printc("[green][+] Config deleted![/green]")
    sys.exit()

def delete_rw():
    printc("[green][-][/green] Deleting config")

    if not checkConfig():
        printc("[yellow][-][/yellow] No configuration exists to delete!")
        return

    success = True
    try:
        db = dbconfig()
        print("Got the DB connection")
        cursor = db.cursor()
        print("Got the cursor")
        query = "DROP DATABASE pm"
        cursor.execute(query)
        print("Executed the query")
        db.commit()
        print("Committed changes")
        db.close()
        print("Closed the connection")
    except Exception as e:
        print(f"Error deleting config: {e}")
        success = False

    if success:
        printc("[green][+] Config deleted![/green]")
    else:
        print("Deletion failed!")

