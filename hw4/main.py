from Paris import *
import UpdateJSON
from dronekit import LocationGlobalRelative

def get_close_box(boxes, location):
    lat = location[0]
    lon = location[1]
    drone_loc = {'lat':lat, 'lon':lon}
    min_dist = sys.float_info.max
    box = ''
    for tup in boxes:
        # print tup[1], tup[2]
        tup_loc = {'lat':tup[1], 'lon':tup[2]}
        tup_dist = get_distance_metres(tup_loc, drone_loc)
        # print tup_dist
        if tup_dist < min_dist:
            # print 'Min'
            box = tup
            min_dist = tup_dist
    return box, location[2], tup_dist

def main():
    # Generate 100 jobs
    deliveryJobs = []
    for jobNum in range(0, 100):
        job = deliveryRequest(jobNum)
        deliveryJobs.append(job);
        jobName = "Job" + str(job.getJobID())
        #Show starting coordinates.
        UpdateJSON.updateMapCoordinateData(jobName, job.getStart().lat, job.getStart().lon)
    UpdateJSON.generateNewFile()

    #***********************************************************************************************************************
    # Figure out the route that the drones should take
    #***********************************************************************************************************************
    recharge_stations = [('station1',48.864446, 2.325283),('station2',48.858093, 2.296604),('station3',48.846185, 2.346708)]

    drones = []

    for i in range(0,5):
        stri = str(i)
        drones.append({
            'id':stri,
            'loc': [48.858093, 2.296604, i * 10 + 30],
            'battery': 25,
            'speed': 20,
            'dist':0
        })
    for i in range(5, 10):
        stri = str(i)
        drones.append({
            'id':stri,
            'loc': [48.858093, 2.296604, i * 10 + 30],
            'battery': 25,
            'speed': 20,
            'dist': 0
        })
    data = list(UpdateJSON.getFile())
    # for tup in data:
    #     print tup

    # drones take off
    for drone in drones:
        drone['battery'] -= 0.5
    i = 0
    j = 1
    with open("routes.js", "a") as tempRouteFile:
        tempRouteFile.write('batch = [')
        while data != []:
            tempRouteFile.write('[')
            for drone in drones:
                point, alt, dist = get_close_box(data, drone['loc'])
                drone['loc'] = (point[1], point[2], alt)
                drone['battery'] -= (dist*0.001 + 0.5)
                drone['dist'] += dist

                tempRouteFile.write('{"droneID":"')
                tempRouteFile.write(drone['id'])
                tempRouteFile.write('","lat":"')
                tempRouteFile.write(str(point[1]))
                tempRouteFile.write('","lon":"')
                tempRouteFile.write(str(point[2]))
                tempRouteFile.write('","alt":"')
                tempRouteFile.write(str(alt))
                tempRouteFile.write('"}')
                tempRouteFile.write(',')
                charge_p, alt, charge_dist = get_close_box(recharge_stations, drone['loc'])
                print 'To charge', charge_dist, charge_p
                if (charge_dist*0.001 + 5) >= drone['battery']:
                    print 'Charged up'
                    # drone['dist'] += charge_dist
                    drone['loc'] = (charge_p[1], charge_p[2], alt)
                    drone['battery'] = 24.5
                # print point
                # print drone
                # print dist
                data.remove(point)
                if point in data:
                    import ipdb; ipdb.set_trace()
                # print len(data)
                i += 1
                j += 1
            tempRouteFile.write('],')
        tempRouteFile.write(']')
        for d in drones:
            print d['id'], d['dist']
        import ipdb; ipdb.set_trace()
        print 'Done', i

if __name__ == '__init__':
    main()
