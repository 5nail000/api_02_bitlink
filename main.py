import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse
import argparse


def create_bitlink(url, token):

    headers = {'Authorization': f'Bearer {token}'}
    long_url = {'long_url': url}
    response = requests.post(
        f'https://api-ssl.bitly.com/v4/bitlinks',
        headers=headers,
        json=long_url
    )
    response.raise_for_status()
    return response.json()['id']


def count_clicks(link, token):

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary',
        headers=headers
    )
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(link, token):

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{link}',
        headers=headers
    )
    return response.ok


def main():

    load_dotenv()
    token = os.getenv('BITLY_TOKEN')

    parser = argparse.ArgumentParser()
    parser.add_argument("user_link", help="link for bitly service")
    args = parser.parse_args()
    parsed_link = urlparse(args.user_link)
    prepared_link = f'{parsed_link.netloc}{parsed_link.path}'

    if is_bitlink(prepared_link, token):
        print(
            f'Количество переходов по ссылке битли: {(count_clicks(prepared_link, token))}')
    else:
        print(create_bitlink(args.user_link, token))


if __name__ == '__main__':
    main()