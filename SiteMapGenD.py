import requests
from bs4 import BeautifulSoup
import re

def cercaUrl(url, filtro, stringUrl):
    links= []
    httpUrl = url
    try:
        req =  requests.get(url, verify='gd_bundle-g2.crt')
    except:
        req =  requests.get(httpUrl, verify='gd_bundle-g2.crt')
    content = req.content

    soup= BeautifulSoup(content,"html.parser")

    all_a_tags = soup.findAll('a', href=True)

    if len(all_a_tags) < 5:
        try:
            soupJs= BeautifulSoup(content,"html.parser")
            all_a_tags = soupJs.findAll('a', href=True)
        except:
            pass

 
    for link in all_a_tags:
        try:
            if filtro in link.get('href') and "mailto" not in link.get('href'):
                links.append(link.get('href'))
            elif filtro not in link.get('href'):
                if "http" not in link.get('href'):
                    if link.get('href').startswith('/'):
                        links.append(stringUrl + link.get('href'))
                    elif re.match(r'^[a-z]',link.get('href')):
                        links.append(stringUrl + "/" + link.get('href'))
                    elif re.match(r'^tel',link.get('href')):
                        links.append(stringUrl + "/" + link.get('href'))
                    elif re.match(r'#',link.get('href')):
                        continue       
        except:
            print('[-] error : ' + link)
            continue
    return links

def cercaUrl2(lista, filtro, stringUrl):
    lista_url=[]
    lista_url.extend(lista)
    gia_controllati=[]
    url_finali = []
    ind = -1
    while len(gia_controllati) < len(lista_url):
        gia_controllati.append(lista_url[ind])
        ind = ind + 1
        print('[+] Founded ' + str(len(gia_controllati)) + ' urls')
        print(len(gia_controllati))
         
        if lista_url[ind] in gia_controllati:
            print('[+] Already present: ' + lista_url[ind] )
        else:
            try:
                new_link = cercaUrl(lista_url[ind],filtro, stringUrl)
                url_finali.append(lista_url[ind])
                print(len(lista_url))
                print(lista_url[ind])
                for i in new_link:
                    if i not in lista_url:
                        lista_url.append(i)
            except TypeError:
                pass
    return url_finali

def stampaXml(elenco_url, nome_file = "sitemap"):
    with open (nome_file + ".xml", "w") as fileXml:
        fileXml.write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

        print('[+] Writing file XML:')

        for i in elenco_url:
            print(len(elenco_url) - elenco_url.index(i))
            fileXml.write('<url>\n')
            fileXml.write('<loc>' + i + '</loc>\n')
            fileXml.write(' </url>\n')
            
        fileXml.write('</urlset>\n')
        print('[+] Completed!')


print(f"""
   _____ _ __       __  ___            ______           ____ 
  / ___/(_) /____  /  |/  /___ _____  / ____/__  ____  / __ *
  \__ \/ / __/ _ \/ /|_/ / __ `/ __ \/ / __/ _ \/ __ \/ / / /
 ___/ / / /_/  __/ /  / / /_/ / /_/ / /_/ /  __/ / / / /_/ / 
/____/_/\__/\___/_/  /_/\__,_/ .___/\____/\___/_/ /_/____ * 
                            /_/
""")

print("Version 1.2\n [+] Developed by Daniele Asteggiante® in 2021 (ver. 1.0), update in 2022 (ver. 1.1) and 2023 (ver. 1.2)\n\n")

print(f"[!] Do Not Support JavaScript generated pages.\nIf you need this update, please contact me at github link -> https://github.com/danieleasteggiante")
print(f"[!] Insert COMPLETE url (ex. https://www.site.com). \n[!!!] IMPORTANT! Do not forget third level domain (ex. 'www.site.com' or 'something.site.com')")
print(f"[!!!] IMPORTANT! Do not forget https:// or http://.site.com')")
print(f"[!!!] IMPORTANT! Do not forget to have in the same folder of SiteMapGenD.exe file the SSL certificate (ex.'certificate.crt)\n\n")

url = input('[+] Insert url COMPLETE (ex. https://www.site.com or https://something.site.com):')
filename = input('[+] Name of file .xml (ex. sitemap)')
filtro = url.split("//")[1]
stringUrl = url
elenco_home = cercaUrl(url,filtro, stringUrl)
elenco_sito = cercaUrl2(elenco_home,filtro, stringUrl)
print('\n\n')
stampaXml(elenco_sito,filename)



