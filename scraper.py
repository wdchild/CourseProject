
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from search_engine_parser import GoogleSearch
from search_engine_parser.core.engines.yahoo import Search as YahooSearch
import soupsieve as sv
import re

def google(query, page_num=1):
	assert(page_num>0) # CHANGE SO YOU CAN CONCATENATE RESULT IF YOU WANT MORE PAGES
	search_args = (query, page_num)
	google_search = GoogleSearch()
	google_results = google_search.search(*search_args)
	return google_results['links']

def yahoo(query, page_num=1):
	search_args = (query, page_num)
	yahoo_search = YahooSearch()
	yahoo_results = yahoo_search.search(*search_args)
	return yahoo_results['links']

# A scraper class used to parse web pages
class Scraper():
	def __init__(self, target, max_depth=5, engine="both"):
		options = Options()
		options.headless = True
		self.target = target # the target expression being sought
		self.driver = webdriver.Chrome('/Users/danielchild/Desktop/TIS/PROJECT/CourseProject/ProjectCode/chromedriver', options=options)
		self.max_depth = max_depth # the max number of pages of Google/Yahoo results to explore
		self.current_depth = 1 # which page of search results being returned
		self.matches_found = False 
		self.num_matches = 0
		self.current_page_set = [] # set of Google or Yahoo pages to analyze
		self.engine = engine
		self.soup = None
		self.results = [] # a list of tuples, with tag type (e.g. <div>) and the text

	# This method gets a set of pages to be explored for the specified engine
	# and at Scraper's current depth
	def find_page_set(self, engine, depth):
		print('*** FINDING PAGE SET ***')
		if engine == "google":
			pages = google(self.target, self.current_depth)
			print('\nGoogle Results for Page {}'.format(self.current_depth))
		elif engine == "yahoo":
			pages = yahoo(self.target, self.current_depth)
			print('\nYahoo Results for Page {}'.format(self.current_depth))
		else: # both
			pages = google(self.target, self.current_depth)
			yahoo_pages = yahoo(self.target, self.current_depth)
			pages.extend(yahoo_pages)
		self.current_page_set = pages
		print('*** Page results for depth {} using engine {}'.format(self.current_depth, self.engine))
		for p in range(len(pages)):
			print('{}\t{}'.format(p, pages[p]))
		
	# This function uses BeautifulSoup to parse the inner html and 
	# returns a BeautifulSoup object for parsing html content
	def get_soup(self, url):
		print('*** GETTING SOUP ***')
		# reinitialize soup
		self.soup = None
		try:
			self.driver.get(url)
			body_html = self.driver.execute_script('return document.body.innerHTML')
			self.soup = BeautifulSoup(body_html,'html.parser')
		except:
			print('Something went wrong with chromedriver retrieving this url...')
			self.soup = None

	# This method removes some of the junk that does not contribute to the text
	def strain_soup(self):
		print('*** STRAINING SOUP ***')
		for tag in self.soup("script", "class", "style", "span"):
			tag.decompose()

	def store_result(self, elmt_name, text):
		self.results.append((elmt_name, text))

	# This method checks for elements that have an exact match with the target expression
	# If the expression is found, the matches_found flag is set to True, and the number
	# of matches is incremented.
	def match_target(self, url_num):
		print('*** MATCHING TARGET ***')
		targ = re.compile(self.target)
		found_targets = self.soup(text=targ)
		if len(found_targets) == 0:
			print('Url {} has no matches for {}'.format(url_num, self.target))
		else:
			print('Url {} has matches for {}'.format(url_num, self.target))
			for element in found_targets:
				self.matches_found = True
				self.num_matches += 1
				elmt_name = element.parent.name
				text = element.parent.get_text().strip()
				if len(text) > len(self.target): # no need to keep just the expression
					print('{}\t{}\n'.format(elmt_name, text))
					self.store_result(elmt_name, text)

	# This method processes a set of urls (one "page set") meaning a page of results from either 
	# Google or Yahoo
	def process_page_set(self, retrieved_urls):
		print('*** PROCESSING PAGE SET ***')
		for url_num in range(len(retrieved_urls)):
			self.get_soup(retrieved_urls[url_num])
			if self.soup != None:
				self.strain_soup()
				self.match_target(url_num)
			else:
				print('CHROMEDRIVER ERROR: Url {} threw an error within chromedriver. Moving to next page.')

	def run_search(self):
		print('*** RUNNING SEARCH ***')
		while (self.num_matches == 0 and self.current_depth <= self.max_depth):
			self.find_page_set(self.engine, self.current_depth)
			self.process_page_set(self.current_page_set)
			self.current_depth += 1

	# For printing a description of the scraper object
	def __str__(self):
		ret_str = '\nScraper with max depth: ' + str(self.max_depth) + '\n\ttarget: ' \
					+ self.target + '\n\tand engine: ' + self.engine + '\n'
		return ret_str

if __name__=='__main__':
	driver = get_driver()
	print(driver)
	# target_url = "https://wiis.info/math/set/set/direct-product/"
	# soup = get_js_soup(target_url, driver)
	# print(soup)
