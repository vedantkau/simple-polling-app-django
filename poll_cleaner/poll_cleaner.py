import time
import sqlite3

while True:
    current_time = time.strftime("%H:%M", time.localtime())
    if current_time == "23:59":
        db = sqlite3.connect("../polling_app.sqlite3")
        cursor = db.cursor()
        print("Cleanup started...")
        cursor.execute("update models_polls_list set disabled = true where (julianday(CURRENT_DATE) - julianday(creation_date)) > 5")
        db.commit()
        db.close()
    time.sleep(15)
