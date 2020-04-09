###########################
# 6.00.2x Problem Set 1: Space Cows 

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    capacity = limit
    loaded_cows, transportation_list = [], [] # loaded_cows is a flattened version of transportation_list
    while len(loaded_cows) != len(cows.keys()): # while not all cows are loaded
        limit = capacity # reset limit to its full capacity in each trip
        checklist, candidate = [], [] # checklist records loaded cows in current trip, candidate record what cows are possible to be loaded in this trip
        for cow in cows.keys():
            if (cows[cow] <= limit) and (cow not in loaded_cows):
                candidate.append(cow)
        candidate.sort(reverse=True, key=lambda x: cows[x])
        if not candidate:
            break
        while limit >= cows[candidate[0]]:
            checklist.append(candidate[0])
            loaded_cows.append(candidate[0])
            limit -= cows[candidate[0]]

            candidate = []
            for cow in cows.keys():
                if (cows[cow] <= limit) and (cow not in loaded_cows):
                    candidate.append(cow)
            candidate.sort(reverse=True, key=lambda x: cows[x])
            if not candidate:
                break

        transportation_list.append(checklist)
    return transportation_list


# Problem 2
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    def check_weight(list_of_cows):
        weight = 0
        for cow in list_of_cows:
            weight += cows[cow]
        return weight

    for trip in get_partitions(cows.keys()):
        sanity_trip = list(map(check_weight, trip))
        flag = True
        for trip_weight in sanity_trip:
            if trip_weight > limit:
                flag = False
        if flag:
            res = trip
            break # detect optimal then
    return res

def check_weight(list_of_cows):
    weight = 0
    for cow in list_of_cows:
        weight += cows[cow]
    return weight

        
# Problem 3
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    cows = load_cows("ps1_cow_data.txt")
    start = time.time()
    ## code to be timed
    res=greedy_cow_transport(cows, limit=10)
    end = time.time()
    print("Greedy algorithm takes {0} trips and uses {1} seconds".format(len(res), end - start))

    start = time.time()
    ## code to be timed
    res = brute_force_cow_transport(cows, limit=10)
    end = time.time()
    print("Brue force algorithm takes {0} trips and uses {1} seconds".format(len(res), end - start))


"""
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

cows = load_cows("ps1_cow_data.txt")
limit=100
# cows = {'Luna': 41, 'Buttercup': 11, 'Starlight': 54, 'Betsy': 39}
# limit = 145
#print(cows)

print(greedy_cow_transport(cows, limit))
print(brute_force_cow_transport(cows, limit))
print(compare_cow_transport_algorithms())

