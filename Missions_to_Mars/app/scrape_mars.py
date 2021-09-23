#import modules
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
from selenium import webdriver

def scrape():
    #link to chromedriver.exe
    executable_path = {'executable_path':'chromedriver'}

    #function that opens browser, parses html, and closes browser
    def parse(url):
        with Browser('chrome',**executable_path) as browse:
            browse.visit(url)
            html = browse.html

            return bs(html, 'html.parser')

    #html for mars news
    marsite = "https://redplanetscience.com/"

    marsoup = parse(marsite)

    #scrape title and summary of feature news article
    titles = marsoup.find_all('div', class_="content_title")
    html_news = titles[0]
    news_title = html_news.text

    html_pgrph = html_news.findNextSibling()
    news_pgrph = html_pgrph.text

    #html for mars images
    featurl = "https://spaceimages-mars.com/"

    imgsoup = parse(featurl)

    #scrape featureimage
    imgs = imgsoup.find_all('img')
    srcs = []
    for im in imgs:
        srcs.append(im['src'])
    urlend = srcs[1]
    urlend

    #concatenate the image page url with the feature image suffix
    featimg_url = featurl + urlend

    #html for mars fact tables
    factsurl = "https://galaxyfacts-mars.com/"

    tables = pd.read_html(factsurl)

    #grab table 0 with pandas
    marscompare = tables[0].set_index(tables[0][0])
    marscompare.drop(columns=0,inplace=True)
    marscompare.rename(columns = {1: "Mars", 2: "Earth"},inplace=True)
    marscompare.drop("Mars - Earth Comparison",inplace=True)
    marscompare.index.name = "Mars - Earth Comparison"
    marscomparehtml = marscompare.to_html().replace("\n", '')

    #grab table 1 with pandas
    marsfcts = tables[1].set_index(tables[1][0])
    marsfcts.drop(columns=0,inplace=True)
    marsfcts.rename(columns = {1: "Mars"},inplace=True)
    marsfcts.index.name = "Mars Facts"
    marsfctshtml = marsfcts.to_html().replace("\n", '')

    #html of hemisphere page
    geourl = "https://marshemispheres.com/"
    geohtml = parse(geourl)

    #scrape the links for the full-size image pages
    linkhref = []
    for link in geohtml.findAll("a",class_="itemLink product-item"):
        linkhref.append(link["href"])
    for href in linkhref:
        i = linkhref.index(href)
        if href in [linkhref[j] for j in range(0,len(linkhref)) if j != i]:
            del linkhref[i]
    del linkhref[-1]

    hrefname = []
    for href in linkhref:
        name = href[0:-5]
        hrefname.append(name)

    #get html for each full-size image page
    htmls = dict.fromkeys(hrefname)
    for href in hrefname:
        with Browser('chrome', **executable_path) as browse:
            browse.visit(geourl+href+'.html')
            htmls[href] = bs(browse.html,'html.parser')

    #scrape the title and img url from the full-size image pages
    hemimglinks = dict.fromkeys(hrefname)
    for i in range(4):
        titles = dict.fromkeys(['title','img_url'])
        a = htmls[hrefname[i]].find('a',text='Sample')
        h2 = htmls[hrefname[i]].find('h2', class_="title")
        titles['title'] = h2.text
        titles['img_url'] = geourl+a['href']
        hemimglinks[hrefname[i]] = titles
    
    scrapedict = {'headline': news_title, "news": news_pgrph, 'featured_img': featimg_url,'table1': str(marscomparehtml), "table2": str(marsfctshtml), 'hemispheres': hemimglinks}
 
    return scrapedict

