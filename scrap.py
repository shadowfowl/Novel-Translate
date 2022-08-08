import requests
from bs4 import BeautifulSoup as bs
import html2text as h2t
import urllib.parse as urll

def scrap(url):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
    req = requests.get(url, headers=headers, timeout=5.0)
    print("Starting Request ...")
    print("Request: %s" %req)
    print("...")
    return (bs(req.content,'html.parser'))
    

url = "https://wuxiaworldsite.com/novel/the-s-classes-that-i-raised/chapter-2/"
print("Link to Scrap: %s" %url)

soup = scrap(url)
novel = soup.find("div", {"class":"text-left"})

print("Chapter Scrap completed")

h = h2t.HTML2Text()
h.ignore_links = True

text = h.handle(str(novel))
text = text.replace("\n","*brk")

print("Converting to Translate API Format")

urltext = urll.quote(text)

print("Saving Scrap")

with open('./inputs.temp','w') as f:
    f.truncate(0)
    f.write(urltext)

print("Scrap Completed")

