import requests
from bs4 import BeautifulSoup
import smtplib
import os

PRODUCT_URL ="https://www.amazon.co.uk/LEGO-76389-Anniversary-Collectible-Minifigure/dp/B08WWRJ2QJ/ref=sr_1_5?dchild=1&keywords=harry+potter+lego&qid=1635321175&sr=8-5"
ACCEPT_LANGUAGE = "en-US,en;q=0.9"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30"

SMTP_ADDRESS = "smtp.gmail.com"
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL")

headers = {
    "Accept-Language": ACCEPT_LANGUAGE,
    "User-Agent": USER_AGENT

}

response = requests.get(PRODUCT_URL, headers=headers).text

soup = BeautifulSoup(response, "html.parser")
product = soup.find(class_="a-size-large product-title-word-break").getText()
price = float(soup.find(class_="a-offscreen").getText().split("£")[1])
max_pay = 200

message = f"Subject: Price tracker of Harry Potter Lego\n\nThe price of {product} has dropped to £{price}.\n Find it at {PRODUCT_URL}".encode("utf-8")

if price < max_pay:
    with smtplib.SMTP(SMTP_ADDRESS,  port=587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=TO_EMAIL,
            msg=message
        )
else:
    pass

