import tensorflow as tf
import numpy as np
from scipy.misc import imresize
from scipy.ndimage.interpolation import shift
from imageio import imread
from PIL import Image
import os

def handle(data):
    #Convert to string
    data = data.decode("utf-8")
    #Create numpy array from string and reshape to 2D
    data = np.array(data.split('/'))
    if(data[1]=="a"):
      return 1
    elif(data[1]=="p"):
      return 2
    elif(data[1]=="d"):
      return 3
    elif(data[1]=="t"):
      return 4

def process_data(data, id, count):
    res = convert_image(data)
    #Read with PIL as greyscale and save
    img = Image.fromarray(res, 'L')
    path = "./static/temp/"+str(id)+"/"
    if not os.path.exists(path):
      os.makedirs(path)
    img.save(path+str(count)+".jpg")

def train(id, count, ground):
    dataset=read_dataset(id, count)
    if dataset.size == 0:
      return
    dataset /= 255
    ground = np.full((count), ground)
    model = tf.keras.models.load_model("./model/model_conv.h5")
    model.fit(dataset, ground, verbose=2)
    model.save("./model/model_conv.h5")
    delete(id, count, count)

  
def delete(id, count, num):
    #Loop through all images in temp folder for that session id and delete them
    for i in range(num):
        path="./static/temp/"+str(id)+"/"+str(count-i)+".jpg"
        os.remove(path)


def predict(data):
    res = convert_image(data)
    res = res/255
    res = res.reshape((1,28,28,1))
    model = tf.keras.models.load_model("./model/model_conv.h5")
    prediction = model.predict(res)
    return np.argmax(prediction)

def vis(image):
    img = Image.fromarray(image[0,:,:,0])
    img.show()

def read_dataset(id, count):
    #Create numpy array to store dataset
    img = np.zeros((28,28),dtype=int)
    dataset=np.zeros((count,28,28), dtype=float)

    #Loop through all images
    for x in range(count):
        path="./static/temp/"+str(id)+"/"+str(x+1)+".jpg"
        img = imread(path)
        dataset[x][:,:] = img
    dataset=dataset.reshape(count,28,28,1)
    return dataset

def convert_image(data):
    #Convert to string
    data = data.decode("utf-8")
    #Delete brackets at beginning and end
    data = data.replace("]", "")
    data = data.replace("[", "")
    #Create numpy array from string and reshape to 2D
    data = np.array(data.split('/'))
    data = np.fromstring(data[0], dtype=float, sep=',')
    data = data.reshape(500,500)
    #Reize and normalize to only 0s and 255s
    res = imresize(data, (20, 20), interp="cubic")
    res[res>0]=255
    #Find centroid and center drawing
    res=centroid(res)

    return res

def centroid(image):
  #Find indices where 255
  values=np.where(image==255)
  #Mean the indices to find centroid pixel
  mean_x=values[1].mean()
  mean_y=values[0].mean()
  #Calculate distance from center of 20x20 image
  move_x=int(round(9.5-mean_x))
  move_y=int(round(9.5-mean_y))
  #Pad with 4 zeros on each side to have a 28x28 image
  res = np.pad(image, 4, "constant", constant_values=(0, 0))
  #Shift rows and colums
  res = np.roll(res,move_x,axis=1)
  res = np.roll(res,move_y,axis=0)
  return res