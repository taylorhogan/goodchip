# Project GoodChip
![chip image](html_images/chip.jpeg)
![connection image](html_images/t0.svg)

There are billions of transistors in modern chips. It is the goal of the designer to make sure the connections between the transistors can be realized.
One of the metrics leading to a "good chip" is to reduce the number of crossings of these connections. Other metrics leading to better connections are component 
alignment, and connection density. 

## Training Data Repository
This directory contains two sets of a data. 
- A collection of images that show a set of components, pins and connections.  The best chips have fewer crossing connections. 
- A file that contains a list of filenames along with a label that represents the percentage of crossings
The code to generate new images, that are stastically similar to real chips is part of this package. Please use generator.py to create more images and 
The goal is to write a model that predicts the crossing percentage from the picture. 
The pictures are generated via a python script but statistically look like real chips. After the model is developed that demonstrates good correlation, more images can be generated.
It would be interesting to see how the correlation changes with the number of images in the training set.
If time permits 2 models could be trained on different image sets. If the two models match in prediction, then the confidence is high, otherwised the confidence is low in the prediction.
