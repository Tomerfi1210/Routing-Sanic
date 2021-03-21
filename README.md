# TCM-TEST
Python test

The goal of this exercise is to create an API webserver that can scrape the Wikipedia site.
This webserver must be coded in Python. It should be created with the Python Sanic library. 
It will have only one route allowing to call the scraping. The only input parameter will be the page to scrape.
Example of parameter: page = New_Zealand
The scraped page will be: https://en.wikipedia.org/wiki/New_Zealand
	“https://en.wikipedia.org/wiki/” is a fixed part.

The objective of this exercise is to retrieve the value of the RLCONF variable from the source page. This variable is a JSON, and from it, you need to store the value of the following labels in a PostgreSQL database:
  - wgRequestId
  - wgCategories
  - wgPageContentLanguage
  - wgRelevantPageName

In order to retrieve the source page data, you can use the Python aiohttp library.
To analyze the data of the page you can use the Selector and xpath methods of the parsel library.
