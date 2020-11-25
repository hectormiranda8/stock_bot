from bs4 import BeautifulSoup
from termcolor import colored
import asyncio
import random
import re
import requests
import sys
import time
import webbrowser

URL_NEWEGG = []
URL_NEWEGG_COMBOS = []

firefox_header = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'}
chrome_header = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                               'Chrome/87.0.4280.66 Safari/537.36'}

avail_stock_firefox = []
avail_stock_chrome = []

availability = [avail_stock_firefox, avail_stock_chrome]

webbrowser.register('firefox', None,
                    webbrowser.BackgroundBrowser("C://Program Files//Mozilla Firefox//firefox.exe"))
webbrowser.register('chrome', None,
                    webbrowser.BackgroundBrowser("C://Program Files//Google//Chrome//Application//chrome.exe"))


async def check_url_newegg_single(url):
    page = requests.get(url, headers=firefox_header)
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup)
    name = str(newegg_name(soup))
    print("\nProduct: " + name)
    instock = newegg_instock(str(soup))
    if instock:
        text = colored("In stock: " + str(instock), 'green')
        print(text)
        price = str(newegg_price(soup))
        print("Price: " + price)
        avail_stock_firefox.append(url)
    else:
        text = colored("In stock: " + str(instock), 'red')
        print(text)


async def check_url_newegg_combo(url):
    page = requests.get(url, headers=firefox_header)
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup)
    print("\nProduct: " + str(newegg_name_combo(soup)))
    instock = newegg_instock_combo(str(soup))
    if instock:
        text = colored("In stock: " + str(instock), 'green')
        print(text)
        price = str(newegg_price_combo(soup))
        print("Price: " + price)
        avail_stock_firefox.append(url)
    else:
        text = colored("In stock: " + str(instock), 'red')
        print(text)


def newegg_instock(soup):
    display = "OUT OF STOCK"
    if soup.find(display) != -1:
        return False
    return True


def newegg_instock_combo(soup):
    display = "class=\"note\">OUT OF STOCK"
    if soup.find(display) != -1:
        return False
    return True


def newegg_price(soup):
    unformat_price = str(soup.find(class_="list_price")).split(">")
    price = re.findall(r"[-+]?\d*\.\d+|\d+", unformat_price[1])
    return "$" + price[0]


def newegg_price_combo(soup):
    data = str(soup.find(class_="current")).split("\n")
    price = re.findall(r"\d+\.\d+", data[0])
    # print(data)
    # print(price)
    return "$" + price[0]


def newegg_name(soup):
    unformat_name = str(soup.find(class_="name")).split(">")
    return unformat_name[1].split("<")[0]


def newegg_name_combo(soup):
    data = str(soup.find(class_="wrapper")).split("\n")
    line = re.findall(r"\"name\">.*</span", data[1])
    name = re.findall(r">.*<", line[0])
    size = len(name[0])
    name = name[0][1:size-1]
    # print(name)
    return name

async def check_newegg():
    tasks = []
    for url in URL_NEWEGG:
        tasks.append(asyncio.ensure_future(check_url_newegg_single(url)))
    for url in URL_NEWEGG_COMBOS:
        tasks.append(asyncio.ensure_future(check_url_newegg_combo(url)))
    await asyncio.gather(*tasks)


def add_urls():
    file = open("../urls/urls_newegg.txt", "r")
    for url in file:
        if url.startswith("https"):
            URL_NEWEGG.append(url)
    file = open("../urls/urls_newegg_combos.txt", "r")
    for url in file:
        if url.startswith("https"):
            URL_NEWEGG_COMBOS.append(url)


def main():
    add_urls()
    while True:
        loop = asyncio.get_event_loop()
        start = time.time()
        try:
            loop.run_until_complete(check_newegg())
        finally:
            end = time.time() - start
            print("\nTime to execute: %.4f" % end, "secs\n")
            for url in avail_stock_firefox:
                webbrowser.get('firefox').open(url)
            # for url in avail_stock_chrome:
            #     webbrowser.get('chrome').open(url)
            close = False
            for stock_list in availability:
                if len(stock_list) > 0:
                    text = colored("STOCK FOUND!", 'green')
                    print(text)
                    for stock in stock_list:
                        print(stock)
                    close = True
            time_to_wait = random.randint(10, 30)
            print("\nTime to refresh or close: " + str(time_to_wait) + " seconds")
            time.sleep(time_to_wait)
            #close = True
            if close:
                print("Closing bot.")
                sys.exit(0)
            print("Refreshing...\n")


if __name__ == '__main__':
    main()

# async def myCoroutine(num):
#     process_time = random.randint(1, 5)
#     await asyncio.sleep(process_time)
#     print("Coroutine {}, has successfully completed after {} seconds.".format(num, process_time))
#
#
# async def dummymain():
#     tasks = []
#     for i in range(10):
#         tasks.append(asyncio.ensure_future(myCoroutine(i)))
#     await asyncio.gather(*tasks)
#
#
# loop = asyncio.get_event_loop()
# start = time.time()
# try:
#     loop.run_until_complete(main())
# finally:
#     loop.close()
# end = time.time() - start
# print("Time to execute: %.4f" % end, "secs")
