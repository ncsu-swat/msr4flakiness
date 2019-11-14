# This script allows to crawl information and repositories from GitHub using the GitHub REST API (https://developer.github.com/v3/search/).
#
# Given a query, the script downloads for each repository returned by the query its ZIP file.
# In addition, it also generates a CSV file containing the list of repositories queried.
# For each query, GitHub returns a json file which is processed by this script to get information about repositories.
#
# The GitHub API limits the queries to get 100 elements per page and up to 1,000 elements in total.
# To get more than 1,000 elements, the main query should be splitted in multiple subqueries using different time windows through the constant SUBQUERIES (it is a list of subqueries).
#
# As example, constant values are set to get the repositories on GitHub of the user 'rsain'.


#############
# Libraries #
#############

import wget
import time
import simplejson
import csv
import pycurl
import math
import io
import os

############
# Constants #
#############

# The basic URL to use the GitHub API
URL = "https://api.github.com/search/issues?q=flaky+test+in%3Atitle++comments%3A4+state%3Aclosed"
#Different subqueries if you need to collect more than 1000 elements
SUBQUERIES = ["+created%3A2015-01-01..2015-12-30", "+created%3A2016-01-01..2016-12-30", "+created%3A2017-01-01..2017-12-30", "+created%3A2018-01-01..2018-12-30", "+created%3A2019-01-01..2019-12-30"]
PARAMETERS = "&per_page=100" #Additional parameters for the query (by default 100 items per page)
DELAY_BETWEEN_QUERYS = 10 #The time to wait between different queries to GitHub (to avoid be banned)
OUTPUT_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/output" #Folder where ZIP files will be stored
OUTPUT_CSV_FILE = OUTPUT_FOLDER + "/issues.csv" #Path to the CSV file generated as output

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

#############
# Functions #
#############

def getUrl (url) :
	''' Given a URL it returns its body '''
	buffer = io.BytesIO()
	c = pycurl.Curl()
	c.setopt(c.URL, url)
	c.setopt(c.WRITEDATA, buffer)
	#c.setopt(pycurl.HTTPHEADER, ['Accept: application/vnd.github.cloak-preview'])
	c.setopt(pycurl.HTTPHEADER, ['Accept: application/vnd.github.symmetra-preview+json'])        
	c.perform()
	c.close()
	body = buffer.getvalue()
	return body

########
# MAIN #
########

#Output CSV file which will contain information about repositories
csvfile = open(OUTPUT_CSV_FILE, 'w')
csvwriter = csv.writer(csvfile, delimiter=',')

#Run queries to get information in json format and download ZIP file for each repository
for subquery in range(1, len(SUBQUERIES)+1):
	print ("Processing subquery " + str(subquery) + " of " + str(len(SUBQUERIES)) + " ...")
	# obtain the number of pages for the current subquery (by default each page contains 100 items)
	baseurl = URL +  str(SUBQUERIES[subquery-1]) + PARAMETERS			
	dataRead = simplejson.loads(getUrl(baseurl))
	totalcount = dataRead.get('total_count')
	if totalcount:
		numberOfPages = int(math.ceil(totalcount/100.0))
		# results are in different pages
		for currentPage in range(1, numberOfPages+1):
			print ("Processing page " + str(currentPage) + " of " + str(numberOfPages) + " ...")
			url = baseurl + "&page=" + str(currentPage)
			dataRead = simplejson.loads(getUrl(url))
			#Iteration over all the repositories in the current json content page
			items = dataRead.get('items')
			# in case there is no items field
			if items:
				for item in items:
					csvwriter.writerow([item['html_url']])
	else:
                print('did not find field total_count for this query')
	#add delay between different subqueries
	if (subquery < len(SUBQUERIES)):
		print ("Sleeping " + str(DELAY_BETWEEN_QUERYS) + " seconds before the new query ...")
		time.sleep(DELAY_BETWEEN_QUERYS)

csvfile.close()
