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

#This function finds the average color value for each connected component
def getAvgColors(img, segments, n_clusters):
    colors = []
    for i in range(n_clusters):
        colors.append( [np.mean(img[segments == i], axis=0)])
    colors = np.array(colors)
    return colors

#This is the main function of the program. It takes in the hyperparameters, segments the clusters into connected components, and processes through each CC until all the small ones are merged. 
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
                
             #This can be uncommented to speed up the process a bit. Essentially, on CCs smaller than 5 pixels, it will arbitrarily merge to the CC to the left (as opposed to searching for the closest color value nearby)
                
                #if currSum < 5:
#                     newGroup = i
#                     for index in indicesForMerge:
#                         if index[0] > 0 and segments[index[0]-1, index[1]] != i:
#                             newGroup = segments[index[0] - 1, index[1]]
#                             break
#                     segments[indicesForMerge[:, 0], indicesForMerge[:, 1]] = newGroup
                   
                   
                #else: #Remember to move the part below inside of the else statement

                bestGroup = findBestNeighbor(img, smallCCArea, segments, targetColor, colors)
                segments[indicesForMerge[:, 0], indicesForMerge[:, 1]] = bestGroup
        print("This is iteration ", i, " out of ", n_clusters)          
                    
    return segments

#This function is used when a Connected Component is too small to be included in the final image. It searches all of the neighboring connected components, finds the neighbor with the most similar color, and merges the smaller connected component into it. 
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


#This function takes the average color of a kmeans cluster and visualizes the image using that average color. 
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