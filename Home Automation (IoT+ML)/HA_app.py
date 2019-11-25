# python3 -m pip3 install scikit-learn 

from flask import Flask, render_template
import RPi.GPIO as GPIO
import Adafruit_DHT

##DHT 11
# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor=Adafruit_DHT.DHT11
 
# Set GPIO sensor is connected to
gpio=17
 
# Use read_retry method. This will retry up to 15 times to
# get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)


####################################
import csv
with open('weather_new1.csv','r') as f1:
    X=list(csv.reader(f1, delimiter=','))
with open('weather_target1.csv','r') as f2:
    Y=list(csv.reader(f2,delimiter=','))

import numpy as np
X=np.array(X, dtype=np.float)
Y=np.array(Y[:35177])
Y=np.ravel(Y,order='C')
print(X.shape)
print(Y.shape)

#-----------
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.3)

#-----------MODEL CREATION-------
print('')                                        
print(X_train.shape) #
print(Y_train.shape) #
print(X_test.shape)  #
print(Y_test.shape)  #

#create model (KNN)
from sklearn.neighbors import KNeighborsClassifier
K=KNeighborsClassifier(n_neighbors=120)

#train model
K.fit(X_train,Y_train)

#test model
Y_pred_knn=K.predict(X_test)
#check
print(Y_pred_knn==Y_test)

#find accuracy of knn model
from sklearn.metrics import accuracy_score
acc_knn=accuracy_score(Y_test,Y_pred_knn)
print("accuracy in knn:",round(acc_knn*100,2),'%')
print('')
print(K.predict([[temperature,humidity]]))
######################################
'''
# Reading the DHT11 is very sensitive to timings and occasionally
# the Pi might fail to get a valid reading. So check if readings are valid.
if humidity is not None and temperature is not None:
  print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
  print('Failed to get reading. Try again!')
'''
########

GPIO.setmode(GPIO.BOARD)

#define actuators pin
relay=40

#initialise pin status
relaySts='OFF'

GPIO.setup(relay,GPIO.OUT)
GPIO.output(relay,False)

app= Flask(__name__)
@app.route('/')
def index():
	#read status
	if GPIO.input(relay):
		relaySts='ON'
	else:
		relaySts='OFF'

	while True:
		humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
		templateData={
			'title': 'Device Status',
			'relay': relaySts,
			'temp': temperature,
			'hum': humidity,
			'weather': K.predict([[temperature,humidity]])
			}
		return render_template('index.html',**templateData)
			
@app.route('/<deviceName>/<action>')
def action(deviceName,action):
	if deviceName=='relay':
		actuator=relay
	
	if action=='on':
		GPIO.output(actuator, True)
	if action=='off':
		GPIO.output(actuator, False)
		
	if GPIO.input(relay):
		relaySts='ON'
	else:
		relaySts='OFF'
		
	while True:
		humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
		templateData={
			'title': 'Device Status',
			'relay': relaySts,
			'temp': temperature,
			'hum': humidity,
			'weather': K.predict([[temperature,humidity]])
			}
		return render_template('index.html',**templateData)
	
if __name__=='__main__':
	app.run(debug=True,port=80,host='0.0.0.0')


#############
