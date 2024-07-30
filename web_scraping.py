from urllib.request import urlopen # function to open an URL

url = "http://olympus.realpython.org/profiles/aphrodite" # URL page
page = urlopen(url)
html_bytes = page.read() # extract HTML from the page, return a sequence of bytes
html = html_bytes.decode("utf-8") # to decode the bytes to a string using UTF-8

# get the title of HTML
title_index = html.find("<title>") # .find() will return the index of the first occurrence of a substring
start_index = title_index + len("<title>")
end_index = html.find("</title>")
title = html[start_index:end_index]

print(title)