import io
import discord
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False
import numpy as np

# from PIL import Image


def friend_exp_img(o:int,edit:int,up_limit:int):
    if o<0:o=0
    title = "親密度"
    labels = ' ',f'{edit:+d}',' '
    if edit>=0:
        outer_colors= ['#7878FF','#007500','#FFFFFF']
        if o+edit>=up_limit:outer_colors=['#FFCF78','#FFCF78','#FFCF78']
        vals = np.array([o,edit,up_limit-o-edit])
    else:    
        outer_colors= ['#7878FF','#D10000','#FFFFFF']
        if o+edit<=0:vals = np.array([0,o,up_limit-o])
        else:vals = np.array([o+edit,-(edit),up_limit-o])
    fig, ax = plt.subplots()
    size = 0.1
    fig.patch.set_facecolor('#f2eadb')
    patches, texts = ax.pie(vals, radius=1,labels=labels, colors=outer_colors,
            wedgeprops=dict(width=size, edgecolor='black'))
    for k, patch in enumerate(patches):
            texts[k].set_color(patch.get_facecolor())
    ax.set_title(title, fontsize=25,color = '#004B97',fontweight = 600)
    ax.set_aspect("equal")
    plt.setp(texts, fontweight=600,fontsize = 15)

    with io.BytesIO() as image_binary:
        plt.savefig(image_binary,format='png', bbox_inches="tight")
        image_binary.seek(0)
        files= discord.File(fp=image_binary, filename='image.png')
        return files