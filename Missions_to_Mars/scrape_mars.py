# import and setup dependencies
# to scrape from html
from bs4 import BeautifulSoup as bs

# to control browser
from splinter import Browser
browser = Browser("chrome", headless=False)

# to format data
import pandas as pd

# to format URLs
from urllib.parse import urlsplit

# for pause
import time

def scrape():
    # set url to NASA news site and visit with splinter
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    # get html from splinter and give to BeautifulSoup
    html = browser.html
    page_to_parse = bs(html,"html.parser")
    # use soup to pull first article title and paragraph
    news_title = page_to_parse.find("div",class_="content_title").find("a").text
    news_p = page_to_parse.find("div", class_="article_teaser_body").text
    # set link to get jpl image, send splinter to fetch
    jpl_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_image_url)
    # navigate browser to full size image
    browser.click_link_by_partial_text('FULL IMAGE')
    # give page time to load
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    # get html from splinter and give to BeautifulSoup
    html = browser.html
    page_to_parse = bs(html,"html.parser")
    # find image url with soup
    img_src = page_to_parse.find('img', class_='main_image').get('src')
    # get the base url
    base_url = "{0.scheme}://{0.netloc}".format(urlsplit(jpl_image_url))
    # put them together
    featured_image_url=base_url + img_src
    #get weather tweet
    tweet_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(tweet_url)
    # xpath to tweet div
    tweet_xpath='//*[@id="stream-item-tweet-1164580766023606272"]/div[1]/div[2]/div[2]/p'
    mars_weather  = browser.find_by_xpath(tweet_xpath).text
    # get mars facts
    url = "https://space-facts.com/mars/"
    mars_table = pd.read_html(url)
    # import table into df, make df into table ... ok
    mars_facts=mars_table[1]
    mars_facts.set_index(0, inplace=True)
    mars_facts = mars_facts.to_html()
    # go to USGS Astrogeology get html
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # get the base url
    base_url = "{0.scheme}://{0.netloc}".format(urlsplit(url))
    browser.visit(url)
    html = browser.html
    page_to_parse = bs(html,"html.parser")
    # collect titles and links to hemisphere_image_urls
    hemisphere_image_urls = []
    hemisphere_image_urls_titles = []
    hemisphere_image_urls_images = []
    img_urls = []
    # collect container divs with links and titles
    item_div = page_to_parse.find_all('div', class_='item')
    # iterate through containers
    for item in item_div: 
    # grab title
        title = item.find('h3').text
    # collect links
        img_urls.append(item.find('a', class_='product-item')['href'])
        hemisphere_image_urls_titles.append(title)
    # visit collected links to gather large image links
    for link in img_urls:
        browser.visit(base_url + link)
        img_html = browser.html
        page_to_parse = bs(img_html, 'html.parser')
    # collect links
        full_img_url = base_url + page_to_parse.find('img', class_='wide-image')['src']
        hemisphere_image_urls_images.append(full_img_url)
    for url, title in zip(hemisphere_image_urls_images, hemisphere_image_urls_titles):
        hemisphere_image_urls.append({"title" : title, "img_url" : url})
    # make dictionary out of all collected data for use in flask app
    mars_info={"news_title":news_title,
            "news_p":news_p,
            "featured_image_url":featured_image_url,
            "tweet_url":tweet_url,
            "mars_weather":mars_weather,
            "mars_facts":mars_facts,
            "hemisphere_image_urls":hemisphere_image_urls    
            }
    browser.quit()
    return mars_info






  