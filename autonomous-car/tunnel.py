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
US_NORTH = 0
US_WEST  = 1
US_EAST  = 2
US_NW    = 3
US_NE    = 4
##DISTANCE THRESHOLDS##
DISTANCE_THRESHOLD_NORTH = 40 #cm
DISTANCE_THRESHOLD_WEST  = 20 #cm
DISTANCE_THRESHOLD_EAST  = 20 #cm
DISTANCE_THRESHOLD_NW    = 30 #cm
DISTANCE_THRESHOLD_NE    = 30 #cm
##DISTANCE SAFE##  
DISTANCE_SAFE_NORTH      = 150 #cm
DISTANCE_SAFE_WEST       = 40 #cm
DISTANCE_SAFE_EAST       = 40 #cm
DISTANCE_SAFE_NW         = 50 #cm
DISTANCE_SAFE_NE         = 50 #cm
##DISTANCE TUNNEL OUTSIDE CHECK##  
DISTANCE_TUNNEL_OUTSIDE_CHECK_NORTH = 200 #cm
DISTANCE_TUNNEL_OUTSIDE_CHECK_WEST  = 120 #cm
DISTANCE_TUNNEL_OUTSIDE_CHECK_EAST  = 120 #cm
DISTANCE_TUNNEL_OUTSIDE_CHECK_NW    = 120 #cm
DISTANCE_TUNNEL_OUTSIDE_CHECK_NE    = 120 #cm
##TIMINGS##
TIMING_TILT  = 0.4
TIMING_EXTRA = 0.06
TIMING_HALT  = 0.2


##########  CONSTANTS (END) ##########

def measure(ultrasonic):
  # This function measures a distance taking the pair of echo and trigger pin
  GPIO.output(ultrasonic[US_TRIGGER_PIN], GPIO.HIGH)
  time.sleep(0.00001)
  GPIO.output(ultrasonic[US_TRIGGER_PIN], GPIO.LOW)
  start = time.time()
  
  while GPIO.input(ultrasonic[US_ECHO_PIN]) == 0 :
    start = time.time()

  stop = start
  while GPIO.input(ultrasonic[US_ECHO_PIN]) == 1 :
    stop = time.time()

  elapsed  = stop-start
  distance = (elapsed * 34300)/2

  #print "time: ",elapsed,"     distance: ", distance # to check the time taken per distance

  return distance

def measure_distance(direction):
  # This function takes 3 measurements and
  # returns the average.

  ultrasonic = lUs[direction] #changed parameters to direction than ultrasonic

  distance1 = measure(ultrasonic)
  time.sleep(0.15)
  distance2 = measure(ultrasonic)
  time.sleep(0.15)
  distance3 = measure(ultrasonic)

  distance = distance1 + distance2 + distance3
  distance = distance / 3
  
  return distance

# sleepTime less than 0 is infinite, default is infinite
#not thread safe
def drive(direction, sleepTime = -1):

	#ignore same direction to avoid unnecessary sleep timer
	if(direction == prevDirection):
		if(sleepTime>0):
			time.sleep(sleepTime)
			direction = DIRECTION_NONE
		else:
			return
	prevDirection = direction

	# reset pins before next direction
	for each in lMotors:
			GPIO.output(each,GPIO.LOW)

	if(direction == DIRECTION_NONE):
		return

	#let the motor halt a li'l before changing direction
	time.sleep(TIMING_HALT)

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

def getCompassReading():
	degrees = 1
	return degrees

def main_function_2():
	#assuming at the end of tunnel
	#degrees = getCompassReading()
	
	drive(DIRECTION_FORWARD)
	distance_north = measure_distance(US_NORTH)
	distance_nw = measure_distance(US_NW)
	distance_ne = measure_distance(US_NE)
	l=[]
	l.append(distance_north,distance_nw,distance_ne)
	mini = min(l)
	if(mini < DISTANCE_THRESHOLD_NORTH):
		drive(DIRECTION_NONE)
		isTurnWestDone = false
		while(isTurnWestDone == False):
			drive(DIRECTION_LEFT,TIMING_TILT)
			distance_check_north = measure_distance(US_NORTH)
			if(distance_check_north > DISTANCE_SAFE_NORTH):
				isTurnWestDone = True
		distance_check_east = measure_distance(US_EAST)
		drive(DIRECTION_FORWARD)
		while(distance_check_east < DISTANCE_SAFE_EAST):
			sleep(TIMING_TILT)
			distance_check_east = measure_distance(US_EAST)
		#return to straight

		distance_ne = measure_distance(US_NE)
		curTime = time()
		while(distance_ne > DISTANCE_SAFE_NE):
			if ((time()-curTime) > 7):
				break
			drive(DIRECTION_RIGHT,TIMING_TILT)
			distance_ne = measure_distance(US_NE)
		drive(DIRECTION_LEFT,TIMING_TILT)
		drive(DIRECTION_FORWARD)


