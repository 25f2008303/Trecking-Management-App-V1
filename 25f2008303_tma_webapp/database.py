import sqlite3

DBN="TMA25f2008303.db"

#establish connection
def connect():
    c=sqlite3.connect(DBN)
    c.row_factory=sqlite3.Row

    return c

#for creating tables(CT)
def ct():
    MyDB=connect()
    MC=MyDB.cursor() #MC-MyCursor

    MC.execute("""CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, FNAME TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE, password TEXT NOT NULL, role TEXT NOT NULL, is_active INTEGER DEFAULT 1)""")
    
    MC.execute("""CREATE TABLE IF NOT EXISTS staff(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, 
                phone_no TEXT, experience TEXT, appstat TEXT DEFAULT 'pending', FOREIGN KEY (user_id) REFERENCES users(id))""")

    MC.execute("""CREATE TABLE IF NOT EXISTS treks(
            id INTEGER PRIMARY KEY AUTOINCREMENT, trek_name TEXT NOT NULL, location TEXT NOT NULL, difficulty TEXT NOT NULL,
            duration_days INTEGER NOT NULL, available_slots INTEGER NOT NULL, start_date TEXT, end_date TEXT, status TEXT DEFAULT 'open',
            assigned_staff_id INT, FOREIGN KEY (assigned_staff_id) REFERENCES users(id))""")
    
    MC.execute("""CREATE TABLE IF NOT EXISTS bookings(id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL, trek_id INTEGER NOT NULL, booking_date TEXT, status TEXT DEFAULT 'booked',
            FOREIGN KEY (user_id) REFERENCES users(id),FOREIGN KEY (trek_id) REFERENCES treks(id))""")

    MyDB.commit()
    MyDB.close()

#for creating admin
def ca():
    MyDB=connect()
    MC=MyDB.cursor()

    MC.execute("SELECT * FROM users WHERE email=?",("HA@tmawebapp.com",))
    a=MC.fetchone()

    if a is None:
        MC.execute("""INSERT INTO users(FNAME, email, password, role, is_active) VALUES (?,?,?,?,?)""",
                   ("HA(Admin)","HA@tmawebapp.com","admin@123321","ADMIN",1))
        MyDB.commit()
    MyDB.close()



def InitialiseDB():
    ct()
    ca()

    
