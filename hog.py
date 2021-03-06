from PIL import Image,ImageOps
import numpy as np
from matplotlib import pyplot as plt
from skimage.draw import line_aa
import argparse
def dira(img,imd,d):#gradient will distribute to 2 closest bin with waightage as its distance from the bin
    m,n=np.shape(img)
    p=np.zeros(d)
    for i in range(m):
        for j in range(n):
            a=int(imd[i,j])
            c=imd[i,j]-a
            if a==d-1:
                b=0
            else:
                b=a+1
            p[b]+=c*img[i,j]
            p[a]+=(1-c)*img[i,j]
    return p
def conve(b,a):#convolution
    (m,n)=b.shape
    (p,q)=a.shape
    c=np.zeros((m-p+1,n-q+1))
    for i in range(p):
        for j in range(q):
            d=b*a[i,j]
            r=(-p+i+1)
            s=(-q+j+1)
            if(r*s!=0):
                d=d[i:r,j:s]
            elif(r!=0):
                d=d[i:r,j:]
            elif(s!=0):
                d=d[i:,j:s]
            else:
                d=d[i:,j:]
            c=c+d
    return c
def dir(img,imd,d):
    m,n=np.shape(img)
    p=np.zeros(d)
    for i in range(m):
        for j in range(n):
            p[int(imd[i,j])]+=img[i,j]
    return p
def cl(m,s):
    if m%s<s/2:
        m=(m//s)*s
    else:
        m=(1+m//s)*s
    return m
def gen(f1,t,s,u,b):
    z=np.zeros((t*(2*b+1),s*(2*b+1)))
    for i in range(s):
        for j in range(t):
            v=np.multiply(u, f1[i,j][:, np.newaxis])
            v=v.astype(np.int)
            for k in v:
                rr, cc, val = line_aa(j*(2*b+1)+b, i*(2*b+1)+b, j*(2*b+1)+b+k[0], i*(2*b+1)+b+k[1])
                z[rr, cc] = val
    return z
parser=argparse.ArgumentParser()
parser.add_argument("-n",'--name',type=str,help="name/path of the image file")
parser.add_argument("-d",'--direction',type=int,help="number of direction")
parser.add_argument("-x",'--blockx',type=int,help="number of blocks on x axis")
parser.add_argument("-y",'--blocky',type=int,help="number of blocks on y axis")
parser.add_argument("-b",'--blocksize',type=int,help="size of the block")
args=parser.parse_args()
if(args.name):
    im=ImageOps.grayscale(Image.open(args.name))
else:
    print('need an argument "-n"')
    exit('error')
m,n=im.size
m-=2
n-=2
if(args.direction):
    direction=args.direction
else:
    direction=16
if(args.blockx):
    s=args.blockx
else:
    print('need an argument "-x"')
    exit('error')
if(args.blocky):
    t=args.blocky
else:
    t=s
if(args.blocksize):
    blocksize=args.blocksize
else:
    blocksize=50
m=cl(m,s)
n=cl(n,t)
im=im.resize((m+2,n+2))
im=np.array(im)/255
u=[]
for i in range(direction):
    u.append([blocksize*np.sin(np.pi+i*np.pi*2/direction),blocksize*np.cos(np.pi+i*np.pi*2/direction)])
u=np.array(u).astype(np.int)
p=np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
imy=conve(im,p)
imx=conve(im,np.transpose(p))
img=np.sqrt(np.multiply(imx,imx)+np.multiply(imy,imy))
imd=(np.arctan2(imy,imx)/np.pi+1)*direction/2
imd=np.where(imd==direction,0,imd)
m,n=np.shape(img)
q=m//t
r=n//s
f=[]
for i in range(s):
    g=[]
    for j in range(t):
        g.append(dira(img[j*q:j*q+q,i*r:i*r+r],imd[j*q:j*q+q,i*r:i*r+r],direction))
    f.append(g)
f=np.array(f)
z=gen(f/f.max(),t,s,u,blocksize)
f=[]
for i in range(s):
    g=[]
    for j in range(t):
        y=dira(img[j*q:j*q+q,i*r:i*r+r],imd[j*q:j*q+q,i*r:i*r+r],direction)
        y1=y.max()
        if y1>.0001:
            g.append(y/y.max())
        else:
            g.append(y)
    f.append(g)
f=np.array(f)
z1=gen(f,t,s,u,blocksize)
plt.imshow(z,cmap='gray')
plt.show()
plt.imsave('global.png',z,cmap='gray')
plt.imshow(z1,cmap='gray')
plt.show()
plt.imsave('local.png',z1,cmap='gray')
