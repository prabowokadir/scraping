import mechanicalsoup
import time

browser = mechanicalsoup.Browser()

url = "http://olympus.realpython.org/dice"
page = browser.get(url)
html = page.soup

for i in range(4):
    title = html.title.text
    result = html.h2.text
    timestamp_utc = html.select("p")[1].text

    print(f"Result is {result} and running at {timestamp_utc}")

    # Wait 5 seconds if this isn't the last request
    if  i < 3:
        time.sleep(5)