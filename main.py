import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse


def create_bitlink(url, token):

    headers = {'Authorization': f'Bearer {token}'}
    post_data = {'long_url': url}
    response = requests.post(f'https://api-ssl.bitly.com/v4/bitlinks',
                             headers=headers,
                             json=post_data)
   
    response.raise_for_status()
    return response.json()['id']


def count_clicks(link, token):

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{urlparse(link).netloc}{urlparse(link).path}/clicks/summary',
        headers=headers)
        
    response.raise_for_status()
    return response.json()['total_clicks']
    

def is_bitlink(link, token):

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{urlparse(link).netloc}{urlparse(link).path}',
        headers=headers)
    return response.ok


def main():

    load_dotenv()
    token = os.getenv('BITLY_TOKEN')
    user_link = input('Введите ссылку: ')

    if is_bitlink (user_link, token):
        print (f'Количество переходов по ссылке битли: {(count_clicks(user_link, token))}')
    else:
        print (create_bitlink(user_link, token))


if __name__ == '__main__':
    main()