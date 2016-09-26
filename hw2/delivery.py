#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
© Copyright 2015-2016, 3D Robotics.
simple_goto.py: GUIDED mode "simple goto" example (Copter Only)

Demonstrates how to arm and takeoff in Copter and how to navigate to points using Vehicle.simple_goto.

Full documentation is provided at http://python.dronekit.io/examples/simple_goto.html
"""

from dronekit import connect, VehicleMode, LocationGlobalRelative
import time


#Set up option parsing to get connection string
import argparse  
import Queue
import sys
import math
import dronekit
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect', 
                   help="Vehicle connection target string. If not specified, SITL automatically started and used.")
parser.add_argument('--delivery', help="directions for the drone to take to")
args = parser.parse_args()

connection_string = args.connect
delivery_string = args.delivery

#Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % connection_string
vehicle = connect(connection_string, wait_ready=True)


def arm_and_takeoff(aTargetAltitude):
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


def get_distance_metres(aLocation1, aLocation2):
    dlat = float(aLocation2['lat']) - float(aLocation1['lat'])
    dlong = float(aLocation2['lon']) - float(aLocation1['lon'])
    return math.sqrt((dlat*dlat) + (dlong*dlong) * 1.113195e5)

def dfs_cycle(G, start, q):
    temp_g = {}
    visited = {}
    for keys in G:
        temp_g[keys] = G[keys]
        visited[keys] = False
    path_distances = dict()
    start_node = G[start]
    del temp_g[start]
    min_dist = sys.maxint
    next = ''
    print('Planned route is as follows: ')
    visited.pop(start, 0)
    while visited:
        for node in visited:
            if node is start:
                continue
            dist_local = get_distance_metres(start_node,G[node])
            if dist_local < min_dist:
                next = node
        visited.pop(next, 0)
        print(next)
        start_node = G[next]
        min_dist = sys.maxint
        q.put( (G[next],next) )
    print(start)
    q.put(G[start])

def greedy_grab_locations(points):
    q = Queue.Queue()
    graph = dict()

    start = points[0]
    for point in points:
        graph[point[0]] = {'lat':point[len(point)-2], 'lon':point[len(point)-1]}
    dfs_cycle(graph, start[0], q)
    return q, graph, graph[start[0]], start[0]

orders = []
with open(delivery_string, 'rb') as f:
    for line in f:
        order = line.rstrip().split(', ')
        orders.append(order)



arm_and_takeoff(30)

print "Set default/target airspeed to 10"
vehicle.airspeed = 10

q, graph, targetLocation, begin = greedy_grab_locations(orders)
currentLocation = vehicle.location.global_frame
currentLocation = {'lat':currentLocation.lat, 'lon':currentLocation.lon}
targetDistance = get_distance_metres(targetLocation,currentLocation)

print 'Delivering to', begin, targetLocation

while vehicle.mode.name=="GUIDED": #Stop action if we are no longer in guided mode.
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
        targ= q.get()
        targetLocation = targ.first
        name = targ.second
        print 'Delivering to', name, targetLocation
        targetDistance = get_distance_metres(targetLocation,currentLocation)
        print('Total Distance:',targetDistance)
        continue;
    time.sleep(5)

# sleep so we can see the change in map
time.sleep(30)

print "Returning to Launch"
vehicle.mode = VehicleMode("RTL")

#Close vehicle object before exiting script
print "Close vehicle object"
vehicle.close()

# Shut down simulator if it was started.
if sitl is not None:
    sitl.stop()
