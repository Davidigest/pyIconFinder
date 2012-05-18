#*******************************************************************************
# PyIconFinder: A python library for search icons from IconFinder
# IconFInder :
# _______________________________
#
#  Authors : David Kou
#			Davidigest@gmail.com
# _______________________________
#
#*******************************************************************************
# History
# v0.1,  May. 18 2012
#*******************************************************************************

import urlparse
import urllib, urllib2, json

from config import settings
import math


# http://www.iconfinder.com/json/search/?q=user&c=10&p=0&min=1&max=48&api_key=123456789
# q: Search term
# p: Specify result page (index). Starts from 0
# c: Number of icons per page. (Takes values between 1 and 100)
# l: Filter on license. Takes the following values:
# 		0 - include all icons
# 		1 - includes only icons with commercial licenses
# 		2 - includes only icons with commercial license which does not require a link to designer's website.
# min: Specify minimum size of icons
# max: Specify maximum size of icons
# api_key: An Iconfinder API key
# callback: Name of callback function (JSONP)

class ImageItem(object) :
	def __init__(self, id, size, tags, imageUrl) :
		self.id = id
		self.size = size
		self.tags = tags
		self.imageUrl = imageUrl



class IconFinder (object) :
	def __init__(self, keywords, nIconsPerPage = 20, minSize = 12, maxSize = 256) :
	   	self.api_key 	= settings['api_key']
	   	self.base_url 	= settings['url']

		self.keywords = keywords
		self.nIconsPerPage = nIconsPerPage
		self.minSize = minSize
		self.maxSize = maxSize

		self.currentPage = None
		self.totalPage = None


	def search(self) :
		"""
		This function searches icons/pngs from IconFinder website, and returns
		matched images
		<I> keywords: 		the search term, e.g. 'Tools', 'settings', 'New', 'Open' etc
		<I> nIconsPerPage:	how many images are returned from this search and in the current page
							note that paging is used to return part of the results
		<I> minSize:		the minimum size of the image to be returned
		<I> maxSize:		the maximum size of the image to be returned
		<O> Images:			the return value, a list of images, each item is of type ImageItem
							see also the class ImageItem above
		"""
		self.currentPage = 0
		return self._search_page()

	def searchNext(self) :
		"""
		This function searches for next N = nIconsPerPage images,
		if there is no more images on the next page, None is returned
		"""
		if self.currentPage >= self.totalPage :
			return None
		else:
			return self._search_page()


	def searchAll(self) :
		output = []
		self.currentPage = 0

		while True:
			images = self._search_page()
			if images == None or len(images) == 0 :
				return output
			else:
				output += images

	def _search_page(self) :
		if self.currentPage == None :
			print "Call IconFinder.Search() first!"
			return

		param = {}
		param['q']  = self.keywords
		param['p']  = self.currentPage		# 0, 1, 2 ...
		param['c']  = self.nIconsPerPage
		param['l']  = '0'
		param['min']  = self.minSize
		param['max']   = self.maxSize
		param['api_key'] = self.api_key

		url = self.base_url + urllib.urlencode(param)
		request = urllib2.Request(url)
		results = urllib2.urlopen(request).read()
		#print results
		
		try:
			results = json.loads(results)
		except Exception, e:
			print results
			return None
		# finally :
		# 	return results				
		# # print results

		output = []
		icons = results['searchresults']['icons']
		# print icons
		nTotoalIcons = results['searchresults']['totalResults']
		# print nTotoalIcons

		if icons is None :
			return None

		for item in icons:
			img = ImageItem(
					id = item['id'],
					size = item['size'],
					tags = item['tags'],
					imageUrl = item['image'])
			output.append(img)

		self.currentPage += 1
		self.totalPage = math.ceil(nTotoalIcons*1.0/self.nIconsPerPage)
		return output;




if __name__ == "__main__":
	finder = IconFinder('Tools', maxSize = 48)
	images = finder.search()			# Search once, default nIconsPerPage = 20
	if images != None:
		images += finder.searchNext() 	# Search next 20 images
	
		for item in images:
		 	print item.imageUrl

