#SENSOR HC-SR40
#VALVE

#Author : Schrodinger's Kat
import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)

TRIGR = 23
EOR = 24
TRIGW = 17
EOW = 27
MOR = 5
MOW = 6
MOO = 13
MOA = 12

GPIO.setup(TRIGR,GPIO.OUT)
GPIO.setup(EOR,GPIO.IN)
GPIO.setup(TRIGW,GPIO.OUT)
GPIO.setup(EOW,GPIO.IN)
GPIO.setup(MOR,GPIO.OUT)
GPIO.setup(MOW,GPIO.OUT)
GPIO.setup(MOO,GPIO.OUT)
GPIO.setup(MOA,GPIO.OUT)
GPIO.setwarnings(False)

def USONICR():
		GPIO.output(TRIGR, False)
  		time.sleep(5)
  		GPIO.output(TRIGR, True)
 		time.sleep(0.00001)
  		GPIO.output(TRIGR, False)

  		while GPIO.input(EOR)==0:
    			pulse_start = time.time()
		while GPIO.input(EOR)==1:
    			pulse_end = time.time()

  		pulse_duration = pulse_end - pulse_start

  		distR = (pulse_duration/2)*34200
  		distR = round(distR, 2)
		print "Rubber Volume in Scale:",distR ,"cm"
		return distR


def USONICW():
		GPIO.output(TRIGW, False)
		time.sleep(5)
		GPIO.output(TRIGW, True)
		time.sleep(0.00001)
		GPIO.output(TRIGW, False)

		while GPIO.input(EOW)==0:
				pulse_start = time.time()
		while GPIO.input(EOW)==1:
				pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start
		distW = (pulse_duration/2)*34200
		distW = round(distW, 2)
		print "Water Volume in Scale:",distW - 0.5,"cm"
		return distW - 0.5



def MOTO(pin):
		GPIO.output(pin,GPIO.HIGH)
		print "Motor Openned @ pin",pin


def MOTC(pin):
		GPIO.output(pin,GPIO.LOW)
		print "Motor Closed @ pin",pin



def Rvolm():
		Rsens = USONICR()
		Rlevel = 33 - Rsens
		vol = 1.5 * Rlevel
		print "Rubber Volume : ",vol
		return vol

def Wvolm():
		Wsens = USONICW()
		Wlevel = 31 - Wsens
		ruvol =  1.5 * Wlevel
		print "Water Volume : ",ruvol
		return ruvol



if __name__ == '__main__' :
	try:
		count = 0
		Wreq = 1
		while count < 5:
                    print"Iteration : ",count
                    Rvol = Rvolm()
                    Wvol = Wvolm()
                    Wsbnit = Wvol - Wreq
                    print"Water Should Be init : ",Wsbnit
                    i = 1 #i = last few litres of neoprene in the Rubber container which is of no use
                    while Rvol > i:
                        MOTO(MOR)
                        time.sleep(5) #Rubber flow rate should be calculated beforehand through the tube (20 sec for 1 litre discharge of Rubber)
                        MOTO(MOW)
                        time.sleep(10)#Water Flow rate should be calculated beforehand through the tube (10 sec for 1 litre discharge of Water)
						MOTC(MOW)
						time.sleep(5)
						MOTC(MOR)
						Rvol = Rvolm() + .2
						Wvol = Wvolm() + .2
						MOTO(MOA)
                        time.sleep(5)#Acid flow rate should be calculated beforehand through the tube (3 sec for required _ml of Acid )
						MOTC(MOA)
						time.sleep(30)#Coagulation for dome time(Rubber,Water,Acid)
                    	MOTO(MOO)
                    	print "Outlet Open"
                    	time.sleep(20)#discharge rate of the coagulated solution to rubber dish
                    	MOTC(MOO)

                    count=count+1

        except KeyboardInterrupt:
		GPIO.cleanup()
