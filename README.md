# yplan_deadlinks
a simple Scrapy spider to locate dead links on the yplanapp.com website 

Install Scrapy if not present:
```shell
pip install scrapy
```
Run the spider:
```shell
cd yplan_deadlink_finder
scrapy crawl deadlink_finder -o output.csv -t csv 
```
The script will create a CSV file, listing the dead links and reason why each was considered dead. 

## Reasoning

Scrapy is used here, because it is a well-established crawling framework. And using a framework instead of writing a custom application has the advantages of:
* saving time on implementation;
* making the application easier for the others to understand and extend;
* better reliability, as the framework has been tested by numerous developers.

The spider first loads the main page of the target website (yplanapp.com), and detects all 'href' attributes in the ```<a>``` tags present on the page.

For all external links on the page, a HEAD request is sent with a timeout time of 10 seconds. The redirects are automatically followed. An external link is considered 'dead' if no successful response is received, or if an exception is thrown by the underlying library (*requests*).

For all internal links, a normal GET request is issued, the corresponding pages are loaded and handled just like the main page. After all available pages of the website are loaded and all external links are checked, the spider stops.
