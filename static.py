import sqlite3

dbname = 'database.db'

tempertures = [
    "36.0°C", "36.1°C", "36.2°C", "36.3°C", "36.4°C", "36.5°C", "36.6°C", "36.7°C", "36.8°C"
]

times = [
    "00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00",
]

def checkLoginState(id: str) -> bool:
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    
    cur.execute("SELECT * FROM users WHERE id = ?", (id,))
    
    res = cur.fetchall()
    
    con.close()
    
    if len(res) == 0:
        return False
    else:
        return True