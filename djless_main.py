"""
Welcome to Dj less source code, here you will find everything that you need to understand the way dj less works
to this time,

 this code was made only for data.csv provided from virtual serato's console. In the future our intention
it's to made this for all kind of history archives from any kind of Dj interface program or controller.



For the easy comprehension of the code it gonna be tag whit a "#" before every chunk to explain what its going on.
"""

#>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# 1) SET UP

#Ignore future warning from cvlib
def ignore():
    #trhis module ise used to irgnore warnings msgs
    from warnings import simplefilter
    simplefilter(action='ignore', category=FutureWarning)
ignore()

#Import packages
import cvlib as cv
import cv2
import numpy as np
import mysql.connector
import pandas as pd
import numpy as np
import csv

#Enable connection whit sql server
#Note, you should create a sql server and enable conection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234",
    database="music_db"
)
mycursor = mydb.cursor()

#>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# 2) READ MUSIC FILE.csv provided from controller program

print("Welcome to DJ less.v0")
print("step1 - Read musica data")

# 2.1 Read text archive

try:
        #musicain = input("Write the name or the source of the archive that you wish to Analaize: ")
        musicain = "example_history.csv"
        musica = pd.read_csv(musicain)

except FileNotFoundError:
        print("Error en el nombre o la ruta del archivo")
        raise()

# 2.2 Prepare data.
print("step 2 - Edit data")

# 2 Edit text archive
mycursor.execute("SELECT MAX(party_id) AS maximum FROM music")
result = mycursor.fetchall()
for i in result:
    n= (i[0])
try:
    musica['party_id'] = n+1
except:
    musica['party_id'] = 1

#musica['party_type'] = input("write the genre of the party: ")
musica['party_type'] = ("edm party")
musica['position'] = np.arange(len(musica))  #add a column of relative position to the list
musica = musica.reindex(columns=['party_id', 'position', 'name', 'year', 'bpm', 'key', 'start time', 'end time', 'playtime', 'party_type']) #re-arrange and add mising rows if not in file
musica.fillna(0, inplace=True) # fill "Nan" data whit 0's
musica1 = musica[1:]
musica1 = musica1.values.tolist() # convert list to a string

# 2.2.2 Add a relative time column to music
'''
Create two time column one as a string and other as a time delta.
'''

import datetime as dt
from datetime import datetime, date

vacio = datetime.strptime(('00:00:00'), '%H:%M:%S').time()
inicio = datetime.strptime(musica1[0][6], '%H:%M:%S').time()
fin = datetime.strptime(musica1[len(musica1)-1][6], '%H:%M:%S').time()
duracion = datetime.combine(date.today(), fin) - datetime.combine(date.today(), inicio)

a =  datetime.combine(date.today(), inicio) - datetime.combine(date.today(), inicio)
time=[a]
time1 = [['00:00:00']]

# Note: on this step we are arranging our time colummn every 10 seconds, it can be modified by changing "minutes and seoncs"
# values below, thanks to this we can have our data arranged by second of the party (vital information)

while a < ((duracion) + dt.timedelta(minutes=0)):
    a = a + dt.timedelta(seconds=10)
    time.append(a)
    time1.append([str((dt.datetime.combine(dt.date(1,1,1),vacio) + a).time())])



'''
To make easier the count, time delta frame list time are converted to seconds, in this way it is easier to know 
wich one is greater and isn't necessary to make other transformations when we start to analise the video
'''

# 2.2.3 time to time_second
# (note: time_second store

x=0
time_second=[]
while x < len(time):
    a = time[x].total_seconds()
    time_second.append(int(a))
    x+=1


# 2.2.4 Indicate the key seconds on the music (when every song has started relatively)

x=0
key_second=[]
while x < len(musica1):
    a = datetime.combine(date.today(), datetime.strptime(musica1[x][6], '%H:%M:%S').time()) - datetime.combine(
    date.today(), datetime.strptime(musica1[0][6], '%H:%M:%S').time())
    secondsa = int(a.total_seconds())
    key_second.append(secondsa)
    x+=1

# 2.2.5 Put music and time columns togheter

repeat=0
x=0
count=0
while repeat < (len(time_second)):
    if count < len(key_second):
        if  time_second[x]== 0:
            time1[x].extend(musica1[count])
            #print(time1[x])
            x+=1
            repeat+=1

        elif time_second[x] < key_second[count]:
            time1[x].extend(musica1[count])
            #print(time1[x])
            x+=1
            repeat+=1
        else:
            count+=1

    else:
        count=len(key_second)
        time1[x].extend(musica1[count-1])
        #print(time1[x])
        x+=1
        repeat+=1
musica2=time1

#>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# 3) Detect images
print("step 3 - Detect persons")

# 3.1 Open video
webcam = cv2.VideoCapture('tokyo_walk.mp4')

if not webcam.isOpened():
    print("Could not open webcam")
    exit()

# 3.2 loop through frames

fps = int(webcam.get(cv2.CAP_PROP_FPS))
count = 0
count_list = 0
npersons=[]

while webcam.isOpened():

    # read frame from webcam
    try:
        status, frame = webcam.read()
        if count%(time_second[count_list]*fps) == 0 :
            #notice that we are using time_second column to pick the frames so we dont analise the whole video
            if not status:
                print("End of the video")

            # apply face detection
            try:
                bbox, label, conf = cv.detect_common_objects(frame)
                npersons.append(label)
                print(npersons)
                count_list=len(npersons)
            except:
                webcam.release()
        count+=1

    except ZeroDivisionError:
        status, frame = webcam.read()
        if count ==0:

            # apply face detection
            bbox, label, conf = cv.detect_common_objects(frame)
            npersons.append(label)
            print(str(npersons) + "this is frame 1")
            count_list = len(npersons)

        count += 1
    except IndexError:
        webcam.release()

# 3.3 Create a column whit only number of persons detected trough the analysis

try:
    npersons_1 =[]
    x=0
    while x<= len(npersons):
        npersons_1.append(int((npersons[x].count('person'))))
        x+=1
except:
    pass


cv2.destroyAllWindows()

# 3.4 Add the column of number of person detected to our main list

x=0
while x < len(musica2):
    musica2[x].append(npersons_1[x])
    x+=1

for row in musica2:
    print(row)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Copy data into data base
print("step 4 - copy data into server")


sqlFormula = "INSERT INTO music (second, party_id, position, song_name, year, song_bpm, song_key, start_time, end_time, playtime, party_type, number_of_people) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
mycursor.executemany(sqlFormula, musica2)


mydb.commit()

print("sucefull copy!!")
print("bye!")

