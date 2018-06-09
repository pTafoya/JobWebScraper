import xlwt
from threading import Thread


class NumberRunner(Thread):
	
	def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
		Thread.__init__(self, group, target, name, args, kwargs)
		self._return = None
		
	def run(self):
		
		mlist = []
		val = 0
		for i in range(self._kwargs['count']):
			val += self._kwargs['value']
			mlist.append(val)
			
		self._return = mlist
		
	def join(self):
		Thread.join(self)
		return self._return

def saveItem(sheet, listing, row):
	
	for count in range(len(listing)):
		sheet.write(row, count, listing[count])
	
if __name__ == "__main__":
	
	mthreads = []
	
	for i in range(100):
		tmpNum = NumberRunner(kwargs = {'count': i, 'value' : i})
		mthreads.append(tmpNum)
		tmpNum.start()
	
	book = xlwt.Workbook(encoding="utf-8")
	sheet = book.add_sheet("Sheet 1")
	
	row = 0
	for cthread in mthreads:
		items = cthread.join()
		saveItem(sheet, items, row)
		row += 1
	book.save("testing.xls")