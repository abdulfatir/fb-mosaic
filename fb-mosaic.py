import os
from PIL import Image
import urllib
import json
import math

def download_images(a,b):
	image_count = 0
	k = a
	no_of_images = b
	baseURL='https://graph.facebook.com/v2.2/'
	imgURL='/picture?type=large'
	sil_check='/picture?redirect=false'
	while image_count<no_of_images:
		obj=urllib.urlopen(baseURL+str(k)+sil_check)
		data=obj.read()
		jsondata=json.loads(data)
		if not jsondata['data']['is_silhouette']:
			img=urllib.urlopen(baseURL+str(k)+imgURL)
			image=img.read()
			f=open(str(k)+'.jpg','wb')
			f.write(image)
			f.close()
			print 'Image written to '+str(k)+'.jpg'
			image_count+=1
		else:
			print str(k)+' is Silhouette.'
		k+=1
def resize_images():
	files=[f for f in os.listdir('.') if os.path.isfile(f) and '.jpg' in f]
	print 'Resizing images ...'
	for i in files:
		img=Image.open(i)
		j = i.replace('jpg','png')
		img.resize((100,100)).save(j)
		img.close()
		os.remove(i)
def create_mosaic(b):
	files=[f for f in os.listdir('.') if os.path.isfile(f) and '.png' in f]
	no_of_images = b
	N = int(math.sqrt(no_of_images))
	mosaic=Image.new('RGB',(N*100,N*100))
	mpixels=mosaic.load()
	mX,mY = 0,0
	counter=0
	print 'Combining images ...'
	for img in files:
		mX = (counter%N)*100
		mY = (counter/N)*100
		image=Image.open(img)
		pixels=image.load()
		for iY in range(100):
			mX = (counter%N)*100
			for iX in range(100):
				try:
					mpixels[mX,mY] = pixels[iX,iY]
				except:
					print mX,mY
				mX+=1
			mY+=1
		counter+=1
		image.close()
		os.remove(img)
	mosaic.save('mosaic.png')

a = int(raw_input('Enter the fb-id from where to begin:'))
b = int(raw_input('Enter the number of images to download (a square):'))
download_images(a,b)
resize_images()
create_mosaic(b)
