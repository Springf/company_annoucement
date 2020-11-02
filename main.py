import requests
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import json
import boto3

def lambda_handler(event, context):
    companies = event['tickers']
    #companies = ['d05-dbs']
    yesterday = datetime.today() - timedelta(days=1)
    for company in companies:
        scrap_sginvestors(company=company, last_updated=yesterday)
    return {
        'statusCode': 200,
        'body': 'success'
    }

def scrap_sginvestors(company: str, last_updated :datetime=datetime.now() ):
    response = requests.get(f'https://sginvestors.io/sgx/stock/{company}/company-announcement')
    soup = BeautifulSoup(response.content, 'html.parser')
    news = soup.findAll('div', {'class': 'corpannouncementitem list-group-item'})

    sns = boto3.client('sns')
    
    for n in news:
        link = n.find('a')
        title = n.a['title']
        date = n.find('div', {'class': 'data_stamp'}).text.split()[0]
        time = n.find('div', {'class': 'data_stamp'}).text.split()[1]
        date_time_obj = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S')
        print(f'{company} last announcement @ {date_time_obj}')
        
        if last_updated == None or date_time_obj > last_updated:
            news_url = link['href']
            
            response = sns.publish(
                TopicArn='arn:aws:sns:ap-southeast-1:872764013972:company_annoucement',    
                Message= news_url,
                Subject = f'{company} - {title}'[:100]
            )
            print(f'Sent: {response}')
        else:
            break