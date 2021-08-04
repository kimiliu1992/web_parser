import sys
import subprocess

# pip install custom package to /tmp/ and add to path
subprocess.call('pip install beautifulsoup4 -t /tmp/ --no-cache-dir'.split(), stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
subprocess.call('pip install requests -t /tmp/ --no-cache-dir'.split(), stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
subprocess.call('pip install twilio -t /tmp/ --no-cache-dir'.split(), stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
sys.path.insert(1, '/tmp/')

from bs4 import BeautifulSoup
import requests
from twilio.rest import Client
from datetime import datetime


def send_message(instock=False):
    account_sid = "***Twillo account***"
    auth_token = "***Twillo token***"
    client = Client(account_sid, auth_token)
    current_time = datetime.strftime(datetime.now(), format="%Y-%m-%d %H:%M:%S EST")

    if instock:
        _ = client.messages \
            .create(
            body="It is in stock! Check out at {}".format(
                "website"),
            from_='***Twillo number***',
            to='***Your phone number***'
        )
    else:
        _ = client.messages \
            .create(
            body="It is out of stock at {}".format(current_time),
            from_='***Twillo number***',
            to='***Your phone number***'
        )


def lambda_handler(event, context):
    URL = "***website***"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        result = soup.find("a", {"href": "/collections/out-of-stock"})
        content = result.contents
    except AttributeError:
        content = None

    if content is None or content[0] != 'Out of Stock':
        send_message(instock=True)
    else:
        pass
        # send_message(instock=False)
