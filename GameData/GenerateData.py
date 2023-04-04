from image.image_handle import convertImageMaker
import os
import glob
import random
import sys

files = glob.glob('./image/crop_images/*')
for f in files:
    os.remove(f)

convertTest=convertImageMaker()
convertTest.image_extract()
convertTest.image_save_crop_location()
convert_type = int(sys.argv[1])
convertTest.image_convert(convert_type)
#convert_type = 1: rotate crop an image 
#convert_type = 2: bitwise_not crop an image
#convert_type = 3: add_image
#convert_type = 4: use gan model to generate image
#convert_type = 5: change brightness and contrast of a crop image
# convertTest.image_convert(convert_type=random.randint(1,4))
