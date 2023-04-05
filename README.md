# **Spot the Differences**

This is an assignment of my Image Processing class. There are 2 tasks:
1. Generate an image with some difference from the original image.
2. Find the difference between 2 images and circle them.

## **Requirement**

This project was built and supported with [Python3.7](https://www.python.org/downloads/release/python-379).

Anyone is using a higher version of Python must downgrade version in order to run project 

Link download file model after training: [Model](https://drive.google.com/file/d/1Qhoa712WZGNe0QfIPoHS5sAfJBD1PQqd/view)

## **Setup**
1. Change directory to *GameData* folder:
    * `cd GameData`
2. Install requirements with command the following commands:
    * `pip install -r requirements.txt`
    * `pip install git+https://www.github.com/keras-team/keras-contrib.git`
3. Store the model in folder `/GameData/pix2pix/`
## **Task 1**
I code a function to generate an image with some difference from the original image. The python file is called `/GameData/GenerateData.py` file. 

Format code: `python GenerateData.py <type of generate technique>`

Python file requires 1 argument: the type of generate technique. There are 6 types of generate technique:
1. Rotate areas in an image.
2. Change color of areas in an image.
3. Add the existing images to the original image.
4. Use GAN model to generate the images to insert into the original image.
5. Change the brightness, contrast of the original image.
6. Mix the 5 types above.
 
## **Task 2**

I code a function to find the difference between 2 images and circle them. The python file is called `/SpotTheDifference/SpotDifference.py` file.

Format code: `python SpotDifference.py <type of option>`

Python file requires 1 argument: the type of option. There are 2 types of option:
1. Display two images without circle the differences.
2. Display two images with circle the differences.