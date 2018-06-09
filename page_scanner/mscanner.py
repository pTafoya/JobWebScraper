#this is the first version of how I wil search a page
#testing will be done on Indeed webpage

import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import xlwt
import re
import sys
from threading import Thread 
import time
from time import sleep
from random import randint
import xlwt

class MyProfile():
	
	def __init__(self, skills):
		self.skills = mskills

class PostScanner():
	
	def __init__(self):
		return
	
	
def collectAll():
	return

def getOne():
	return
	
def scan(url, ):
	
	
	response = get(url)
	html_soup = BeautifulSoup(response.text, 'html.parser')
	page_results = html_soup.find_all('h2', class_ = 'jobtitle')
	
	return

if __name__ == "__main__":
	
	mskills = {"java": 2 , "eclipse": 2, "git": 1,"javafx": 1, "python": 1, "javascript":1, "html": 1, "css":1, "c": 2 }
	
	murl = "https://www.indeed.com/viewjob?jk=60fd214f9ed0665c&from=recjobs&vjtk=1cfb4aqpu18h13dl"
	scan(murl)