# docs: https://mechanicalsoup.readthedocs.io/en/stable/

import mechanicalsoup

# an instance called browser to request the URL
browser = mechanicalsoup.Browser()

url = "http://olympus.realpython.org/login"
login_page = browser.get(url)
login_html = login_page.soup

# .select("form") return the list of all <form> element on the page
form = login_html.select("form")[0] # or login_html.form if there're only one form on the page
form.select("input")[0]["value"] = "zeus" # fill the first input value i.e user
form.select("input")[1]["value"] = "ThunderDude" # fill the second input value i.e pwd

profiles_page = browser.submit(form, login_page.url) # submit the form
list_profiles_page = profiles_page.soup.select("a") # get all of the element from tag <a>

title = profiles_page.soup.select("title")[0].text # or profiles_page.soup.title.text if there're only one title on the page

print(f"Title: {title}\n")
base_url = "http://olympus.realpython.org"
for i in range(len(list_profiles_page)):
    link = base_url + list_profiles_page[i]["href"]
    text = list_profiles_page[i].text
    print(f"{text}: {link}")