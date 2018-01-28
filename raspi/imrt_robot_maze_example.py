# Example code for IMRT100 robot project


# Import some modules that we need
import imrt_robot_serial
import signal
import time
import sys

LEFT = -1
RIGHT = 1
FORWARDS = 1
BACKWARDS = -1
DRIVING_SPEED = 100
TURNING_SPEED = 100

def stopRobot(duration):

    iterations = int(duration * 10)
    
    for i in range(iterations):
        motor_serial.sendCommand(0, 0)
        time.sleep(0.10)



def driveRobot(direction, duration):
    
    speed = DRIVING_SPEED * direction
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.sendCommand(speed, speed)
        time.sleep(0.10)



def turnRobot(direction, duration):
    
    speed = TURNING_SPEED * direction
    iterations = int(duration * 10)
    
    for i in range(iterations):
        motor_serial.sendCommand(speed, -speed)
        time.sleep(0.10)



# We want our program to send commands at 10 Hz (10 commands per second)
execution_frequency = 10 #Hz
execution_period = 1. / execution_frequency #seconds


# Create motor serial object
motor_serial = imrt_robot_serial.IMRTRobotSerial()


# Open serial port. Exit if serial port cannot be opened
try:
    motor_serial.connect("/dev/ttyACM0")
except:
    print("Could not open port. Is your robot connected?\nExiting program")
    sys.exit()

    
# Start serial receive thread
motor_serial.run()

stop_dist = 20
# Now we will enter a loop that will keep looping until the program terminates
# The motor_serial object will inform us when it's time to exit the program
# (say if the program is terminated by the user)
print("Entering loop. Ctrl+c to terminate")
while not motor_serial.shutdown_now :


    ###############################################################
    # This is the start of our loop. Your code goes below.        #
    #                                                             #
    # An example is provided to give you a starting point         #
    # In this example we get the distance readings from each of   #
    # the two distance sensors. Then we multiply each reading     #
    # with a constant gain and use the two resulting numbers      #
    # as commands for each of the two motors.                     #
    #  ________________________________________________________   #
    # |                                                        |  #
    # V                                                           #
    # V                                                           #
    ###############################################################






    # Get and print readings from distance sensors
    dist_1 = motor_serial.getDist1()
    dist_2 = motor_serial.getDist2()
    print("Dist 1:", dist_1, "   Dist 2:", dist_2)

    # Check if there is an obstacle in the way
    if dist_1 < stop_dist or dist_2 < stop_dist:
        # There is an obstacle in front of the robot
        # First let's stop the robot for 1 second
        print("Obstacle!")
        stopRobot(1)

        # Turn left for 1.4 seconds
        print("Turning left")
        turnRobot(LEFT, 1.4)

        # Get sensor values
        dist_1 = motor_serial.getDist1()
        dist_2 = motor_serial.getDist2()

        # Check if there is an obstacle in the way
        if dist_1 < stop_dist or dist_2 < stop_dist:
            # There was an obstacle on the left side
            # Let's see try turning to the right
            print("Obstacle!")
            print("Turning right")
            turnRobot(RIGHT, 2.8)

            dist_1 = motor_serial.getDist1()
            dist_2 = motor_serial.getDist2()

            # Check if there is an obstacle in the way
            if dist_1 < stop_dist or dist_2 < stop_dist:
                # There was an obstacle on the right side
                # Let's turn back and reverse for a bit, the turn right
                print("Obstacle!")
                print("Will try further back")
                turnRobot(LEFT, 1.4)
                driveRobot(BACKWARDS, 2)
                turnRobot(RIGHT, 1.4)

    else:
        # If there is nothing in front of the robot it continus forwards
        driveRobot(FORWARDS, 0.1)


        
                

        # Now we'll check if there is open space here
        

    



    ###############################################################
    #                                                           A #
    #                                                           A #
    # |_________________________________________________________| #
    #                                                             #
    # This is the end of our loop,                                #
    # execution continus at the start of our loop                 #
    ###############################################################
    ###############################################################





# motor_serial has told us that its time to exit
# we have now exited the loop
# It's only polite to say goodbye
print("Goodbye")
