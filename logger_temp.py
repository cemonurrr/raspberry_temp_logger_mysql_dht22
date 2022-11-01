import sys, Adafruit_DHT
import mysql.connector
import requests

sensor=Adafruit_DHT.DHT22  

db =mysql.connector.connect(host='localhost',user='user', passwd='pass', db='temp_log')

humidity, temperature = Adafruit_DHT.read_retry(sensor, 4)

if humidity is not None and humidity >= 0.0 and humidity <= 100.0 and temperature is not None and temperature > -100.0 and temperature < 150.0:
    cur = db.cursor()
    cur.execute("INSERT INTO kayitlar(cihaz, temperature, humidity) VALUES ('1'," + str(temperature) + "," + str(humidity) + ")")
    db.commit()
    cur.close()
    del cur
    db.close()

#send sms if temp up > 25 
if  temperature is not None and temperature > 25.0:
 response = requests.get(
    'https://api.netgsm.com.tr/sms/send/get',
    params={'usercode': 'user', 'password': 'pass', 'gsmno':'05550000000','message': 'Server odasi sicaklik uyarisi: Suanki oda sicakligi : " + str(temperature) + " ', 'msgheader': 'header.'},
 )
