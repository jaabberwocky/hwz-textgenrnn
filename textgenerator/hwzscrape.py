"""
created by Tobias Leong
v1.1

Scrape any HWZ thread!
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd
import argparse
from textblob import TextBlob
import os
from pyfiglet import Figlet


def setupCLI():
	'''
		Setups CLI tooling.

		Args: None
	'''
	parser = argparse.ArgumentParser(
	    description='Scrape a HWZ post and returns a CSV file.\nBy: Tobias Leong')
	parser.add_argument('URL', metavar='URL', type=str,
	                    help='Specify the URL of the post here')
	parser.add_argument('--output', metavar='Output Directory',
	                    help='Specify the path of the output directory here')
	args = parser.parse_args()
	return parser, args


def printWelcomeMessage(message, font='slant'):
	'''
		Prints *pretty* welcome message

		Args: None
	'''
	f = Figlet(font=font)
	print(f.renderText(message))
	return None


def getURL(args):
	'''
		gets URL from arguments parsed to CLI

		Args: args [arguments from parser]
	'''
	url = args.URL
	return url


def getPageHTML(url):
	'''
		Opens connection and gets HTML

		Args: url
	'''
	client = urlopen(url)
	page_html = client.read()
	client.close()
	return page_html


def getPageSoup(page_html):
	'''
	Parses HTML to get Soup

	Args: page_html
	'''
	return soup(page_html, "html.parser")


def getPageNumbers(page_soup):
	'''
		Gets page numbers from soup object.

		Args: page_soup
	'''
	y = page_soup.find("div", {"class": "pagination"})
	if y is None:
		# this means that it is single page !
		total_pages = 1
	else:
		total_pages = int(y.span.text.split(" ")[-1])
	return total_pages


def getPosts(page_soup):
	'''
		Gets all posts from soup object.

		Args: page_soup
	'''
	return page_soup.findAll("div", {"class": "post-wrapper"})


if __name__ == "__main__":

	# initialise
	printWelcomeMessage('HWZ Scrapper!')
	parser, args = setupCLI()
	my_url = getURL(args)

	# get initial page soup and html
	page_html = getPageHTML(my_url)
	page_soup = getPageSoup(page_html)
	total_pages = getPageNumbers(page_soup)

	# loop for page
	pg = 1
	count = 0

	# initialise lists
	username_list = []
	content_list = []
	sentiment_polarity_list = []
	sentiment_subj_list = []
	datetime_list = []

	while pg <= total_pages:
		print("Scrapping page: ", pg, "....")
		url_loop = my_url.split(".html")[0] + '-' + str(pg) + ".html"
		pg += 1

		page_html = getPageHTML(url_loop)
		page_soup = getPageSoup(page_html)

		posts = getPosts(page_soup)

		for post in posts:
			count += 1
			username = post.find("a", {"class": "bigusername"}).text
			post_content = post.find("div", {"class": "post_message"}).text
			datetime_post = post.find("td", {"class": "thead"}).text.strip()

			# get sentiment polarity and subj
			sentiment_polarity, sentiment_subj = TextBlob(post_content).sentiment

			# append into lists, this will be used later to form the dataframe
			username_list.append(username)
			content_list.append(post_content)
			sentiment_polarity_list.append(sentiment_polarity)
			sentiment_subj_list.append(sentiment_subj)
			datetime_list.append(datetime_post)

			print("Scrapped %s post. Post: %d" % (username, count))

	df = pd.DataFrame({
		'datetime': datetime_list,
		'username': username_list,
		'content': content_list,
		'polarity': sentiment_polarity_list,
		'subjectivity': sentiment_subj_list})

	print("Scrapping complete!")

	if args.output:
		if os.path.isfile(os.path.join(os.getcwd(), args.output, 'hwzdata.csv')):
			os.remove(os.path.join(os.getcwd(), args.output, 'hwzdata.csv'))
			print("hwzdata.csv file found at output directory location...\ndeleting...")
		print("Creating csv...")
		df.to_csv(os.path.join(os.getcwd(), args.output, 'hwzdata.csv'))
	else:
		if os.path.isfile('hwzdata.csv'):
			print("hwzdata.csv file found at output directory location...\ndeleting...")
			os.remove('hwzdata.csv')
		print("Creating csv...")
		df.to_csv('hwzdata.csv')
