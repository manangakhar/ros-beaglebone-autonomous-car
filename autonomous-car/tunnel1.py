import time
import Adafruit_BBIO.GPIO as GPIO

##########  CONSTANTS (START)  ##########
##DIRECTION##
DIRECTION_NONE     = 0
DIRECTION_FORWARD  = 1
DIRECTION_LEFT     = 2
DIRECTION_BACKWARD = 3
DIRECTION_RIGHT    = 4
##MOTOR##
MOTOR_LEFT_0  = 0
MOTOR_LEFT_1  = 1
MOTOR_RIGHT_0 = 2
MOTOR_RIGHT_1 = 3
##ULTRASONIC PINS##
US_TRIGGER_PIN = 0
US_ECHO_PIN    = 1
##ULTRASONIC LOCATIONS##
US_LOCATION_NORTH = 0
US_LOCATION_WEST  = 1
US_LOCATION_EAST  = 2
US_LOCATION_NW    = 3
US_LOCATION_NE    = 4
##DISTANCE THRESHOLDS##
DISTANCE_THRESHOLD_NORTH = 
DISTANCE_THRESHOLD_WEST  = 
DISTANCE_THRESHOLD_EAST  =
DISTANCE_THRESHOLD_NW    = 
DISTANCE_THRESHOLD_NE    =
##DISTANCE SAFE##  
DISTANCE_SAFE_NORTH      = 150 #cm
DISTANCE_SAFE_WEST       =
DISTANCE_SAFE_EAST       =
DISTANCE_SAFE_NW         =
DISTANCE_SAFE_NE         =
##TIMINGS##
TIMING_TILT  = 0.4
TIMING_EXTRA = 0.06


##########  CONSTANTS (END) ##########

def measure(ultrasonic):
  # This function measures a distance taking the pair of echo and trigger pin
  #print "in measure"
  GPIO.output(ultrasonic[US_TRIGGER_PIN], GPIO.HIGH)
  #print "b4 sleep"
  time.sleep(0.00001)
  #print "after sleep"
  GPIO.output(ultrasonic[US_TRIGGER_PIN], GPIO.LOW)
  start = time.time()
  
  while GPIO.input(ultrasonic[US_ECHO_PIN])==0:
    start = time.time()

  stop = start
  while GPIO.input(ultrasonic[US_ECHO_PIN])==1:
    stop = time.time()

  elapsed  = stop-start
  distance = (elapsed * 34300)/2

  return distance

def measure_average(direction):
  # This function takes 3 measurements and
  # returns the average.

  ultrasonic = lUs[direction] #changed parameters to direction than ultrasonic

  distance1 = measure(ultrasonic)
  time.sleep(0.2)
  distance2 = measure(ultrasonic)
  time.sleep(0.2)
  distance3 = measure(ultrasonic)

  distance = distance1 + distance2 + distance3
  distance = distance / 3
  
  return distance

# sleepTime less than 0 is infinite, default is infinite
def drive(direction, sleepTime = -1):
	if(direction == DIRECTION_NONE):
		for each in lMotors:
			GPIO.output(each,GPIO.LOW)
		if(sleepTime > 0): #btw no need for timer
			time.sleep(sleepTime)
		return

	# reset pins before next direction
	for each in lMotors:
			GPIO.output(each,GPIO.LOW)
	time.sleep(.2)

	if(direction == DIRECTION_FORWARD):
		GPIO.output(lMotors[MOTOR_LEFT_0],GPIO.HIGH)
		GPIO.output(lMotors[MOTOR_RIGHT_0],GPIO.HIGH)

	elif(direction == DIRECTION_LEFT):
		GPIO.output(lMotors[MOTOR_LEFT_1],GPIO.HIGH)
		GPIO.output(lMotors[MOTOR_RIGHT_0],GPIO.HIGH)

	elif(direction == DIRECTION_BACKWARD):
		GPIO.output(lMotors[MOTOR_LEFT_1],GPIO.HIGH)
		GPIO.output(lMotors[MOTOR_RIGHT_1],GPIO.HIGH)

	elif(direction == DIRECTION_RIGHT):
		GPIO.output(lMotors[MOTOR_LEFT_0],GPIO.HIGH)
		GPIO.output(lMotors[MOTOR_RIGHT_1],GPIO.HIGH)

	if(sleepTime > 0):
		time.sleep(sleepTime)
		drive(DIRECTION_NONE)
		#for each in lMotors:
			#GPIO.output(each,GPIO.LOW)


