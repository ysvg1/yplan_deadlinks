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
