import mechanicalsoup

browser = mechanicalsoup.Browser()

url = "https://www.mlb.com/stats"
page = browser.get(url)
html = page.soup

team = html.find_all("span")

print(team)