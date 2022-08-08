import requests
from bs4 import BeautifulSoup as bs
import html2text as h2t
import urllib.parse as urll
import requests
import json


def translate(text):
    url = "https://nlp-translation.p.rapidapi.com/v1/translate"
    langfrom = "en"
    langto = "pt"

    payload = ('text=%s&to=%s&from=%s' %(text, langto, langfrom))
    headers = {
	    "content-type": "application/x-www-form-urlencoded",
	    "X-RapidAPI-Key": "22f2beb1e2msh265267a744dd9dbp140be9jsn258c847b6a82",
	    "X-RapidAPI-Host": "nlp-translation.p.rapidapi.com"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    
    post_return = json.loads(response.text)
    
    translated = ((post_return["translated_text"])["%s"%langto])
    print('...')
    return (translated)


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
novel = soup.find("div", {"class":"text-left"}) #Div with text on wuxiaworldsite.com novel pages

print("Chapter Scrap completed")

h = h2t.HTML2Text() #Define a var to converting HTLM to text format (without tags <p> and <div>)
h.ignore_links = True #Remove hiperlinks

text = h.handle(str(novel)) #converting
text = text.replace("\n","*brk") #replacing break line, to not have problems when the URL encoded return

print("Converting to Translate API Format")

urltext = urll.quote(text) # converting to URL encoded

print("Saving Scrap")

with open('./inputs.temp','w') as f:
    f.truncate(0)
    f.write(urltext)

print("Scrap Completed")

print("Starting Translate")
with open('./inputs.temp', 'r') as inputs:
    text_input = inputs.read()

output = "" #empty string to save the API return
print("Getting Translated Text")

while len(text_input) > 1000: # breaking in 1000 characters per POST, is a API limit in Free plan
    output =  output + (translate(text_input[:1000]))
    text_input = text_input[1000:]

output =  output + (translate(text_input[:1000]))

output = output.replace("*brk","\n") # return *brk as break line after convert backs to text string
print("Saving file output.txt")

with open('./output.txt', 'w') as out:
    out.truncate(0)
    out.write(output)

print("Translate Completed")
