pyIconFinder
============

pyIconFinder offers an intuitive python interface to query/search icon images from IconFinder.com. 
Making things simple is great! Never make simple things complex.

IconFinder is an efficient search engine with more than 150.000 free icons. 
This project aims at offering a programatic interface to allow users to 
query/search related icons with Python language.

Example :
-----------------------------------------------------
Search icons related to "Zoom"
# finder = IconFinder('Zoom', maxSize = 48) 
-----------------------------------------------------
Search once, default 20 icons are returned   
# images = finder.search()	 
-----------------------------------------------------
Search next 20 images. if there exists
# if images != None:
#         images += finder.searchNext()  
-----------------------------------------------------
# images with url info are returned.
-----------------------------------------------------                                   


# Note:
You should have your own IconFinder account, so that you have a valid api_key to perform the icon search.


