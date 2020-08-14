# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from twitter_scraper import get_tweets


# Function to choose the executable path to driver
def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Full Scrape function.
def scrape():

    browser = init_browser()

    # Visit Nasa news url.
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    # HTML Object.
    html = browser.html

    # Parse HTML with Beautiful Soup
    news_soup = BeautifulSoup(html, "html.parser")

    # Retrieve the most recent article's title and paragraph.
    # Store in news variables.
    result = news_soup.find('div',class_="slide")
    news_title = result.find('div',class_='content_title')
    news_paragraph = result.find('div',class_='rollover_description_inner')
    news_title = news_title.text
    news_paragraph = news_paragraph.text
    # Exit Browser.
    browser.quit()

    # Print Title and Text.
    print(f'Title: {news_title}\nText: {news_paragraph}')

    """ JPL Mars Space Images - Featured Image """

    # Run init_browser/driver.
    browser = init_browser()

    # Visit the url for JPL Featured Space Image.
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    # Select "FULL IMAGE".
    browser.click_link_by_partial_text("FULL IMAGE")

    # Find "more info" for first image, set to variable, and command click.
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.links.find_by_partial_text("more info")
    more_info_element.click()

    # HTML Object.
    html = browser.html

    # Parse HTML with Beautiful Soup
    image_soup = BeautifulSoup(html, "html.parser")

    # Scrape image URL.
    image_url = image_soup.find("figure", class_="lede").a["href"]

    # Concatentate https://www.jpl.nasa.gov with image_url.
    featured_image_url = f'https://www.jpl.nasa.gov{image_url}'

    # Exit Browser.
    browser.quit()

    # Print Faetured Image URL.
    print(featured_image_url)

    """ Mars Weather """

    # Run init_browser/driver.
    browser = init_browser()

    # Visit Nasa news url.
    tweet_url = "https://twitter.com/MarsWxReport"
    browser.visit(tweet_url)

    # HTML Object.
    html = browser.html

    # Parse HTML with Beautiful Soup
    twitter_soup = BeautifulSoup(html, "html.parser")

    # Retrieve the most recent article's title and paragraph.
    # Store in news variables.
    result = twitter_soup.find('div',{"data-testid":"tweet"})
    mars_weather = result.find("div",class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    result = result.find('div',class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")

    mars_weather = result.text
    mars_weather = mars_weather.replace("Mars Weather@MarsWxReport·12h","")


    # Exit Browser.
    browser.quit()

    # Print most recent Mars Weather.
    print(mars_weather)

    """ Mars Facts """
    browser = init_browser()
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_facts = mars_data.to_html(header = False, index = False)
    browser.quit()

    """ Mars Hemispheres """

    browser = init_browser()
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    hemisphere_image_urls = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    browser.quit()

    print(hemisphere_image_urls)

    """ Mars Data Dictionary - MongoDB """

    # Create empty dictionary for all Mars Data.
    mars_data = {}

    # Append news_title and news_paragraph to mars_data.
    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_paragraph

    # Append featured_image_url to mars_data.
    mars_data['featured_image_url'] = featured_image_url

    # Append mars_weather to mars_data.
    mars_data['mars_weather'] = mars_weather

    # Append mars_facts to mars_data.
    mars_data['mars_facts'] = mars_facts

    # Append hemisphere_image_urls to mars_data.
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    print("Scrape Complete!!!")

    return mars_data