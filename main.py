#!/usr/bin/env python3
import requests
import os
import json
import pickle
import random
import time
from tqdm import tqdm

categories=["latest","popular"]
catfiles={"latest":"links.pkl","popular":"links2.pkl"}


#initialize directory to store image
directory=os.getenv("HOME")+"/bin/wallp/"
if(not os.path.exists(directory)):
	os.mkdir(directory)

def setWallpaper():
	command="gsettings set org.gnome.desktop.background picture-uri file://{}wallp.jpg".format(directory)
	os.system(command)

def getLinks(cat):
	try:
		#get list of links to images from file based on category
		filename=directory+catfiles[cat]
		with open(filename,"rb") as file:
			links=pickle.load(file)
		return links
	except:
		updateLinks()

def updateLinks():
	#get links to images from the unsplash.com api, save them to file based on category
	links=[]
	try:
		#get links from  both categories
		for j in range(2):
			payload={
				"client_id":"your_api_key_here",
				"per_page":"30",
				"order_by":categories[j]
			}
			if j==0:
				filename=directory+"links.pkl"
			else:
				filename=directory+"links2.pkl"
			#loop through pages 1-3
			for i in range(20):
				r=requests.get("https://api.unsplash.com/photos?page={}".format(i+1),params=payload)
				data=json.loads(r.text)
				#for each page loop through each dictionary (image object) returned
				for d in data:
					link=d["urls"]["raw"]#grab link
					links.append(link)
			with open(filename,"wb") as file:
				pickle.dump(links,file)
			print("Successfully updated links")
	except:
		print("Error when querying api, limit has been reached")

def downloadImg(link,name):
	#downloads image from a url
	chunk_size=1024
	try:
		r=requests.get(link,stream=True)
		total_size=int(r.headers['content-length'])
		with open(name,'wb') as file:
			for chunk in tqdm(iterable=r.iter_content(chunk_size=chunk_size),total = total_size/chunk_size,unit='KB'):
				file.write(chunk)
		print("Download Complete")
		return True
	except:
		return False

def updateWallpaper():
	#get random category to choose from
	cat=random.choice(categories)
	links=getLinks(cat)
	#get random link from category
	link=random.choice(links)
	#print(link)
	downloadImg(link,directory+"wallp.jpg")
	setWallpaper()

def main():
	updateWallpaper()

if __name__=="__main__":
	main()