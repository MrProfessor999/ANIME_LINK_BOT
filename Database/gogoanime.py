import requests
from bs4 import BeautifulSoup
from animeSupport import PRIMARY_URL, SEARCH_URL

mozhdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}


def anime_search(anime_name):
    animes = []
    url = PRIMARY_URL + SEARCH_URL + anime_name
    page_get = requests.get(url, headers=mozhdr)
    soupdata = BeautifulSoup(page_get.text, "lxml")
    allDivs = soupdata.findAll("div", attrs={'class': 'img'})
    for x in allDivs:
        link_current = PRIMARY_URL + x.find('a')['href']
        title = x.find('a')['title']
        img = x.find('img')['src']
        animes.append({
            "name": title,
            "link": link_current,
            "img": img
        })
    return animes


def download_episode(link, ep_no):
    anime_name = link.split('/')[-1]
    mod_link = PRIMARY_URL + '/' + anime_name + '-episode-' + str(ep_no)
    page_get = requests.get(mod_link, headers=mozhdr)
    soupdata = BeautifulSoup(page_get.text, "lxml")
    allDivs = soupdata.findAll("div", attrs={'class': 'favorites_book'})
    for x in allDivs:
        link_download_site = x.find('a')['href']
    return link_download_site