def main_function():
	#assuming at the start of tunnel
	drive(DIRECTION_FORWARD)
	#check north
	distance_north = measure_average(US_LOCATION_NORTH)
	if(distance_north < DISTANCE_THRESHOLD_NORTH):
		drive(DIRECTION_NONE)
		distance_west = measure_average(US_LOCATION_WEST)
		distance_east = measure_average(US_LOCATION_EAST)

		if(distance_west < DISTANCE_THRESHOLD_WEST):
			isTurnEastDone = false
			while(isTurnEastDone == False):
				drive(DIRECTION_RIGHT,TIMING_TILT)
				sleep(TIMING_TILT + TIMING_EXTRA)
				distance_check_north = measure_average(US_LOCATION_NORTH)
				if(distance_check_north > DISTANCE_SAFE_NORTH):
					isTurnEastDone = True

		else:
			isTurnWestDone = false
			while(isTurnWestDone == False):
				drive(DIRECTION_LEFT,TIMING_TILT)
				sleep(TIMING_TILT+TIMING_EXTRA)
				distance_check_north = measure_average(US_LOCATION_NORTH)
				if(distance_check_north > DISTANCE_SAFE_NORTH):
					isTurnWestDone = True

		drive(DIRECTION_FORWARD) #finally drive forward

	#check east
	distance_east = measure_average(US_LOCATION_EAST)
	if(distance_east < DISTANCE_THRESHOLD_EAST):
		drive(DIRECTION_LEFT,TIMING_TILT)
		sleep(TIMING_TILT)
		drive(DIRECTION_FORWARD)

	#check west
	distance_west = measure_average(US_LOCATION_WEST)
	if(distance_west < DISTANCE_THRESHOLD_WEST):
		drive(DIRECTION_RIGHT,TIMING_TILT)
		sleep(TIMING_TILT)
		drive(DIRECTION_FORWARD)

##TODO
##main thread starts (write code to check for main thread)

lMotors = ["P9_12","P9_11","P9_16","P9_15"]

#### ULTRASONIC (Initialization) ####
#assuming 5 ultrasonic sensors
#change values below
lUsNorth                 = ["",""]
lUsNorth[US_TRIGGER_PIN] = ""   #change here
lUsNorth[US_ECHO_PIN]    = ""   #change here

lUsWest                 = ["",""]
lUsWest[US_TRIGGER_PIN] = ""  #change here
lUsWest[US_ECHO_PIN]    = ""  #change here

lUsEast                 = ["",""]
lUsEast[US_TRIGGER_PIN] = "" #change here
lUsEast[US_ECHO_PIN]    = "" #change here

lUsNW                   = ["",""]
lUsNW[US_TRIGGER_PIN]   = "" #change here
lUsNW[US_ECHO_PIN]      = "" #change here

lUsNE                   = ["",""]
lUsNE[US_TRIGGER_PIN]   = "" #change here
lUsNE[US_ECHO_PIN]      = "" #change here

lUs                    = [[],[],[],[],[]]
lUs[US_LOCATION_NORTH] = lUsNorth
lUs[US_LOCATION_WEST]  = lUsWest
lUs[US_LOCATION_EAST]  = lUsEast
lUs[US_LOCATION_NW]    = lUsNW
lUs[US_LOCATION_NE]    = lUsNE


##setting up GPIO pins
for each in lMotors:
	GPIO.setup(each,GPIO.OUT)
for each in lUs:
	GPIO.setup(each[US_TRIGGER_PIN],GPIO.OUT)
	GPIO.setup(each[US_ECHO_PIN],GPIO.IN)
#resetting values
drive(DIRECTION_NONE)
for each in lUs:
	GPIO.output(each[US_TRIGGER_PIN], GPIO.LOW)

try:
	while(True):
		main_function()
except KeyboardInterrupt:
	# User pressed CTRL-C
	# Reset GPIO settings
	GPIO.cleanup()