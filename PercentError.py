import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

# Assume leeway_Percentage is set higher to ignore minor discrepancies
leeway_Percentage = 100  # Increase this value to consider only larger errors

def get_percent_error(inputA, inputB):
    temp = []
    for i in range(len(inputA)):
        percentError = abs((inputA[i] - inputB[i]) / inputA[i]) * 100 if inputA[i] != 0 else 0
        temp.append(round(percentError, 3))
    return temp

def compare_angle_lists(coach_List, player_List, path, fps=30):
    percent_error_list = []
    flagged_timestamps = []
    netAccuracy = 0

    for index_pair in path:
        index1, index2 = index_pair
        percent_error = get_percent_error(coach_List[index1], player_List[index2])
        percent_error_list.append(percent_error)

        # Process each joint error and check against the dynamic/raised threshold
        for j, error in enumerate(percent_error):
            netAccuracy += error
            if error >= leeway_Percentage:
                timestamp = index1 / fps  # Calculate the timestamp using fps
                flagged_timestamps.append(round(timestamp, 3))

    netAccuracy = netAccuracy / (len(path) * 10)
    return percent_error_list, flagged_timestamps, netAccuracy
