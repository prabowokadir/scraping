import mechanical_soup

browser = mechanical_soup.browser()

url = "http://olympus.realpython.org/login"
page = browser.get(url)

print(page)