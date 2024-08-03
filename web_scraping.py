import re
from urllib.request import urlopen # function to open an URL

url = "http://olympus.realpython.org/profiles/dionysus" # URL page
page = urlopen(url)
html_bytes = page.read() # extract HTML from the page, return a sequence of bytes
html = html_bytes.decode("utf-8") # to decode the bytes to a string using UTF-8

# get the title of HTML

# <title.*?> berarti karakter awalnya <title dan setelahnya bisa karakter apa aja dengan jumlah zero atau lebih hingga >
for string in ["Profile: ", "Name: ", "Favorite Color: "]:
    string_start_idx = html.find(string)
    text_start_idx = string_start_idx + len(string)

    next_html_tag_offset = html[text_start_idx:].find("<")
    text_end_idx = text_start_idx + next_html_tag_offset

    raw_text = html[text_start_idx:text_end_idx]
    clean_text = raw_text.strip(" \r\n\t")
    print(clean_text)