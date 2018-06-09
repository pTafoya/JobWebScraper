import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import xlwt
import re

class Writter:
	
	def __init__(self, book_name):
		self.book = xlwt.Workbook(encoding="utf-8")
		self.book_name = book_name
	
	def addSheet(self, title):
		if title is None :
			return
			
		self.current_sheet = self.book.add_sheet(title)
		
	def writeToSheet(self, sheet = None, text, row, column):
		if sheet is None:
			sheet = self.current_sheet
		
		sheet.write( row, column, text);