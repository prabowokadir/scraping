import re
from urllib.request import urlopen # function to open an URL

url = "http://olympus.realpython.org/profiles/dionysus" # URL page
page = urlopen(url)
html_bytes = page.read() # extract HTML from the page, return a sequence of bytes
html = html_bytes.decode("utf-8") # to decode the bytes to a string using UTF-8

# get the title of HTML

# <title.*?> berarti karakter awalnya <title dan setelahnya bisa karakter apa aja dengan jumlah zero atau lebih hingga >
pattern = "<title.*?>.*?</title.*?>"
match_results = re.search(pattern, html, re.IGNORECASE)
title = match_results.group()
title = re.sub("<.*?>", "", title)

print(title)