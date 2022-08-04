import time
import datetime
from firebase import firebase

watered = False
art_light=False
fan=False

def automate():
    thresh = 30
    lthresh=30
    fthresh=50
    name="Rice"
    tl=0
    th=0
    ml=0
    mh=0
    moisture = 706
    temp=500
    humidity=400
    light=300
    for i in range(0,17):
      namec=firebase.get('crop_data/'+str(i) , 'name')
      if namec==name:
        tl=int(firebase.get('crop_data/'+str(i) , 'temp_low'))
        th=int(firebase.get('crop_data/'+str(i) , 'temp_high'))
        ml=int(firebase.get('crop_data/'+str(i) , 'moist_low'))
        mh=int(firebase.get('crop_data/'+str(i) , 'moist_high'))
        break
    print("Ideal conditions for "+name+": \nTemperature(in C): "+str(tl)+"-"+str(th)+": \nMoisture level(in rainfall cms): "+str(ml)+"-"+str(mh))
    light=100*light/1023
    temp=100*temp/1023
    global watered
    global art_light
    global fan
    if light<lthresh and art_light==False:
        print("turning on artificial light")
        art_light=True
    else:
      if light>lthresh:
        print("turning off artificial light")
        art_light=False
    print(th)
    print(temp)    
    if temp>th and not fan:
        print("turning on fan")
        fan=True
    else:
      if temp<tl:
        print("turning off fan")
        fan=False
    print("watered?", watered)
    time = datetime.datetime.now().strftime("%H:%M")
    print("current time", time)
    if (((time > "17:00") and (time < "18:00")) or ((time > "10:45") and (time < "11:30"))):
        if not watered:
            while True:
                    #read moisture sensor value using Raspberry Pi
                moisture = 100 - (100*moisture/1023)
                if moisture < ml*0.1:
                        #turn motor off
                    watered = True
                    break
                else:
                    #turn motor on
                    print()
    else:
        watered = False
    #turn motor off

dht_sensor = 4
light_sensor = 0
moisture_sensor = 1
motor = 3
moisture=706

#motor - output pin
#temparature and humidity sensor - input pin
#light sensor - input pin
#moisture sensor - input pin

firebase = firebase.FirebaseApplication('https://iot-garden-7364d-default-rtdb.firebaseio.com/', None)

initTime = time.time()

while True:
    motor_state = firebase.get('/enter the project bucket here', 'motor_state')
    update = firebase.get('/enter the project bucket here', 'update')
    pi_state = firebase.get('/enter the project bucket here', 'pi_state')
    print("received data in ",int(time.time()-initTime),"seconds")
    initTime = time.time()

    if (pi_state == "0"):
    #turn motor off
        break
    
    #read temperature sensor reading
    #read humidity sensor reading
    #read light sensor reading
    #read moisture sensor reading
    temp=500
    humidity=400
    light=300

    light = 100*light/1023
    moisture = 100 - (100*moisture/1023)

    print("temp = ",temp)
    print("humidity = ", humidity)
    print("light = ", light)
    print("moisture = ", moisture)
    if (update == "1"):
        print("updating db")
        firebase.put('enter the project bucket here', 'temperature', str(temp))
        firebase.put('enter the project bucket here', 'humidity', str(humidity))
        firebase.put('enter the project bucket here', 'light', str(light))
        firebase.put('enter the project bucket here', 'moisture', str(moisture))
        firebase.put('enter the project bucket here', 'update', str(0))
    if (motor_state == "1"):
        #turn on motor
        print("motor turned on\n")
    elif (motor_state == "2"):
        #automate
        print("motor automatic control\n")
        automate()
    else:
        #turn off motor
        print("motor turned off\n")