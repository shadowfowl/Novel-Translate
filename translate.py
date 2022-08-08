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


print("Starting Translate")
print("Open Scrap Input")
with open('./inputs.temp', 'r') as inputs:
    text_input = inputs.read()

output = ""
print("Getting Translated Text")

while len(text_input) > 1000:
    output =  output + (translate(text_input[:1000]))
    text_input = text_input[1000:]

output =  output + (translate(text_input[:1000]))

output = output.replace("*brk","\n")
print("Saving file output.txt")

with open('./output.txt', 'w') as out:
    out.truncate(0)
    out.write(output)

print("Translate Completed")
