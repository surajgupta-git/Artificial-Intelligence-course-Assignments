#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: surgudla-sgaraga-bgogineni
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#
# !/usr/bin/env python3

#importing required libraries
import heapq
import math
import sys

#Function to read and load read and load the gps coordinates of all cities
def read_gps(filename):
    locs = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            ele = line.split()
            city = ele[0]
            lat = float(ele[1])
            long = float(ele[2])
            locs[city] = (lat, long)
    return locs

# function to read and load the details of segments between any 2 cities
def read_roadSegments(filename):
    roadSegments = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            roads = line.split()
            city1 = roads[0]
            city2 = roads[1]
            if not roadSegments.get(city1, None):
                roadSegments[city1] = {}
            if not roadSegments.get(city2, None):
                roadSegments[city2] = {}
            # Adding it both ways
            roadSegments[city1][city2] = (float(roads[2]), float(roads[3]), roads[4])
            roadSegments[city2][city1] = (float(roads[2]), float(roads[3]), roads[4])
    return roadSegments

roads,gps,approx_distance_cities = {},{},{}

roads = read_roadSegments("road-segments.txt")

gps = read_gps("city-gps.txt")

#function to calculate all the successor cities of a particular city
def successors(city):
    return roads[city].keys()

#function to calculate the haversine distance between 2 points - this will be used as heuristic function
def haversine_distance(coord1, coord2):
    latitude1,longitude1=coord1
    latitude2,longitude2=coord2
    lat1_radia = math.radians(latitude1)
    lat2_radia = math.radians(latitude2)
    diff_lat = math.radians(abs(latitude2 - latitude1))
    diff_lon = math.radians(abs(longitude2 - longitude1))
    ang = (math.pow((math.sin(diff_lat / 2.0)), 2)) + math.cos(lat1_radia) * math.cos(lat2_radia) * (math.pow((math.sin(diff_lon / 2.0)), 2))
    arc = 2.0 * (math.atan2(*(math.sqrt(ang), math.sqrt(1 - ang))))
    return (3958.756 * arc)**(1./3.)


def distance_cities(city1, city2):
    if city1 not in gps.keys() or city2 not in gps.keys():
        return 0
    city_pair = tuple(sorted((city1, city2)))
    return approx_distance_cities.get(city_pair,haversine_distance(gps[city1], gps[city2]))

#Evaluation Function to get the priority value of the fringe element
def get_priority_index(cost_function, end_city, present_state):
    route_covered, miles_covered, segments_covered, time_elapsed_covered, accidents_till_now = present_state
    current_city = route_covered[-1]
    distance_to_cover = distance_cities(current_city, end_city)
    if cost_function == "distance":
        return miles_covered + distance_to_cover
    if cost_function == "time":
        max_speed = 65 #assuming
        time_required_to_destination = distance_to_cover / max_speed
        return time_elapsed_covered + time_required_to_destination
    if cost_function=="safe":
        return accidents_till_now + (1/(10**6))*distance_cities(current_city, end_city)
    return segments_covered + 1

#Core function that finds the best route between 2 cities
def get_route(start_city, end_city, cost_function):
    fringe=[]
    route_covered = [start_city]
    visited = {}
    priority_index_when_visited = {}
    segments_covered, miles_covered, time_elapsed_covered,accidents_till_now = 0, 0, 0, 0
    initial_fringe_element = (route_covered, miles_covered, segments_covered, time_elapsed_covered,accidents_till_now)
    priority_index = get_priority_index(cost_function, end_city, initial_fringe_element)
    heapq.heappush(fringe, (priority_index, initial_fringe_element))
    while fringe:
        #popping the fringe element with highest priority
        priority_index, (route_covered, miles_covered, segments_covered, time_elapsed_covered,accidents_till_now) = heapq.heappop(fringe)
        source = route_covered[-1]
        if source == end_city:
            route_taken=[]
            templist = []
            templist1 = []
            for i in range(0, len(route_covered) - 1):
                key_list = []
                for key in roads.keys():
                    key_list.append(key)
                for m in range(0, len(key_list)):
                    if key_list[m] == route_covered[i]:
                        templist.append((roads[key_list[m]][route_covered[i + 1]]))
            for i in range(1,len(route_covered) ):
                templist1.append(route_covered[i])
            route_taken=[]
            for i in range(0,len(templist)):
                a=[]
                a.append(templist1[i])
                a.append(templist[i][2]+" for "+ str(int(templist[i][0])) + " miles" )
                route_taken.append(tuple(a))
            # the result route and other parameters will be returned
            return {"total-segments": len(route_taken),
                    "total-miles": miles_covered,
                    "total-hours": time_elapsed_covered,
                    "total-expected-accidents": accidents_till_now,
                    "route-taken": route_taken}
        # Mark the city as visited and note down the priority
        visited[source] = True
        priority_index_when_visited[source] = priority_index
        # Generate successors
        next_cities = successors(source)
        for city in next_cities:
            miles_to_city, speed_limit_on_highway, highway_name = roads[source][city]
            time_to_city = miles_to_city / speed_limit_on_highway
            if "I-" in highway_name :
                accidents_to_city=(2/(10**6))*miles_to_city
            else:
                accidents_to_city=(1/(10**6))*miles_to_city
            next_fringe_element = (route_covered + [city], miles_covered + miles_to_city, segments_covered + 1,time_elapsed_covered + time_to_city,accidents_till_now + accidents_to_city)
            priority_index = get_priority_index(cost_function, end_city, next_fringe_element)
            has_city_been_visited = visited.get(city, False)
            if has_city_been_visited and priority_index < priority_index_when_visited[city] and cost_function != "segments":
                visited[city] = False
                heapq.heappush(fringe, (priority_index, next_fringe_element))
            if not has_city_been_visited:
                heapq.heappush(fringe, (priority_index, next_fringe_element))
    return None

#Main function
# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))
    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "safe"):
        raise(Exception("Error: invalid cost function"))
    result = get_route(start_city, end_city, cost_function)
    #Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("Then go to %s via %s" % step)
    print("\n Total segments: %6d" % result["total-segments"])
    print("    Total miles: %10.3f" % result["total-miles"])
    print("    Total hours: %10.3f" % result["total-hours"])
    print("Total accidents: %15.8f" % result["total-expected-accidents"])
