# Image Color Segmentation
This program uses kmeans clustering in order to reduce the numbers of colors in an image to a user-specified number. 

Only using kmeans on the RGB values leads to singular dots of different colors across the image, whereas my goal is to have cohesive chunks. 
Therefore, after the kmeans is run, I peform an algorithm that finds all of the connected components (areas of a single color) of the new image. If a connected component has fewer pixels than a particular threshold, it will be absorbed by a nearby color. This gets rid of any small areas of a color. 

The output image of this process can then be converted to vector form and from there be applied to other areas, such as laser engraving. 
