import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse
import argparse


def create_bitlink(url, token):

    headers = {'Authorization': f'Bearer {token}'}
    url = {'long_url': url}
    response = requests.post(
        f'https://api-ssl.bitly.com/v4/bitlinks',
        headers=headers,
        json=url
    )
    response.raise_for_status()
    return response.json()['id']


def count_clicks(link, token):

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{urlparse(link).netloc}{urlparse(link).path}/clicks/summary',
        headers=headers
    )
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(link, token):

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{urlparse(link).netloc}{urlparse(link).path}',
        headers=headers
    )
    return response.ok


def main():

    load_dotenv()
    token = os.getenv('BITLY_TOKEN')

    parser = argparse.ArgumentParser()
    parser.add_argument("user_link", type=str, default="",
                        help="link for bitly service")

    try:
        args = parser.parse_args()
    except:
        print('Argument is missing, needs link as argument')
    else:
        if is_bitlink(args.user_link, token):
            print(
                f'Количество переходов по ссылке битли: {(count_clicks(args.user_link, token))}')
        else:
            print(create_bitlink(args.user_link, token))


if __name__ == '__main__':
    main()
