import requests
from bs4 import BeautifulSoup
from datetime import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}

def main():
    #scrap('http://investor.koufu.com.sg/newsroom.html', 'http://investor.koufu.com.sg','http://investor.koufu.com.sg','div','ir_home_news_list')
    #scrap('https://sginvestors.io/sgx/stock/1d0-kimly/company-announcement', '','https://links.sgx.com','div','corpannouncementitem list-group-item')
    #scrap('https://www.talkmed.com.sg/category/announcements/', '','','p','news-listing-title')
    scrap_sginvestors(company='5g3-talkmed')

def scrap_sginvestors(company: str, last_updated :datetime=datetime.now() ):
    response = requests.get(f'https://sginvestors.io/sgx/stock/{company}/company-announcement')
    soup = BeautifulSoup(response.content, 'html.parser')
    news = soup.findAll('div', {'class': 'corpannouncementitem list-group-item'})

    for n in news:
        link = n.find('a')
        title = n.a['title']
        date = n.find('div', {'class': 'data_stamp'}).text.split()[0]
        time = n.find('div', {'class': 'data_stamp'}).text.split()[1]
        date_time_obj = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S')
        if last_updated == None or date_time_obj > last_updated:
            news_url = link['href']
            response = requests.get(news_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            for a in soup.select('a[href$=".pdf"]'):
                r = requests.get('https://links.sgx.com' + a['href'], allow_redirects=True)
                open(a['href'].split('/')[-1], 'wb').write(r.content)
        else:
            break
        
def scrap_general(site, news_prefix, pdf_prefix, wrapper, css_class):
    response = requests.get(site, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    news = soup.findAll(wrapper, {'class': css_class})
    link = news[0].find('a')
    title = link.text
    news_url = link['href']
    response = requests.get(news_prefix + news_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    for a in soup.select('a[href$=".pdf"]'):
        r = requests.get(pdf_prefix + a['href'], allow_redirects=True)
        open(a['href'].split('/')[-1], 'wb').write(r.content)
    

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

def talkmed():
    url_talkmed = 'https://www.talkmed.com.sg/category/announcements/'
    response = requests.get(url_talkmed, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    #print(soup.prettify())
    news = soup.findAll('p', {'class': 'news-listing-title'})
    print(news[0])
    response = requests.get(news[0].a['href'] , headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    for a in soup.select('a[href$=".pdf"]'):
        print(a['href'])
        r = requests.get(a['href'], allow_redirects=True)
        open(a['href'].split('/')[-1], 'wb').write(r.content)

if __name__ == "__main__":
    main() 