import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}

def main():
    print("Getting koufu")
    #koufu()
    kimly()

def koufu():
    url_koufu = 'http://investor.koufu.com.sg'
    response = requests.get(url_koufu + "/newsroom.html", headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    news = soup.findAll('div', {'class': 'ir_home_news_list'})
    link = news[0].find('a')
    title = link.text
    news_url = link['href']
    response = requests.get(url_koufu + news_url, headers=headers)
    print(url_koufu + news_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for a in soup.select('a[href$=".pdf"]'):
        r = requests.get(url_koufu + a['href'], allow_redirects=True)
        open(a['href'].split('/')[-1], 'wb').write(r.content)

def kimly():
    url_kimly = 'https://sginvestors.io/sgx/stock/1d0-kimly/company-announcement'
    response = requests.get(url_kimly , headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    #print(soup.prettify())
    news = soup.findAll('div', {'class': 'corpannouncementitem list-group-item'})
    #print(news[0])
    response = requests.get(news[1].a['href'] , headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    for a in soup.select('a[href$=".pdf"]'):
        print(a['href'])
        r = requests.get("https://links.sgx.com"+a['href'], allow_redirects=True)
        open(a['href'].split('/')[-1], 'wb').write(r.content)
    #print(news)

if __name__ == "__main__":
    main() 