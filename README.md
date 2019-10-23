# Dj-less-main

“Dj less”, AI based project aiming to measure the flow of a party via a camera and select the right song for the moment, looking to create the first real substitute for Dj’s in small parties. 



In this folder you gonna find the code for a basic data collector that uses as imput history archives from Seratos Dj pro (.csv) and videos (.mp4) 
At this point we are able to cross the information provided by the music reproductor whit the image recognition program and merge it in one data base. Notice that image recognition is being made whit a generic dataset trained to detect common object as well as people, due this we are using videos whit people from easier angles and birghter images, so the algorithm can detect them easily. 


To set up dj less.v0.0 please 

1) download:

SQL DB_TABLE.py
djless_main.py
example_history.csv

and the example video here:
https://drive.google.com/file/d/1IJFRLDy4gP74rnNfZikbmbaW7OWu7t6D/view?usp=sharing

2) make sure that you have a local instance in SQL, djless_main.py uses by default
   host="localhost",
    user="root",
    passwd="1234"

3) move everything to the same folder
4) Run SQL DB_TABLE.py
4) Run djless_main.py
    
  
To continue the development of the program and get a minimum viable product (MVP) we still have ahead:

  - Collect a small size DataBase (20 samples)
  - Create a data set for the image recognition program, made specifically whit people under club conditions
  - Develop the regresion algorithm (temptative random forest)
  - Develop te song selection algorithm that have a camera as imput
  - Develop an small music reproductor capable of use a crossfader.

*Song selection algorithm could be made using the same dataset and algorithm in the image recognition module in use (cvlib)






