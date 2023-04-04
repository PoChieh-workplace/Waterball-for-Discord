import io
from random import randint
import discord
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False
import numpy as np

# from PIL import Image

def pick_img(title:str):
       fig, ax = plt.subplots()
       i=randint(1,200)
       size = 0.2
       if i>=100 and i<150:
              vals = np.array([100,0])
              labels = '我覺得可以',' '
              outer_colors = ['#007500','#FFFFFF']
       elif i>=150:
              vals = np.array([100,0])
              labels = '我覺得不行',' '
              outer_colors = ['#D10000','#FFFFFF']
       else:
              vals = np.array([i,100-i])
              labels = '我覺得不行', '我覺得可以'
              outer_colors = ['#D10000','#007500']
       
       fig.patch.set_facecolor('#f2eadb')
       patches, texts = ax.pie(vals, radius=1,labels=labels, colors=outer_colors,
              wedgeprops=dict(width=size, edgecolor='w'))
       for k, patch in enumerate(patches):
              texts[k].set_color(patch.get_facecolor())
       ax.set_title(title, fontsize=25,color = '#004B97',fontweight = 600)
       ax.set_aspect("equal")
       plt.setp(texts, fontweight=600,fontsize = 15)

       with io.BytesIO() as image_binary:
             plt.savefig(image_binary,format='png', bbox_inches="tight")
             image_binary.seek(0)
             files= discord.File(fp=image_binary, filename='image.png')
             return (files,i)
