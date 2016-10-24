#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal
from TestCoords import hideBlackBox, getPing
import time


#Set up option parsing to get connection string
import argparse
import Queue
import sys
import math


#Coordinates
right = -86.239092
left = -86.240807
top = 41.519441
bottom = 41.518968

#Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

def arm_and_takeoff(aTargetAltitude, vehicle):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)


    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print " Waiting for arming..."
        time.sleep(1)

    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
            print "Reached target altitude"
            break
        time.sleep(1)

def main(args):

    connection_string = args.connect
    delivery_string = args.delivery

    # Connect to the Vehicle
    print 'Connecting to vehicle on: %s' % connection_string
    vehicle = connect(connection_string, wait_ready=True)

    arm_and_takeoff(10, vehicle)

    print "Set default/target airspeed to 10"
    vehicle.airspeed = 10

    # fly to starting location
    takeOffPoint = (41.519165,-86.239902)
    vehicle.simple_goto( dronekit.LocationGlobalRelative(takeOffPoint.first,takeOffPoint.second,30))

    # Hide the black box
    hiddenCoords = hideBlackBox()
    hiddenSpot = LocationGlobal(hiddenCoords[0], hiddenCoords[1],hiddenCoords[2])

    print hiddenSpot

    def decreaseRange(curr):
        if curr == curr_top_right:
            direction = 'west'
            curr_topr = (curr_topr.first - (5/111111.),curr_topr.second - (5*math.cos(curr_topr.first))
            curr_top_right = dronekit.LocationGlobalRelative(curr_topr.first,curr_topr.second,30)
            return curr_top_right
        else if curr == curr_top_left:
            direction = 'south'
            curr_topl = (curr_topl.first - (5/111111.),curr_topl.second + (5*math.cos(curr_topl.first))
            curr_top_left = dronekit.LocationGlobalRelative(curr_topl.first,curr_topl.second,30)
            return curr_top_left
        else if curr == curr_bot_left:
            direction = 'east'
            curr_botl = (curr_botl.first + (5/111111.),curr_botl.second + (5*math.cos(curr_botl.first))
            curr_bot_left = dronekit.LocationGlobalRelative(curr_botl.first,curr_botl.second,30)
            return curr_bot_left
        else if curr == curr_bot_right:
            direction = 'north'
            curr_botr = (curr_botr.first - (5/111111.),curr_botr.second - (5*math.cos(curr_botr.first))
            curr_bot_right = dronekit.LocationGlobalRelative(curr_botr.first,curr_botr.second,30)
            return curr_bot_right
        else:
            print "Underlying assumption proven wrong"
            exit()

    def inRange(vehicle_local, ping_result,vehicle):
        a = (vehicle_local, ping_result)

        time.sleep(1)
        vehicle_obj = vehicle.location.global_frame
        vehicle_local = {'lat':vehicle_obj.lat,'lon':vehicle_obj.lon}

        b = (vehicle_local, getPing(vehicle_local))

        if direction == 'north':
            vehicle.simple_goto( dronekit.LocationGlobalRelative(float(vehicle_local['lat']),float(vehicle_local['lon'] - (1*math.cos( vehicle_local['lat'] ),30))))
            time.sleep(1)
            vehicle_obj = vehicle.location.global_frame
            vehicle_local = {'lat':vehicle_obj.lat,'lon':vehicle_obj.lon}
            c = (vehicle_local, getPing(vehicle_local))
        else if direction == 'south':
            vehicle.simple_goto( dronekit.LocationGlobalRelative(float(vehicle_local['lat']),float(vehicle_local['lon'] + (1*math.cos( vehicle_local['lat'] ),30))
            time.sleep(1)
            vehicle_obj = vehicle.location.global_frame
            vehicle_local = {'lat':vehicle_obj.lat,'lon':vehicle_obj.lon}
            c = (vehicle_local, getPing(vehicle_local))
        else if direction == 'east':
            vehicle.simple_goto( dronekit.LocationGlobalRelative(float(vehicle_local['lat'] + (1/111111.)),float(vehicle_local['lon']),30))
            time.sleep(1)
            vehicle_obj = vehicle.location.global_frame
            vehicle_local = {'lat':vehicle_obj.lat,'lon':vehicle_obj.lon}
            c = (vehicle_local, getPing(vehicle_local))
        else if direction == 'west':
            vehicle.simple_goto( dronekit.LocationGlobalRelative(float(vehicle_local['lat'] - (1/111111.)),float(vehicle_local['lon']),30))
            time.sleep(1)
            vehicle_obj = vehicle.location.global_frame
            vehicle_local = {'lat':vehicle_obj.lat,'lon':vehicle_obj.lon}
            c = (vehicle_local, getPing(vehicle_local))

        x = ( ( (a.second^2 - b.second^2) + (b.first['lat']^2 - a.first['lat']^2) + (b.first['lon']^2 - a.first['lon']^2) )*(2.*b.first['lon'] - 2.*c.first['lon']) )
        x = x - ( (b.second^2 - c.second^2) + (c.first['lat']^2 - b.first['lat']^2) + (c.first['lon']^2 - b.first['lon']) )*(2.*b.first['lon'] - 2.*a.first['lon'])
        x = x / ( (2.*b.first['lat'] - 2.*c.first['lat'])*(2.*b.first['lon'] - 2.*a.first['lon']) - (2.*a.first['lat'] - 2.*b.first['lat'])*(2.*c.first['lon'] - 2.*b.first['lon']) )

        y = ( (a.second^2 - b.second^2) + (b.first['lat']^2 - a.first['lat']^2) + (b.first['lon']^2 - a.first['lon']^2) + x*(2.*a.first['lat'] - 2.*b.first['lat']) )
        y = y / (2.*b.first['lon'] - 2.*a.first['lon'])

        final_target = dronekit.LocationGlobalRelative(x,y,30)
        while True:
            vehicle.simple_goto( final_target )
            vehicle_obj = vehicle.location.global_frame
            vehicle_local = {'lat':vehicle_obj.lat,'lon':vehicle_obj.lon}
            remainingDistance=get_distance_metres(vehicle_local,{'lat':x, 'lon':y})
            if remainingDistance<=targetDistance*0.01 or remainingDistance<=0.01: #Proximity of target
                vehicle.mode = VehicleMode("LAND")
    # search for vehicle
    q = Queue.Queue()
    curr_top_right = dronekit.LocationGlobalRelative(top,right,30)
    curr_top_left = dronekit.LocationGlobalRelative(top,left,30)
    curr_bot_right = dronekit.LocationGlobalRelative(bottom,right,30)
    curr_bot_left = dronekit.LocationGlobalRelative(bottom,left,30)

    q.put(curr_top_right)
    q.put(curr_top_left)
    q.put(curr_bot_left)
    q.put(curr_bot_right)

    direction = 'north'
    curr_topr = (top,right)
    curr_topl = (top,left)
    curr_botr = (bottom,right)
    curr_topl = (bottom,left)
    while vehicle.mode.name=="GUIDED": #Stop action if we are no longer in guided mode.
        vehicle_obj = vehicle.location.global_frame
        vehicle_local = {'lat':vehicle_obj.lat,'lon':vehicle_obj.lon}
        ping_result = getPing(vehicle_local)
        if ping_result != -1:
            inRange(vehicle_local, ping_result,vehicle)

        vehicle.simple_goto( dronekit.LocationGlobalRelative(float(targetLocation['lat']),float(targetLocation['lon']),30))
        vehicle_obj = vehicle.location.global_frame
        vehicle_local = {'lat':vehicle_obj.lat,'lon':vehicle_obj.lon}
        remainingDistance=get_distance_metres(vehicle_local,targetLocation)
        print('Remaining:', remainingDistance)
        if remainingDistance<=targetDistance*0.01 or remainingDistance<=0.01: #Proximity of target
            print "Reached target"
            if q.empty():
                break;
            currentLocation = targetLocation
            targ = q.get()
            q.put( decreaseRange(currentLocation) )
            prev_targ = currentLocation
            targetLocation = targ
            targetDistance = get_distance_metres(targetLocation,currentLocation)
            print('Total Distance:',targetDistance)
            continue;
        time.sleep(5)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
    parser.add_argument('--connect',
                       help="Vehicle connection target string. If not specified, SITL automatically started and used.")
    parser.add_argument('--delivery', help="directions for the drone to take to")
    args = parser.parse_args()

    main(args)