def main_function():

	if(isTunnelOver == True):
		main_function_2()
		return

	#assuming at the start of tunnel
	drive(DIRECTION_FORWARD)
	#check north
	distance_north = measure_distance(US_NORTH)
	if(distance_north < DISTANCE_THRESHOLD_NORTH):
		drive(DIRECTION_NONE)
		distance_west = measure_distance(US_WEST)
		distance_east = measure_distance(US_EAST)

		if(distance_west < DISTANCE_THRESHOLD_WEST):
			isTurnEastDone = false
			while(isTurnEastDone == False):
				drive(DIRECTION_RIGHT,TIMING_TILT)
				#sleep(TIMING_TILT + TIMING_EXTRA)
				distance_check_north = measure_distance(US_NORTH)
				if(distance_check_north > DISTANCE_SAFE_NORTH):
					isTurnEastDone = True

		else:
			isTurnWestDone = false
			while(isTurnWestDone == False):
				drive(DIRECTION_LEFT,TIMING_TILT)
				#sleep(TIMING_TILT+TIMING_EXTRA)
				distance_check_north = measure_distance(US_NORTH)
				if(distance_check_north > DISTANCE_SAFE_NORTH):
					isTurnWestDone = True

		drive(DIRECTION_FORWARD) #finally drive forward

	#check east
	distance_east = measure_distance(US_EAST)
	if(distance_east < DISTANCE_THRESHOLD_EAST):
		drive(DIRECTION_LEFT,TIMING_TILT)
		#sleep(TIMING_TILT)
		distance_east = measure_distance(US_EAST)
		drive(DIRECTION_FORWARD)

	#check west
	distance_west = measure_distance(US_WEST)
	if(distance_west < DISTANCE_THRESHOLD_WEST):
		drive(DIRECTION_RIGHT,TIMING_TILT)
		#sleep(TIMING_TILT)
		distance_west = measure_distance(US_WEST)
		drive(DIRECTION_FORWARD)

	if(distance_west > DISTANCE_TUNNEL_OUTSIDE_CHECK_WEST and distance_east > DISTANCE_TUNNEL_OUTSIDE_CHECK_EAST):
		drive(DIRECTION_NONE)
		distance_north = measure_distance(US_NORTH)
		distance_ne = measure_distance(US_NE)
		distance_nw = measure_distance(US_NW)
		if(distance_north > DISTANCE_TUNNEL_OUTSIDE_CHECK_NORTH and distance_ne > DISTANCE_TUNNEL_OUTSIDE_CHECK_NE && distance_nw > DISTANCE_TUNNEL_OUTSIDE_CHECK_NW):
			isTunnelOver = True


##TODO
##main thread starts (write code to check for main thread)

lMotors = ["P9_12","P9_11","P9_16","P9_15"]

#### ULTRASONIC (Initialization) ####
#assuming 5 ultrasonic sensors
#change values below
lUsNorth                 = ["",""]
lUsNorth[US_TRIGGER_PIN] = "" #change here
lUsNorth[US_ECHO_PIN]    = "" #change here

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
lUs[US_NORTH] = lUsNorth
lUs[US_WEST]  = lUsWest
lUs[US_EAST]  = lUsEast
lUs[US_NW]    = lUsNW
lUs[US_NE]    = lUsNE

prevDirection = DIRECTION_NONE
isTunnelOver = False

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

#TODO errors for ultrasonic
#TODO errors for infinite tilting

try:
	while(True):
		main_function()
except KeyboardInterrupt:
	# User pressed CTRL-C
	# Reset GPIO settings
	GPIO.cleanup()