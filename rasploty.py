import sys
import RPi.GPIO as gpio
import time
import math

#Setup the hardware information
#------------------------------------------------------------------------
#------------------------------------------------------------------------
motorWidth = 72

# Pen position information
positionX = 36
positionY = 36

# Spool information
diameter = 2
outline = diameter * 3.14

#Setup the raspberry pi's GPIOs
#------------------------------------------------------------------------
#------------------------------------------------------------------------
#use the broadcom layout for the gpio
gpio.setmode(gpio.BCM)
#GPIO17 and GPIO23 = Direction
#GPIO22 and GPIO24 = Step

gpio.setup(17, gpio.OUT)
gpio.setup(22, gpio.OUT)
gpio.setup(23, gpio.OUT)
gpio.setup(24, gpio.OUT)
#------------------------------------------------------------------------
#------------------------------------------------------------------------



#Set direction of rotation
#------------------------------------------------------------------------
#------------------------------------------------------------------------
#set the direction equal to the appropriate gpio pin
gpio.output(23, True)
gpio.output(17, False)
#------------------------------------------------------------------------
#------------------------------------------------------------------------


def drawLine(x,y):
    global positionX
    global positionY
    global motorWidth
    global outline

    xNow = positionX
    yNow = positionY

    xFuture = x
    yFuture = y

    xSteps = (xFuture - positionX) / 10
    ySteps = (yFuture - positionY) / 10

    for i in range(1,11):
        print(i, xSteps, x + (xSteps*i), positionX, positionY)
        goToPos(xNow + (xSteps*i), yNow + (ySteps*i))

def goToPos(x,y):
    global positionX
    global positionY
    global motorWidth
    global outline

    xNow = positionX
    yNow = positionY
    x2Now = motorWidth - xNow

    x = x
    x2 = motorWidth - x
    y = y

    # Check thread length
    threadLeftNow = math.sqrt((xNow * xNow) + (yNow * yNow))
    threadRightNow = math.sqrt((x2Now * x2Now) + (yNow * yNow))

    # Check new thread length
    threadLeftFuture = math.sqrt((x * x) + (y * y))
    threadRightFuture = math.sqrt((x2 * x2) + (y * y))

    #STEPS necessary
    stepOutline = outline / 1600

    # determine if it has to pull up or down
    if threadLeftFuture < threadLeftNow:
        gpio.output(23, False)
        totalStepsLeft = math.floor((threadLeftNow - threadLeftFuture) / stepOutline)
    else:
        gpio.output(23, True)
        totalStepsLeft = math.floor((threadLeftFuture - threadLeftNow) / stepOutline)

    if threadRightFuture < threadRightNow:
        gpio.output(17, True)
        totalStepsRight = math.floor((threadRightNow - threadRightFuture) / stepOutline)
    else:
        gpio.output(17, False)
        totalStepsRight = math.floor((threadRightFuture - threadRightNow) / stepOutline)

    #EXECUTE
    #track the number of steps taken
    StepCounterLeft = 0
    StepCounterRight = 0

    #waittime controls speed
    WaitTime = 0.001
    timePassed = 0.001
    drawLine = False

    #totalAction time
    if totalStepsLeft > totalStepsRight:
        totalTime = totalStepsLeft * WaitTime
    else:
        totalTime = totalStepsRight * WaitTime

    while drawLine == False:
        stepperLeftEnd = False
        stepperRightEnd = False

        procesPercentage = timePassed / totalTime
        stepsLeftNow = math.floor(totalStepsLeft * procesPercentage)
        stepsRightNow = math.floor(totalStepsRight * procesPercentage)

        while StepCounterLeft < stepsLeftNow:
            gpio.output(24, True)
            gpio.output(24, False)
            StepCounterLeft += 1

        while StepCounterRight < stepsRightNow:
            gpio.output(22, True)
            gpio.output(22, False)
            StepCounterRight += 1

        if StepCounterRight == totalStepsRight and StepCounterLeft == totalStepsLeft:
            drawLine = True

        timePassed += WaitTime
        time.sleep(WaitTime)

    # save new position
    positionX = x
    positionY = y

    return True

links = True
drawLine(18,20)

for i in range(1,80):
    if links == True:
        drawLine(54,20+i)
        drawLine(54,20+i+1)
        links = False
    else:
        drawLine(18,20+i)
        drawLine(18,20+i+1)
        links = True

drawLine(36,36)

# drawLine(27,36)
# drawLine(27,50)
# drawLine(18,50)
# drawLine(18,36)
# drawLine(18,50)
# drawLine(36,50)
# drawLine(36,36)
# drawLine(36,50)
# drawLine(41,50)
# drawLine(41,36)
# drawLine(47,36)
# drawLine(47,43)
# drawLine(41,43)
# drawLine(47,50)
# drawLine(54,50)
# drawLine(54,43)
# drawLine(48,43)
# drawLine(48,36)
# drawLine(54,36)
# drawLine(54,20)
# drawLine(36,20)
#
# time.sleep(20)
#
# drawLine(36,36)


gpio.cleanup()
