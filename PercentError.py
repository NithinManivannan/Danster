import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

leeway_Percentage = 15


def get_percent_error(inputA, inputB):

    temp = []

    for i in range(10):
        percentError = abs(((inputA[i] - inputB[i]) / inputA[i])) * 100
        temp.append(round(percentError, 3))

    return temp


def compare_angle_lists(coach_List, player_List, path):

    percent_error_list = []
    flagged_timestamps = []
    netAccuracy = 0

    #algorithm for comparing two node angle lists

    for i in range(len(path)):
        percent_error = get_percent_error(coach_List[path[i][0]], player_List[path[i][1]]) 
        percent_error_list.append(percent_error) 

        for j in range(len(percent_error)):

            netAccuracy += percent_error[j]

            if percent_error[j] >= leeway_Percentage:
                timestamp = j * 1/30 # check 30 to make sure its fps
                flagged_timestamps.append(round(timestamp, 3))

    netAccuracy = netAccuracy / (len(path) * 10)
    
    return [percent_error_list, flagged_timestamps, netAccuracy]