# Import BeautifulSoup and other modules needed
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
import time 

#time.sleep() provides time delay in seconds

# Import Splinter and set the chromedriver path

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

    browser = init_browser()

    #put all consolidated data into a dictionary 
    nasa_data_scrape = {}

    #Visit the following URL for NASA news
    url1 = "https://mars.nasa.gov/news/"
    browser.visit(url1)

    time.sleep(5)

    #might need to put a time delay on this scrap to get all the html
    html = browser.html
    soup = bs(html, "lxml")


    latest_news_title_html = soup.find('div', class_='content_title')
    #print(latest_news_title_html.a.text)
    news_title = latest_news_title_html.a.text

    nasa_data_scrape['latest_news_title'] = news_title
    
    #print(news_title)

    latest_news_teaser_html = soup.find('div', class_='article_teaser_body')
    news_p = latest_news_teaser_html.text

    nasa_data_scrape['latest_news_teaser'] = news_p
    
    #print(news_p)

    #Visit the url for JPL Featured Space Image https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    #Use splinter to navigate the site 
    #and find the image url for the current Featured Mars Image
    #assign the url string to a variable called `featured_image_url`.
    time.sleep(5)

    xpath1 = '//footer//a[@class="button fancybox"]'


    # Design an XPATH selector to click on current featured mars image
    results1 = browser.find_by_xpath(xpath1)
    img1 = results1
    img1.click()

    time.sleep(5)
    #large image within the article, need to click on another button
    xpath2 = '//div[@class="buttons"]/a[@class="button"]'


    results2 = browser.find_by_xpath(xpath2)
    img2 = results2
    img2.click()

    time.sleep(5)

    # Scrape the browser into soup and use soup to find the full resolution image of mars
    # Save the image url to a variable called `img_url`
    html2 = browser.html
    soup2 = bs(html2, 'html.parser')
    partial_img_url = soup2.find("figure", class_='lede').a["href"]
    featured_img_url = f'https://www.jpl.nasa.gov{partial_img_url}'
    
    #print(featured_img_url)
    nasa_data_scrape['featured_img_url'] = featured_img_url



    #Visit the Mars Weather twitter account
    mars_weather_twitter = 'https://twitter.com/marswxreport?lang=en'

    #scrape the latest Mars weather tweet from the page
    #Save the tweet text for the weather report as a variable called `mars_weather`.
    browser.visit(mars_weather_twitter)

    time.sleep(5)
    #get weather from twitter
    html3 = browser.html
    soup3 = bs(html3, 'html.parser')
    mars_weather_html = soup3.find_all('div', class_='js-tweet-text-container')
    #find all is used since there is a pinned tweet 
    #if there wasnt a pinned tweet, i'd be able to get the first result using find()

    #print(mars_weather_html[1].p.text)

    #a twitter link in embedded with the text, need to split it out
    #need to append back the pressure units: hPa
    split_weather = mars_weather_html[1].p.text.split(" ")
    split_weather.pop(-1)
    split_weather.append('hPa')

    #print(split_weather)

    merged_weather = " ".join(split_weather)

    mars_weather = merged_weather

    nasa_data_scrape['latest_mars_weather'] = mars_weather

    #print(mars_weather)

    #Visit the Mars Facts webpage
    url4 = 'https://space-facts.com/mars/'

    #use Pandas to scrape the table containing facts about the planet
    #including Diameter, Mass, etc.
    table = pd.read_html(url4)
    mars_facts_init = table[0]
    mars_facts = mars_facts_init.rename(columns={0:'Fact type', 1:'Fact Value'})
    mars_facts.set_index("Fact type", inplace=True)
    #mars_facts.head()
    mars_facts.head()

    #Use Pandas to convert the data to a HTML table string.
    mars_facts_html_table = mars_facts.to_html()
    
    #print(mars_facts_html_table)
    nasa_data_scrape['mars_facts_table'] = mars_facts_html_table


    #Visit the USGS Astrogeology site
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)
    time.sleep(10)

    hemisphere_html = browser.html

    soup_hemisphere = bs(hemisphere_html, 'html.parser')

    #all hemispheres are nicely within one type of header: h3
    list_of_hemispheres = soup_hemisphere.find_all('h3')


    #print(list_of_hemispheres)


    #dictionary list with the image url string and the hemisphere title 
    #This list will contain one dictionary for each hemisphere.
    hemisphere_image_urls = []

    link_to_images = soup_hemisphere.find_all('div', class_='description')

    #print(link_to_images[0].a['href'])
    #with a list of number of hemispheres, i can iterate each link 
    for hemisphere_num in range(len(list_of_hemispheres)):
        partial_link1 = link_to_images[hemisphere_num].a['href']
        full_link1 = f'https://astrogeology.usgs.gov{partial_link1}'
        browser.visit(full_link1)
        time.sleep(5)
        hemisphere_page_html = browser.html
        soup_each_hemisphere = bs(hemisphere_page_html, 'html.parser')
        hemisphere_title = soup_each_hemisphere.find('h2', class_='title')
        link = soup_each_hemisphere.find('li')
        title_and_link = dict({'title': hemisphere_title.text, 'img_url':link.a['href']})
        hemisphere_image_urls.append(title_and_link)
        browser.back()
        time.sleep(2)

    #obtain high resolution images for each of Mar's hemispheres.
    #You will need to click each of the links to the hemispheres 

    #Save both the image url string for the full resolution hemisphere image
    #and the Hemisphere title containing the hemisphere name. 
    # use `img_url` and `title`.
    
    #print(hemisphere_image_urls)

    nasa_data_scrape['hemisphere_name_and_img'] = hemisphere_image_urls


    browser.quit()
    return nasa_data_scrape

