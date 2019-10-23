import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234",
)


mycursor = mydb.cursor()

drop_db = ("DROP DATABASE music_db")
create_db = ("CREATE DATABASE music_db")


#mycursor.execute(drop_db)
mycursor.execute(create_db)
mydb.commit()
mydb.close()


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234",
    database="music_db"
)
mycursor = mydb.cursor()

create_table = ("CREATE TABLE music (second VARCHAR(255), party_id INTEGER(255), position INTEGER(255),"
                " song_name VARCHAR(255), song_bpm VARCHAR(255), song_key VARCHAR(10), year VARCHAR(10),"
                " start_time VARCHAR(255), end_time VARCHAR(255), playtime VARCHAR(255), party_type VARCHAR(255),"
                " number_of_people INTEGER(255))")

drop_table = "DROP TABLE music"

#mycursor.execute(drop_table)
mycursor.execute(create_table)
mydb.commit()
