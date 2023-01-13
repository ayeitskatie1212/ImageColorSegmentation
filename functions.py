import numpy as np
import matplotlib.pyplot as plt
from skimage.util import img_as_float
from skimage import transform
from skimage import io
from skimage.measure import label
from skimage.segmentation import find_boundaries
import os
from PIL import Image
from scipy.spatial.distance import squareform, pdist, cdist

def outlineSegments(segments, n_clusters, H, W):
    enlargedSegments = np.copy(segments)
    enlargedSegments.resize((H, W))
    outline = np.full((H, W, 1), 255, dtype=int)
    print(enlargedSegments)
    plt.imshow(enlargedSegments)
    plt.axis('off')
    plt.show()
    for i in range(n_clusters):
        boolArea = np.where(enlargedSegments == i, 1, 0)
        connectedComponents, numCCs = label(boolArea, return_num=True, connectivity = 2)
        outlineShape = find_boundaries(boolArea, connectivity=2, mode='outer')
        outlineIndices = np.transpose((outlineShape == 1).nonzero())
        outline[outlineIndices[:, 0], outlineIndices[:, 1]] = 0
        
        
    return outline


def getAvgColors(img, segments, n_clusters):
    colors = []
    for i in range(n_clusters):
        colors.append( [np.mean(img[segments == i], axis=0)])
    colors = np.array(colors)
    return colors

def getGroups(img, segments, width, height, n_clusters, threshold, colors):
    for i in range(n_clusters): 
        boolArea = np.where(segments == i, 1, 0)
        connectedComponents, numCCs = label(boolArea, return_num=True, connectivity = 1) #skimage.measure.label
        targetColor = colors[i]
        print(numCCs)
        plt.imshow(connectedComponents)
        plt.axis('off')
        plt.show()
        for j in range(0, numCCs + 1): #for every connected component, check how many attached pixels they have.
            if (j % 100 == 0):
                print("I am at ", j, " out of ", numCCs, ".")
            currSum = np.sum(connectedComponents == j)
            if currSum < threshold:
                smallCCArea = np.where(connectedComponents == j, 1, 0)
                indicesForMerge = np.transpose((smallCCArea == 1).nonzero())
                
                #if currSum < 5:
#                     newGroup = i
#                     for index in indicesForMerge:
#                         if index[0] > 0 and segments[index[0]-1, index[1]] != i:
#                             newGroup = segments[index[0] - 1, index[1]]
#                             break
#                     segments[indicesForMerge[:, 0], indicesForMerge[:, 1]] = newGroup
                   
                    
                #else: 

                bestGroup = findBestNeighbor(img, smallCCArea, segments, targetColor, colors)
                segments[indicesForMerge[:, 0], indicesForMerge[:, 1]] = bestGroup
        print("This is iteration ", i, " out of ", n_clusters)          
                    
    return segments


def findBestNeighbor(img, smallCCArea, segments, targetColor, colors):
    edgeValues = find_boundaries(smallCCArea, connectivity=2, mode='outer')
    boundaryIndices = np.transpose((edgeValues == 1).nonzero())
    groupings = segments[boundaryIndices[:, 0], boundaryIndices[:, 1]]
    minDist = 500
    bestGroup = groupings[0]
    for group in groupings:
        currColor = colors[group]
        currDist = np.linalg.norm(targetColor - currColor)
        if currDist < minDist:
            midDist = currDist
            bestGroup = group
   
    return bestGroup 

def visualize_mean_color_image(img, segments):
    img = img_as_float(img)
    k = np.max(segments) + 1
    mean_color_img = np.zeros(img.shape)

    for i in range(k):
        mean_color = np.mean(img[segments == i], axis=0)
        mean_color_img[segments == i] = mean_color

    plt.imshow(mean_color_img)
    plt.axis('off')
    plt.show()
    return mean_color_img
    
    
    
# def kmeans(features, k, num_iters=100):
#     """ Use kmeans algorithm to group features into k clusters.

#     This function makes use of numpy functions and broadcasting to speed up the
#     first part(cluster assignment) of kmeans algorithm.

#     Args:
#         features - Array of N features vectors. Each row represents a feature
#             vector.
#         k - Number of clusters to form.
#         num_iters - Maximum number of iterations the algorithm will run.

