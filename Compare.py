# compare.py

import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from SinglePersonTracking import getAngleList
from PercentError import compare_angle_lists

def calculate_dance_score(ref1_path, ref2_path):
    # Step 1: Get angle lists for Input A and Input B
    list1 = getAngleList(ref1_path)
    list2 = getAngleList(ref2_path)

    # Step 2: Pass through Dynamic Time Warping (DTW) Algorithm
    distance, path = fastdtw(np.array(list1), np.array(list2), dist=euclidean)

    # Step 3: Use Path to get aggregate Percent Error Difference per frame
    result = compare_angle_lists(list1, list2, path)
    percentErrorList, flaggedTimeStamps, danceScore = result

    # Assuming danceScore is the value you want to return
    return abs(100 - round(danceScore, 2))

if __name__ == "__main__":
    # Example usage
    ref1 = "Assets/RobotDance.mov"
    ref2 = "Assets/DanceTest.mp4"
    score = calculate_dance_score(ref1, ref2)
    print(f"Dance Score: {score}")
