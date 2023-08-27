# Image Color Segmentation
This program uses kmeans clustering in order to reduce the numbers of colors in an image to a user-specified number. 

First, an image is passed in along with the number of colors the user would like to limit the output to. For this image, I limited the number of colors to 10.

![Hoover Tower](./testInputImages/hoover.jpg)

Next, using kmeans clustering, the pixels in the images are grouped into 10 groups depending on how similar they are in color. Here, you see all of the different groups visualized as a different color.

![Hoover Tower with Connected groups showing](./processImages/HooverCCs.png)



Here is another example of a converted image limited to 9 colors:
![An image of a train and sunflowers](./testInputImages/train.jpg)
![An image of a train and sunflowers converted into a cartoon rendition](./testOutputImages/trainThreshold9img.png)



Only using kmeans on the RGB values in the image leads to singular dots of different colors across the image. My goal is to have cohesive chunks of color. 
Therefore, after the kmeans is run, I peform an algorithm that finds all of the connected components (areas of a single color) of the new image. If a connected component has fewer pixels than a particular threshold, it will be absorbed by a nearby color. This gets rid of any small areas of a color. 

The output image of this process can then be converted to vector form and from there be applied to other areas, such as laser engraving. 
