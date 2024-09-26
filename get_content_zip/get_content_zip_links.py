"""
Instructions:

1. After you copy the code to your local machine, fill the portal_token and get_links_token.

2. When you wonna get the content zip file links, fill in the email and languageIds list and run the script, you will get a csv.

"""

import requests
import pandas as pd

portal_token = "your_portal_token"

get_links_token = "get_links_token"

email = "customer_email"

languageIds = ["125", "126"]


def get_products(languageId):
    headers = {
        "accept": "*/*",
        "accept-language": "en,zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7",
        "authorization": f"Bearer {portal_token}",
        "origin": "https://portal.pimsleur.com",
        "priority": "u=1, i",
        "referer": "https://portal.pimsleur.com/",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    }

    params = {
        "page": "0",
        "size": "10",
        "productTypes": "SINGLE_LEVEL",
        "languageId": "122",
        "isPremium": "false",
        "sort": "lastModifiedDate,DESC",
    }

    response = requests.get(
        "https://portal.api.pimsleur.com/products", params=params, headers=headers
    )

    products = response.json().get("content")

    products.sort(key=lambda x: x["productName"])

    return products


def get_links(isbn, email):
    headers = {
        "Content-Type": "application/json",
        "token": get_links_token,
    }
    json_data = {
        "isbn": isbn,
        "hasCreatePermission": False,
        "email": email,
        "effectiveTime": 864000000,
    }

    response = requests.post(
        "https://entitlement.api.pimsleur.com/prod/content-zip",
        headers=headers,
        json=json_data,
    )

    return response.json()


products = []
for languageId in languageIds:
    products += get_products(languageId)

products_info = []
for product in products:
    products_info.append(
        {
            "isbn": product["isbn"],
            "courseLevel": product["course"]["courseLevel"],
            "languageName": product["languageName"],
        }
    )

for product in products_info:
    product["link"] = ""
    try:
        links = get_links(product["isbn"], email)
        product["link"] = links[0]
    except:
        pass

df = pd.DataFrame(products_info)

df.to_csv("output.csv", index=False)
