from graph_search import bfs, dfs
from vc_metro import vc_metro
from vc_landmarks import vc_landmarks
from landmark_choices import landmark_choices



landmark_string = ""
for i, j in landmark_choices.items():
    landmark_string += "{0} - {1}\n".format(i, j) #The view object contains the key-value pairs of the dictionary, as tuples in a list.

#hypothetical situation of stations under construction 
stations_under_construction = ["Olympic Village"]

def greet():
    print("Hi there and welcome to Skyroute!")
    print("We help you find the sortest route between the following Vancouver landmarks: \n" + landmark_string)


def skyroute():
    greet()
    new_route()
    goodbye()




def set_start_and_end(start_point, end_point):
    if start_point != None:
        change_point = input("What would you like to change? Enter 'o' for 'origin', 'd' for 'destination' or 'b' for 'both': ")
        if change_point == "b":
            start_point = get_start()
            end_point = get_end()
        elif change_point == "o":
            start_point = get_start()
        elif change_point == "d":
            end_point = get_end()
        else:
            print("Try again!")
            set_start_and_end(start_point, end_point)
    else:
        start_point = get_start()
        end_point = get_end()
    
    return start_point, end_point

def get_start():
    user = input("Where are you coming from? Type in the corresponding letter: ")
    if user not in landmark_choices: 
        print("Sorry try again!")
        user = input("Where are you coming from? Type in the corresponding letter: ")
    start_point = landmark_choices[user]
    return start_point

def get_end():
    user = input("Where are you going to? Type in the corresponding letter: ") 
    if user not in landmark_choices:
        print("Sorry try again!")
        user = input("Where are you going to? Type in the corresponding letter: ") 
    end_point = landmark_choices[user]
    return end_point



def new_route(start_point=None, end_point=None):
    start_point, end_point=set_start_and_end(start_point, end_point)
    
    shortest_route = get_route(start_point, end_point)
    if shortest_route != None:
        shortest_route_string = "\n".join(shortest_route)
        print("The shortest metro route from {0} to {1} is:\n{2}".format(start_point, end_point, shortest_route_string))
    else:
        print("Unfortunately, there is currently no path between {0} and {1} due to maintenance.".format(start_point, end_point))
    again = input("Would you like to see another route? Enter y/n: ")
    if again == "y":
        show_landmark()
        new_route(start_point, end_point)

   
def get_route(start_point, end_point):
    start_stations = vc_landmarks[start_point]
    end_stations = vc_landmarks[end_point]
    routes = []
    for start in start_stations:
        for end in end_stations:
            if len(stations_under_construction) > 0:
                metro_sys = get_active_stations()
            else: metro_sys = vc_metro
            if len(stations_under_construction) > 0:
                possible_route = dfs(metro_sys, start, end)
                if not possible_route:
                    continue
            route = bfs(metro_sys, start, end)
            if route != None:
                routes.append(route)
    if routes:
        shortest_route = min(routes, key=len)
        return shortest_route
def show_landmark():
    see_landmarks = input("Would you like to see the list of landmarks again? Enter y/n: ")
    if see_landmarks == "y":
        print(landmark_string)

def get_active_stations():
    updated_metro = vc_metro
    for station in stations_under_construction:
        for the_station, neighbours in vc_metro.items():
            if the_station != station:
                updated_metro[the_station] -= set(stations_under_construction) 
            else:
                updated_metro[the_station] = set([])
    return updated_metro



def goodbye():
    print("Thanks for using SkyRoute!")

skyroute()
