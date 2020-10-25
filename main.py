import requests
from bs4 import BeautifulSoup

soup = BeautifulSoup("<html>a web page</html>", 'html.parser')
def main():
    print("main starting")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    response = requests.get("http://investor.koufu.com.sg/newsroom.html", headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup.prettify())

if __name__ == "__main__":
    main() 