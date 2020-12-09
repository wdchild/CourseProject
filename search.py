# running python 3.7.4
from bs4 import BeautifulSoup
import bs4
from search_engine_parser import GoogleSearch
from search_engine_parser.core.engines.yahoo import Search as YahooSearch
from scraper import *
from analyzer import *

# DUMMY DATA FOR TESTING PURPOSES
dummy_html = '''	<title>積集合演算と和集合の違い</title>
					<h1>合演算</h1>
					<div>積集
						<p>積集合こと演算</p>
						<p>合演合和集合演合演合演積集合演算合演合演合演合演</p>
						<p>黒文字は花です。文字とは関係がない。</p>
					</div>
					<h2>黒文字とは</h2>
				'''

if __name__=='__main__':

	# TARGET EXPRESSIONS FOR DEMO PURPOSES
	easy_target = '積集合'
	medium_target = '黒文字'
	hard_target = '出来高'
	harder_target = '縦横断測量'
	hardest_target = '積集合演算'

	# CREATE A SCRAPER OBJECT AND RUN THE SEARCH
	scraper = Scraper(target = hard_target, max_depth = 1, engine="yahoo")
	print(scraper) # shows the settings
	scraper.run_search()

	# for each page in the set of pages returned by chromedriver ...
		# get the soup
		# clean it up 
		# see if the text has the actual word verbatim (regex)
		# if it is, store the data in "scraper.results"
	print(scraper.results)

	# load Stanza NLP module for Japanese
	# load the data from scraper.results into format used by analyzer
	# analyze the results
	# write the sentences containing expression and corresponding analysis to file
	analyzer = Analyzer(hard_target) # make sure this variable matches the one that was scraped
	analyzer.load_data_directly(scraper.results)
	analyzer.analyze_data()
	analyzer.write_analysis() 

	# MAY WANT TO BE ABLE TO SEARCH FOR TRANSLATIONS
	# MAY WANT TO SEARCH FOR DEFINITIONS

	# FOR DUMMY TESTING THE dummy_html AT TOP
	# scraper.soup = bs4.BeautifulSoup(dummy_html, 'html5lib')
	# scraper.match_target(url_num = 1)

