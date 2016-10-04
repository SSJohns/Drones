import random
from dronekit import LocationGlobal
#Coordinates
right = -86.239092
left = -86.240807
top = 41.519441
bottom = 41.518968
#***********************************************************************************************************************
# Generate coordinates for the black box
#***********************************************************************************************************************
def hideBlackBox():
    mRight = right * 1000000
    mLeft = left*1000000
    mTop = top * 1000000
    mBottom = bottom * 1000000
 

    verticalRange = mTop-mBottom
    horizontalRange = mLeft-mRight

    # Create latitude
    i=0
    randNum = random.random()
    verticalOffSet = randNum* verticalRange
    newLatitude = (mBottom+verticalOffSet)/1000000
    newLatitude = '%.6f'%(newLatitude)
    
    # Create longitude
    randNum = random.random()
    horizontalOffSet = randNum* horizontalRange
    newLongitude = (mLeft-horizontalOffSet)/1000000
    newLongitude = '%.6f'%(newLongitude)

    return (newLatitude, newLongitude,0)

# Hide the black box
# hiddenCoords = hideBlackBox()
# hiddenSpot = LocationGlobal(hiddenCoords[0], hiddenCoords[1],hiddenCoords[2])
# print hiddenSpot

#***********************************************************************************************************************
# Ping
# Assumes that you have setup a visible LocationGlobal variable called hiddenSpot
# Returns -1 (i.e. silence) if the vehicle is more than 5 meters away
# Otherwise returns the distance in meters.
#***********************************************************************************************************************

def get_distance_metres(aLocation1, aLocation2):
    dlat = float(aLocation2['lat']) - float(aLocation1['lat'])
    dlong = float(aLocation2['lon']) - float(aLocation1['lon'])
    return math.sqrt((dlat*dlat) + (dlong*dlong) * 1.113195e5)

def getPing(currentLocation):
    distance= get_distance_metres(currentLocation,hiddenSpot)
    if distance > 5:
        return -1
    else:
        return distance

