#!/usr/bin/env python
# coding: utf-8

# In[1]:

# import dependencies
import pandas as pd
import pymongo
import requests as req
from bs4 import BeautifulSoup as bs
from flask import Flask, redirect, render_template
from flask_pymongo import PyMongo
from selenium import webdriver
from splinter import Browser
import time 
import urllib.error

# In[2]:


executable_path = {'executable_path': '/Users/mraza/Downloads/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=True)


# In[3]:


#NASA Mars News Site


# In[4]:


news_url = "https://mars.nasa.gov/news/"
browser.visit(news_url)
html = browser.html

# Parse HTML with Beautiful Soup
soup = bs(html, "html.parser")

# Extract article title and paragraph text
article = soup.find("div", class_='list_text')
news_title = article.find("div", class_="content_title").text
news_p = article.find("div", class_ ="article_teaser_body").text
print(news_title)
print(news_p)


# In[5]:


### JPL Mars Space Images - Featured Image


# In[7]:


# visit JPL for featured Space Image
image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(image_url)
# look at full image
browser.click_link_by_partial_text('FULL IMAGE')
time.sleep(10)
# look at more information
browser.click_link_by_partial_text('more info')
# parse HTML with beautiful soup
html = browser.html
image_soup = bs(html, 'html.parser')
# scrape the URL
feat_img_url = image_soup.find('figure', class_='lede').a['href']
featured_image_url = f'https://www.jpl.nasa.gov{feat_img_url}'
print(featured_image_url)


# In[8]:


### Mars Facts


# In[9]:


# visit Mars facts webpage for interesting facts about Mars
facts_url = "https://space-facts.com/mars/"
browser.visit(facts_url)
html = browser.html


# In[10]:


# scrape the table containing mars facts using pandas
facts_url = 'https://space-facts.com/mars/'
tables = pd.read_html(facts_url)
tables


# In[11]:


mars_facts = tables[2]
mars_facts.columns = ["Description", "Value"]
mars_facts


# In[12]:


# convert the data to HTML
mars_facts.to_html('table.html')


# In[13]:


### Mars Hemispheres


# In[14]:


# visit the USGS astrogeology site
hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hemispheres_url)
html = browser.html

# parse HTML with beautiful soup
soup = bs(html, "html.parser")

# Create dictionary to store titles and links to images
hemisphere_image_urls = []

# retrieve all elements that contain image information
results = soup.find("div", class_ = "result-list" )
hemispheres = results.find_all("div", class_="item")
# create forloop to iterate through each image
for hemisphere in hemispheres:
    title = hemisphere.find("h3").text
    title = title.replace("Enhanced", "")
    end_link = hemisphere.find("a")["href"]
    image_link = "https://astrogeology.usgs.gov/" + end_link    
    browser.visit(image_link)
    html = browser.html
    soup = bs(html, "html.parser")
    downloads = soup.find("div", class_="downloads")
    image_url = downloads.find("a")["href"]
    hemisphere_image_urls.append({"title": title, "img_url": image_url})
# print image
print(hemisphere_image_urls)


# In[15]:

# Store data in a dictionary
mars_data = {
    "news_title": news_title,
    "news_p": news_p,
    "featured_image_url": featured_image_url,
    "mars_facts": mars_facts,
    "hemisphere_image_urls": hemisphere_image_urls
  }


# In[16]:

if __name__ == "__main__":
  scrape();