# BSE-Bhavcopy
* Stand alone CherryPy webapp.
* For scraping the data from the "Nifty 50" using dryscrape and beautifulsoup(bs4) libraries of python.
scrapy.py python script which scraps the data in every 5 minutes is running on different thread using multithreading standard library of python.
* Data is storing into a Redis instance using a third party python library redisworks. 
* All the data fetched from redis is showing in card layouts using html/css.

Deployed on heroku check the weapp [here](http://ec2-54-149-205-131.us-west-2.compute.amazonaws.com:8080/)
