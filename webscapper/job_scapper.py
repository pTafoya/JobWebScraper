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

"""
Example command to run:

python job_scapper.py -j java_developer,programmer,web_developer -c indeed -q entry -e -u "https://www.indeed.com/jobs?q=java+developer&l=perth+amboy%2C+nj" -p "&start=" -b "results.xls" -i 10 -m 10

python job_scapper.py -j java_developer,programmer,web_developer -c indeed -q entry -e -u "https://www.monster.com/jobs/search/?q=java-developer&where=Perth-Amboy__2C-NJ&intcid=skr_navigation_nhpso_searchMain" -p "&start=" -b "results.xls" -i 10 -m 10
"""

class CommandReader():
	
	def __init__(self, argv):
		self.argv = argv
		self.enforced = False
		self.job_titles = []
		self.readArguments()
		
	def default(self, str):
		return str + ' [Default: %default]'
		
	def readArguments(self):
		
		USAGE_STRING = """
			USAGE:		python job_scapper.py <options>
						"""
		from optparse import OptionParser  
		parser = OptionParser(USAGE_STRING)
		
		parser.add_option('-j', '--job_titles', help = self.default('Give a list of job titles appplying to, seperated by commas, replace spaces with underscore'), default = None, type = "string")
		parser.add_option('-c', '--company_name', help = self.default('Name of Company'), default = None, type = "string")
		parser.add_option('-q', '--experience_level', help = self.default('Indicate level of experience'), choices = ['entry', 'mid', 'senior', 'intern'], default = None)
		parser.add_option('-e', '--enforced', help = self.default('Indicate if there is some enforcement in search'), default = False, action = "store_true")
		parser.add_option('-u', '--given_url', help = self.default('Url that will be used for searching, please have an initial search'), default = None, type = "string")
		parser.add_option('-p', '--page_nav', help = self.default('Add the url part that is used for navigation'), default = None, type = "string")
		parser.add_option('-b', '--name_of_file', help = self.default('Name where url search will be saved'), default = None, type = "string")
		parser.add_option('-d', '--url_domain', help = self.default('Indicate the domain for url'), default = None, type = "string")
		parser.add_option('-i', '--iteration', help = self.default('Indicate the number of items to search per page'), default = 0, type = "int" )
		parser.add_option('-m', '--max_iterations', help = self.default('Indicate max number of pages to search'), default = 0, type = "int")
		
		options, otherstuff = parser.parse_args(self.argv)
		
		if len(otherstuff) != 0:
			raise Exception('Command line input not understood: ' + str(otherstuff))
		
		jlisting = []
		jlisting = list(options.job_titles.split(','))
		
		for job in jlisting:
			tjob = job.replace("_", " ")
			self.job_titles.append(tjob)
		
		self.company_name = options.company_name
		self.level_of_experience = options.experience_level
		self.enforced = options.enforced
		self.initial_url_page = options.given_url
		self.page_nav = options.page_nav
		self.book_name = options.name_of_file
		self.url_domain = options.url_domain
		self.iteration = options.iteration
		self.max_iterations = options.max_iterations
		
		
class Searcher(Thread):

	def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
		Thread.__init__(self, group, target, name, args, kwargs)
		self._return = None
		

	def run(self):
		count = 0
		curr_interval = 0
		pages_to_search = []
		
		
		while count < self._kwargs['max_iterations']:
			
			response = get(self._kwargs['s_url'] + str(curr_interval))
			html_soup = BeautifulSoup(response.text, 'html.parser')
			page_results = html_soup.find_all('h2', class_ = 'jobtitle')
			
			for result in page_results:
				url_link = result.find('a', href=True)
				mlink = url_link['href']
				
				if "/company/" in mlink:
					link = "https://www.indeed.com" + mlink
				else:
					mlink = mlink.replace("/rc/clk?", "")
					link = "https://www.indeed.com/viewjob?"+mlink
				pages_to_search.append(link)
			
			count += 1
			curr_interval += self._kwargs['iteration']
			sleep(randint(1,3))
			
		self._return = pages_to_search
		
	def join(self):
		Thread.join(self)
		return self._return
		
class Company:
	
	def __init__(self, company, url, job_titles, level_of_experience, enforced, page_url_part, url_domain):
		self.company = company
		self.url = url
		self.level_of_experience = level_of_experience
		self.urls = []
		self.job_titles = job_titles
		self.enforced = enforced
		self.page_url = page_url_part
		self.url_domain = url_domain
		self.defineURLSearches()
		
			
	def defineURLSearches(self):
		first_job = self.job_titles[0]
		strn_arr = first_job.split(' ')
		
		count = 0
		first = True
		for strn in strn_arr:
			if first:
				self.url = self.url.replace(strn, '{}', 1)
				first = False
			else:
				self.url = self.url.replace(strn, '', 1)
			count += 1
			
		count -= 1
		
		if count > 0:
			self.url = self.url.replace("+", "", count)
		
		
		for title in self.job_titles:
			title_arr = title.split(' ')
			search_strn = ""
			
			for word in title_arr:
				search_strn += word + "+"
			
			tmp = search_strn.rsplit("+", 1)
			search = "".join(tmp)
			if(self.level_of_experience is not None):
				if self.enforced:
					search += "+\""+self.level_of_experience+"\""
				else:
					search += "+"+self.level_of_experience
			
			
			self.urls.append(self.url.format(search) + self.page_url)
			
	def startSearching(self, iteration, max_iterations):
		
		mthreads = []
		counter = 1
		
		for s_url in self.urls:
			margs  = {'counter': counter, 's_url': s_url, 'iteration': iteration, 'max_iterations': max_iterations , 'domain': self.url_domain}
			tmpSearcher = Searcher(kwargs = margs)
			tmpSearcher.start()
			mthreads.append(tmpSearcher)
		
		mIterations = []	
		
		for t in mthreads:
			mIterations.append(t.join())
		
		return mIterations

def saveResults(book, sheetName, results):
	
	curr_sheet = book.add_sheet(sheetName)
	
	row = 0 
	for result in results:
		curr_sheet.write(row, 0, result)
		row += 1
	
if __name__ == "__main__":

	argv = CommandReader(sys.argv[1:])
	
	indeed = Company(argv.company_name, argv.initial_url_page, argv.job_titles, argv.level_of_experience, argv.enforced, argv.page_nav, argv.url_domain)
	
	mIterations = indeed.startSearching(argv.iteration, argv.max_iterations)
	
	bookname = argv.book_name
	book = xlwt.Workbook(encoding="utf-8")
	count = 0
	
	for results in mIterations:
	
		saveResults(book, argv.job_titles[count], results)
		count += 1
		
	book.save(bookname)
	
	