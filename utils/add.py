from getpass import getpass
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from . import aesutils 
from . import dbconfig
from . import generate

from rich import print as printc
from rich.console import Console

def mp_ds():
    db= dbconfig()
    cur = db.cursor()
    cur.execute("SELECT device_secret FROM pm.secrets")


def computeMasterKey(mp,ds):
    password = mp.encode()
    salt = ds.encode()
    mk = PBKDF2(password,salt,dkLen = 32,count =1000000,hmac_hash_module= SHA512)
    return mk

def checkEntry(sitename, siteurl, email, username):
	db = dbconfig.dbconfig()
	cursor = db.cursor()
	query = f"SELECT * FROM pm.entries WHERE sitename = '{sitename}' AND siteurl = '{siteurl}' AND email = '{email}' AND username = '{username}'"
	cursor.execute(query)
	results = cursor.fetchall()

	if len(results)!=0:
		return True
	return False


def addEntry(mp, ds, sitename, siteurl, email, username):
	# Check if the entry already exists
	if checkEntry(sitename, siteurl, email, username):
		printc("[yellow][-][/yellow] Entry with these details already exists")
		return

	printc("[blue][Yes/No][/blue] Do you want to generate a password?")
	res = input()
	res = res.title()
	if res == 'Yes':
		password = generate.generatePassword(8)
	else:# Input Password
		password = getpass("Password: ")

	# compute master key
	mk = computeMasterKey(mp,ds)

	# encrypt password with mk
	encrypted = aesutils.encrypt(key=mk, source=password, keyType="bytes")

	# Add to db
	db = dbconfig.dbconfig()
	cursor = db.cursor()
	query = "INSERT INTO pm.entries (sitename, siteurl, email, username, password) values (%s, %s, %s, %s, %s)"
	val = (sitename,siteurl,email,username,encrypted)
	cursor.execute(query, val)
	db.commit()

	printc("[green][+][/green] Added entry ")