#     Returns:
#         assignments - Array representing cluster assignment of each point.
#             (e.g. i-th point is assigned to cluster assignments[i])
#     """

#     N, D = features.shape

#     assert N >= k, 'Number of clusters cannot be greater than number of points'

#     # Randomly initalize cluster centers
#     idxs = np.random.choice(N, size=k, replace=False)
#     centers = features[idxs]
#     assignments = np.zeros(N, dtype=np.uint32)
    
#     print('SOMETHING IS HAPPENING IN THIS FKING FUNCTION')
#     for n in range(num_iters):
#         print(n)
#         distances = cdist(centers, features, metric='euclidean')
#         for i in range(N):
#             assignments[i] = np.argmin(distances[:, i])
 
#         oldCenters = np.copy(centers)
#         for j in range(k):
#             centers[j] = np.mean(features[assignments == j],axis=0)
#         if np.array_equal(oldCenters, centers):
#             break

#     return assignments




# def dfs(img, segments,j,i,width,height):
#     targetNum = segments[j, i]
#     todo = [(j,i)]
#     seen = set()
#     reachablePixels = []
#     while todo:
#         j,i = todo.pop()
#         seen.update((j, i))
#         if inBounds(j, i, width, height) and segments[j,i] == targetNum:
#             reachablePixels.append((j, i))
#             if ((j+1, i) not in seen):
#                 todo.append((j+1, i))
#             if ((j-1, i) not in seen):
#                 todo.append((j-1, i))
#             if ((j, i+1) not in seen):
#                 todo.append((j, i+1))
#             if ((j, i-1) not in seen):
#                 todo.append((j, i-1))
#             if ((j+1, i+1) not in seen):
#                 todo.append((j+1, i+1))
#             if ((j-1, i-1) not in seen):
#                 todo.append((j-1, i-1))
#             if ((j+1, i-1) not in seen):
#                 todo.append((j+1, i-1))
#             if ((j-1, i+1) not in seen):
#                 todo.append((j-1, i+1))
#     print(len(reachablePixels))
#     if len(reachablePixels < threshold):
#         merge(reachablePixels)
#     return reachablePixels


# def findSimilarColors(img, x, y, searched, threshold):
#     #Takes in an image, the selected x and y coordinates, and a threshold. 
#     #Finds all of the connected pixels of a similar color within the given threshold
#     unsearched = [(x, y)]
#     abc = 0
#     searched.update((x, y))
#     print(searched)
#     while abc < 10:#unsearched:
#         currX, currY = unsearched.pop()
#         searched.update((x,y))
#         print((x, y) in searched)
#         for i in range(-1, 2):
#             for j in range(-1, 2):
#                 checkSurroundingSquares(x + i, y + j, searched, unsearched)
#         print('searched:', searched)
#         print(unsearched)
#         abc += 1   
#     return img


# def mergeSmallGroups(img, segments, width, height):
#     completed = np.zeros((height, width))
#     for i in range(width):
#         for j in range(height):
#             if (completed[i][j] == 0):
#                 oneColorGroup = dfs(img, segments, j, i, width, height)
#                 for x, y in oneColorGroup:
#                     completed[x, y] = 1
                
#     return newSegments

# def inBounds(j, i, width, height):
#     if ((0 <= j < height) and (0 <= i < width)):
#         return True
#     return False

# def findClosestColorGroup(targetNum, groupsNearby):
#     mean_colors = {}
#     for group in groupsNearby:
#         mean_color = np.mean(img[segments == group], axis=0)
#         mean_colors[group] = mean_color
#     targetColor = np.mean(img[segments == targetNum], axis=0)
    
#     closestGroup = mean_colors.keys()[0]
#     minDist = 1000
#     targetR = targetColor[0]
#     targetG = targetColor[1]
#     targetB = targetColor[2]
#     for group in mean_colors.keys():
#         groupColor = mean_colors[group]
#         r = groupColor[0]
#         g = groupColor[1]
#         b = groupColor[2]
#         dist = ((targetR - r)**2 + (targetG - g)**2 + (targetB - b)**2)**.5
#         if dist < minDist:
#             minDist = dist
#             closestGroup = group
#     return closestGroup