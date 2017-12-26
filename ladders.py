# Reza, TUM Informatics

import collections
import sys

def add_char_in_string(str, ch):
    return str + ch

def remove_char_from_string(str, ch):
    return str.replace(ch, "", 1) #Third argument is the number of occurences of ch in the string that has to be deleted

def heuristic_cost_estimate(current_node, goal_node):
    #print current_node , " " , goal_node
    listCurrent = collections.Counter(current_node);
    listGoal = collections.Counter(goal_node);
    listRemove = list((listCurrent - listGoal).elements()) #chars to be removed
    listAdd = list((listGoal - listCurrent).elements())    #chars can be added
    mergedList = listRemove + listAdd
    return len(mergedList)

def reconstruct_path(cameFrom, current, goal):
    total_path = [goal]
    while current in cameFrom:
        current = cameFrom[current]
        total_path.append(current)

    return total_path


def a_star_search(startword, goalword):
    word_dict = dict()
    closed_set = [] # The set of nodes already evaluated
    open_set = [startword]
    cameFrom = {}
    gScore = collections.defaultdict(lambda: 100000)
    fScore = {}
    gScore[startword] = 0 # The cost of going from start to start is zero.
    fScore[startword] = heuristic_cost_estimate(startword, goalword)
    open_set_val = [heuristic_cost_estimate(startword, goalword)]


    #read the file as a dictionary
    with open("wordList.txt") as file:
        for word in file:
            key = word.split()
            data = key[0]
            k = ''.join(sorted(data))
            word_dict[k] = data


    while True:
        if not open_set : break #if open_set is empty then break
        current_node = open_set.pop(0) # the node in open_set having the lowest fScore[] value
        open_set_val.pop(0)
       
        if(len(current_node) == len(goalword) and sorted(current_node) == sorted(goalword)):
            return reconstruct_path(cameFrom, current_node, goalword)

        closed_set.append(current_node)
        #check neighbour of current node
        #adding a-z
        for i in range(26 + len(current_node)):
            if(i>=26):
                neighbour = remove_char_from_string(current_node, current_node[i-26])
            else : 
                neighbour = add_char_in_string(current_node,chr(97+i))
            neighbour = ''.join(sorted(neighbour))

            if neighbour in word_dict: #this string is present in the dictionary
                actual_neighbour = word_dict[neighbour] #the actual word in the dictionary
                if(actual_neighbour in closed_set) : 
                    continue # Ignore the neighbor which is already evaluated.
                
                if(actual_neighbour not in open_set) : open_set.append(actual_neighbour) # Discover a new node

                tentative_gscore = gScore[current_node] + 1 #1 is the distance between the current_node and neighbour
                if(tentative_gscore >= gScore[actual_neighbour]):
                    continue #This is not a better path

                # This path is the best until now. Record it!
                cameFrom[actual_neighbour] = current_node
                gScore[actual_neighbour] = tentative_gscore
                fScore[actual_neighbour] = gScore[actual_neighbour] + heuristic_cost_estimate(actual_neighbour, goalword)
                open_set_val.append(fScore[actual_neighbour])


        #sort the open_set according to the fscore value
        if len(open_set_val) > 0 :
            open_set_val, open_set = (list(t) for t in zip(*sorted(zip(open_set_val, open_set))))
        #print open_set_val
        #print open_set

if __name__ == "__main__":
    ladder = a_star_search(sys.argv[1], sys.argv[2])
    ladder = list(reversed(ladder))
    file = open("output.txt", "w")
    for item in ladder:
        file.write("%s\n" %item)
