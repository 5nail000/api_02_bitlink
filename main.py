import os
import requests
from dotenv import load_dotenv


def create_bitlink(url, token):

    headers = {'Authorization': f'Bearer {token}'}
    data = {'long_url': url}
    response = requests.post(f'https://api-ssl.bitly.com/v4/bitlinks',
                             headers=headers,
                             json=data)
   
    response.raise_for_status()
    return response.json()['id']


def count_clicks(bitly, token):

    if '://' in bitly: bitly = bitly.split('://')[1]    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitly}/clicks/summary',
        headers=headers)

    response.raise_for_status()
    return response.json()['total_clicks']
    

def is_bitlink(link, token):

    if '://' in link: link = link.split('://')[1]
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{link}',
        headers=headers)
    
    return response.ok


def main():

    load_dotenv()
    token = os.getenv('BITLY_TOKEN')
    user_link = input()

    if is_bitlink (user_link, token):
        print (f'Количество переходов по ссылке битли: {(count_clicks(user_link, token))}')
    else:
        print (create_bitlink(user_link, token))


if __name__ == '__main__':
    main()