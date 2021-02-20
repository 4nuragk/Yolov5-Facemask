import time
import subprocess

from io import BytesIO
import numpy as np
from PIL import Image


def cmd(command):
    subp = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
    subp.wait(100)
    if subp.poll() == 0:
        print(subp.communicate()[0])
    else:
        print("..")


def read_imagefile(file) -> Image.Image:

    image = Image.open(BytesIO(file))
    return image


def predict(mycmd):  
    result = cmd(mycmd)
    return result 
