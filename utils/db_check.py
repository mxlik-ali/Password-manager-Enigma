import dbconfig
from rich import print as printc
from rich.console import Console

def mark_db():
    db = dbconfig.dbconfig()
    cur = db.cursor()
    try:
        query = "CREATE TABLE initialization(initialized BOOLEAN)"
        cur.execute(query)
        query = "INSERT INTO initialization(initialized) VALUES(TRUE)"
        cur.execute(query)
    
    except Exception as e:
        printc('[red][Error in making the initialization table]')
        print(e)
        db.rollback()

    db.commit()
    db.close()


mark_db()

