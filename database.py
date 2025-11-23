import sqlite3
import os

# veri tabanı yolu oluşturma data/assistant.db
DB_PATH=os.path.join("data","assistant.db")

def initialize_db():
    #eğer data klasörü yoksa oluştursun
    os.makedirs("data",exist_ok=True)

    # veritabanına bağlan ve dosya yoksa oluştur
    conn=sqlite3.connect(DB_PATH)
    cursor=conn.cursor()

    #eğer notes tablosu yoksa oluştur
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS notes(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,        --not icerigi
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- NOT GELDİĞİ ZAMAN ŞİMDİKİ ZAMANI VERECEK
                    )
        
                   """)


    # etkinlik açıklaması ve etkinlik tarihi
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS calendar(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        event TEXT NOT NULL,     --etkinlik açıklaması boş olamaz
                        event_date TEXT NOT NULL  --etkinlik tarihi
                   )

                   """)


    conn.commit()
    conn.close()


#veritabanına not ekleme
def add_notes(content):
    # veritabanına bağlan
    conn=sqlite3.connect(DB_PATH)
    cursor=conn.cursor()

    #content notes tablossuna ekle
    cursor.execute("insert into notes (content) VALUES (?)",(content,))

    conn.commit()
    conn.close()



# veritabanına etkinlik ekleme
def add_event(event,event_date):
    conn=sqlite3.connect(DB_PATH)
    cursor=conn.cursor()

    # etkinlik ve tarih "calendar" tablosuna ekle
    cursor.execute("INSERT INTO calendar (event,event_date) VALUES (?,?)",(event,event_date))
    conn.commit()
    conn.close()


# tüm notları veritabanından sıralı getirme
def get_notes():
    conn=sqlite3.connect(DB_PATH)
    cursor=conn.cursor()

    cursor.execute("SELECT content,created_at FROM notes ORDER BY created_at DESC")
    notes=cursor.fetchall()# sonuçları liste olarak alma
    conn.close()

    return notes

# tüm etkinlikleri veri tabanından sıralı şekilde getiren 
def get_events():
    conn=sqlite3.connect(DB_PATH)
    cursor=conn.cursor()

    cursor.execute("select event,event_date FROM calendar ORDER BY event_date")

    events=cursor.fetchall()
    conn.close()
    return events



if __name__=="__main__":
    initialize_db()
    #add_notes("yumurta al")
    #add_event("toplantı var","25.11.2025")

    #print(f"Notes: {get_notes()}")

    #print(f"Events: {get_events()}")



   






