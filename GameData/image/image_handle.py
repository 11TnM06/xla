import cv2
import os
from pix2pix.pix2pix import *
import random
class convertImageMaker:
  def __init__(self):
    self.box=[]
    self.abs_dir="./result_images"
    self.crop_location=str()
    self.convert_type=int()
    self.original_dir=""
    pass

  def image_extract(self):
    original_dir = 'image/result_images/original_image.jpg'
    self.original_dir=original_dir
    print(original_dir)
    img_ori = cv2.imread(original_dir, cv2.IMREAD_COLOR)
    
    # print(img_ori)
    img = img_ori.copy()
    # img.resize(img, (1200, 500))
    # cv2.imshow("img", img)
    # cv2.waitKey()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
    img_canny = cv2.Canny(img_blur, 100, 200)
    #img_ori = cv2.resize(img_ori, (1200, 500))
    contours, hierarchy = cv2.findContours(img_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(contours)):
      cnt = contours[i]
      if i != len(contours) - 1:
        cnt2 = contours[i + 1]
        x2, y2, w2, h2 = cv2.boundingRect(cnt2)
        rect_area2 = w2 * h2  # area size
      x, y, w, h = cv2.boundingRect(cnt)
      rect_area = w * h  # area size
      aspect_ratio = float(w) / h  # ratio = width/height
      if (aspect_ratio >= 0.01) and (aspect_ratio <= 10000.0) and (rect_area >= 500) and (rect_area <= 10000):
        if (0 <= abs(rect_area - rect_area2)) and (abs(rect_area - rect_area2) <= 20):
          cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
          self.box.append(cv2.boundingRect(cnt))
    # cv2.imshow("img", img)
    # cv2.waitKey()
    for i in range(len(self.box)):  # Buble Sort on python
      for j in range(len(self.box) - (i + 1)):
        if self.box[j][0] > self.box[j + 1][0]:
          temp = self.box[j]
          self.box[j] = self.box[j + 1]
          self.box[j + 1] = temp
          pass
        pass
      pass
    print(len(self.box))
  def image_save_crop_location(self):
    crop_list = []
    img_ori = cv2.imread(self.original_dir, cv2.IMREAD_COLOR)
    img_cut = img_ori.copy()
    img_cut2 = img_ori.copy()
    crop_dir = './image/crop_images'
    crop_text = open(os.path.join(crop_dir, "crop_location.txt"), 'w')
    for i in range(len(self.box)):
      crop_img = img_ori[self.box[i][1]:self.box[i][1] + self.box[i][3], self.box[i][0]:self.box[i][0] + self.box[i][2]]
      data = str(self.box[i][1]) + " " + str(self.box[i][3]) + " " + str(self.box[i][0]) + " " + str(self.box[i][2]) + "\n"
      crop_text.write(data)
      crop_list.append(crop_img)
      cv2.imwrite(os.path.join(crop_dir, "crop_" + str(i) + ".jpg"), crop_img)
      img_cut[self.box[i][1]:self.box[i][1] + self.box[i][3], self.box[i][0]:self.box[i][0] + self.box[i][2]] = 0
      img_cut2[self.box[i][1]:self.box[i][1] + self.box[i][3], self.box[i][0]:self.box[i][0] + self.box[i][2]] = 255
      cv2.imwrite(os.path.join(crop_dir, "cut_image1.jpg"), img_cut)
      cv2.imwrite(os.path.join(crop_dir, "cut_image2.jpg"), img_cut2)
      pass
    crop_text.close()
    self.crop_location=os.path.join(crop_dir, "crop_location.txt")
  def get_rotation(self, dir, lines, img_cut1, item):
    if os.path.isfile(dir + item) and ".jpg" in item and "crop" in item:
      item_index = item.replace("crop_", "")
      item_index = int(item_index.replace(".jpg", ""))
      img_paste = cv2.imread(dir + item, cv2.IMREAD_COLOR)
      height, width, channel = img_paste.shape
      matrix = cv2.getRotationMatrix2D((width / 2, height / 2), 180, 1)
      dst = cv2.warpAffine(img_paste, matrix, (width, height))

      crop_location = lines[item_index].split()
      crop_location = list(map(int, crop_location))
      img_cut1[crop_location[0]:crop_location[0] + crop_location[1],
      crop_location[2]:crop_location[2] + crop_location[3]] = dst
      pass
    return img_cut1
  def bitwise_image(self, dir, lines, img_cut1, item):
    if os.path.isfile(dir + item) and ".jpg" in item and "crop" in item:
      # print(item)
      item_index = item.replace("crop_", "")
      item_index = int(item_index.replace(".jpg", ""))
      img_paste = cv2.imread(dir + item, cv2.IMREAD_COLOR)
      dst = cv2.bitwise_not(img_paste)
      crop_location = lines[item_index].split()
      crop_location = list(map(int, crop_location))

      # print(crop_location)
      # print(img_paste.shape)
      # print(crop_location[0], crop_location[0] + crop_location[1], crop_location[2], crop_location[2] + crop_location[3])
      img_cut1[crop_location[0]:crop_location[0] + crop_location[1],
      crop_location[2]:crop_location[2] + crop_location[3]] = dst
      pass
    return img_cut1
  def add_image(self, dir, lines, img_ori, item):
    if os.path.isfile(os.path.join(dir, item)) and ".jpg" in item:
      item_index = item.replace(".jpg", "")

      crop_location = lines[item_index].split()
      crop_location = list(map(int, crop_location))
      item = cv2.resize(item, dsize=(crop_location[3], crop_location[1]),interpolation=cv2.INTER_AREA)
      y_offset = crop_location[0]
      x_offset = crop_location[2]
      y1, y2 = y_offset, y_offset + item.shape[0]
      x1, x2 = x_offset, x_offset + item.shape[1]
      alpha_s = item[:, :, 2] / 255.0
      alpha_l = 1.0 - alpha_s
      for c in range(0, 3):
        img_ori[y1:y2, x1:x2, c] = (alpha_s * item[:, :, c] + alpha_l * img_ori[y1:y2, x1:x2, c])
        pass
    return img_ori
  
  def do_gan(self, dir, lines, img_cut1, item):
    if os.path.isfile(os.path.join(dir, item)) and ".jpg" in item and "crop" in item:
      #print(item)
      item_index = item.replace("crop_", "")
      item_index = int(item_index.replace(".jpg", ""))
      img_paste = cv2.imread(os.path.join(dir, item), cv2.IMREAD_COLOR)
      #item_index >= len(lines)
      if item_index < len(lines):
        crop_location = lines[item_index].split()
        crop_location = list(map(int, crop_location))
        img_cut1[crop_location[0]:crop_location[0] + crop_location[1],
        crop_location[2]:crop_location[2] + crop_location[3]] = img_paste
    pass
  def change_quality(self, dir, lines, img_cut1, item):
    if os.path.isfile(dir + item) and ".jpg" in item and "crop" in item:
      # print(item)
      item_index = item.replace("crop_", "")
      item_index = int(item_index.replace(".jpg", ""))
      img_paste = cv2.imread(dir + item, cv2.IMREAD_COLOR)
      alpha = random.uniform(0.5, 1.5)
      beta = random.randint(-100, 100)
      dst = cv2.convertScaleAbs(img_paste, alpha=alpha, beta=beta)
      crop_location = lines[item_index].split()
      crop_location = list(map(int, crop_location))
      img_cut1[crop_location[0]:crop_location[0] + crop_location[1],
      crop_location[2]:crop_location[2] + crop_location[3]] = dst
      pass
    return img_cut1
  def save_image(self, image, width, height):
    dst2 = cv2.resize(image, dsize=(width, height), fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imwrite(os.path.join("./image/result_images/converted_image.jpg"), dst2)
  def image_convert(self, convert_type):
    dir = 'image/crop_images/'
    img_ori = cv2.imread(self.original_dir, cv2.IMREAD_COLOR)
    img_cut1 = cv2.imread(os.path.join(dir, "cut_image1.jpg"), cv2.IMREAD_COLOR)
    crop_text = open(os.path.join(dir, "crop_location.txt"), 'r')
    height_ori, width_ori, channel_ori = img_ori.shape
    lines = crop_text.readlines()
    if convert_type == 1:
      dirs = os.listdir(dir)
      for item in dirs:
        img_cut1 = self.get_rotation(dir, lines, img_cut1, item)
      self.save_image(img_cut1, width_ori, height_ori)
      pass
    elif convert_type == 2:
      dirs = os.listdir(dir)
      for item in dirs:
        self.bitwise_image(dir, lines, img_cut1, item)
        pass
      self.save_image(img_cut1, width_ori, height_ori)
      pass
    elif convert_type == 3:
      img_ori = cv2.imread(os.path.join("image/result_images/original_image.jpg"), cv2.IMREAD_COLOR)
      dir_addImage = './image/clean_back'
      dirs_addImage = os.listdir(dir)
      print(os.path.join(dir, "apple.png"))
      for item in dirs:
        img_ori = self.add_image(dir, lines, img_ori, item)
        pass
      self.save_image(img_ori, width_ori, height_ori)
      pass

    # GAN, pix2pix
    elif convert_type == 4:
      print("Start GAN")
      pix = pixStart()
      pix.start()
      dir = './pix2pix/datasets/tmp/saved'
      dirs = os.listdir(dir)
      for item in dirs:
        #print(item)
        self.do_gan(dir, lines, img_cut1, item)
        pass
      self.save_image(img_cut1, width_ori, height_ori)
      print("Done")
      pass
    # Change contrast, brightness
    elif convert_type == 5:
      dirs = os.listdir(dir)
      for item in dirs:
        img_cut1 = self.change_quality(dir, lines, img_cut1, item)
        pass
      self.save_image(img_cut1, width_ori, height_ori)   
      pass
    # Mix
    elif convert_type == 6:
      dirs = os.listdir(dir)
      crop_text = open(os.path.join(dir, "crop_location.txt"), 'r')
      pix = pixStart()
      pix.start()
      dir_gan = './pix2pix/datasets/tmp/saved'

      dir_addImage = './image/clean_back'
      item_addImage = os.listdir(dir_addImage)
      img_ori = cv2.imread(os.path.join("image/result_images/original_image.jpg"), cv2.IMREAD_COLOR)
      res = 0

      for item_gan in os.listdir(dir_gan):
        option = random.randint(5, 5)
        #print(item)
        if option == 1:
          #do get_rotation
          if res >= len(item_addImage):
            continue
          img_cut1 = self.get_rotation(dir, lines, img_cut1, dirs[res])
        elif option == 2:
          #do bitwise_image
          if res >= len(item_addImage):
            continue
          self.bitwise_image(dir, lines, img_cut1, dirs[res])
          pass
        elif option == 3:
          if res >= len(item_addImage):
            continue
          img_ori = self.add_image(dir_addImage, lines, img_ori, item_addImage[res])
          self.save_image(img_ori, width_ori, height_ori)
          pass
        elif option == 4:
          #print(item_gan[res])
          self.do_gan(dir_gan, lines, img_cut1, item_gan)
        elif option == 5:
          if res >= len(item_addImage):
            continue
          img_cut1 = self.change_quality(dir, lines, img_cut1, dirs[res])
        else:
          pass
        res = res + 1
      self.save_image(img_cut1, width_ori, height_ori)
      pass

    pass