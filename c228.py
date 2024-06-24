
import glob
import os
import sys
import time
import csv

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

actor_list = []
#define vehicle_control variable as list
vc=[]



#write the code of fuction by pressing ENTER end of this sentence to avoid indentation error.
reading = open('manual_control_data.csv', 'r')
reader=csv.reader(reading)
next(reader)
for row in reader:
    vc.append(row)

try:
    client = carla.Client('127.0.0.1', 2000)
    client.set_timeout(2.0)
    world = client.get_world()
    get_blueprint_of_world = world.get_blueprint_library()
    car_model = get_blueprint_of_world.filter('crossbike')[0]
    spawn_point = world.get_map().get_spawn_points()[1]
    dropped_vehicle = world.spawn_actor(car_model, spawn_point)


    simulator_camera_location_rotation = carla.Transform(spawn_point.location, spawn_point.rotation)
    simulator_camera_location_rotation.location += spawn_point.get_forward_vector() * 30
    simulator_camera_location_rotation.rotation.yaw += 180
    simulator_camera_view = world.get_spectator()
    simulator_camera_view.set_transform(simulator_camera_location_rotation)
    dropped_vehicle.set_transform(spawn_point)
    actor_list.append(dropped_vehicle)

    #write the code of fuction by pressing ENTER end of this sentence to avoid indentation error.
    def throttle_vehicle():
        for vc_data in vc:
            dropped_vehicle.apply_control(carla.VehicleControl(throttle=float(vc_data[2]),
                brake=float(vc_data[0]),
                steer=float(vc_data[3])))

            print(vc_data[2], vc_data[0], vc_data[3])
            time.sleep(15/1000)

    throttle_vehicle()

    time.sleep(1000)
finally:
    print('destroying actors')
    for actor in actor_list:
        actor.destroy()
    print('done.')