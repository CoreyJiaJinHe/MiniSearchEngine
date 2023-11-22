# Importing Python libraries
import bs4 as BeautifulSoup
import urllib.request 
import os.path
import re
import Levenshtein as lev

countries=[]
url=['https://en.wikipedia.org/wiki/Canada',
    'https://en.wikipedia.org/wiki/China',
        'https://en.wikipedia.org/wiki/United_States', 
         'https://en.wikipedia.org/wiki/Korea',
        'https://en.wikipedia.org/wiki/United_Kingdom', 
        'https://en.wikipedia.org/wiki/France',
        'https://en.wikipedia.org/wiki/Turkey',
        'https://en.wikipedia.org/wiki/Italy'] #'''
for count in range(len(url)):
    country=url[count]
    country=country[country.rindex('/')+1:]
    countries.append(country)

filelinks=[]
#make file links
for count in range(len(countries)):
    filelinks.append((str(countries[count]))+".html")


#scrape wikipedia
def scrape_wikipedia():
    for count in range (len(url)):
        get_data = urllib.request.urlopen(url[count])

        html = get_data.read()
        parse_page = BeautifulSoup.BeautifulSoup(html,'html.parser')

        with open(((str(countries[count]))+".html"), "w", encoding = 'utf-8') as file: 
            file.write(str(parse_page.prettify()))
    del html




descriptioncontent=[]
#store the first description paragraphs
for count in range (len(url)):
    with open(filelinks[count], encoding='utf8') as html:
        parse_page = BeautifulSoup.BeautifulSoup(html, 'html.parser')

    allparagraphs=parse_page.find_all('p')
    page_content=''
    thefirstparagraph=[]
    # Looping through each of the paragraphs and adding them to the variable
    for p in allparagraphs:
        if not(p.text=='' or p.text=='\n'):
            page_content += p.text
            page_content=page_content.lstrip("\n")
            x=p.text.replace("\n",'')
            x=re.sub(r'\s+',' ',x)
            x=re.sub(r'\s+\.','.',x)
            x=re.sub(r'\s+\,',',',x)
            x=x.strip()
            thefirstparagraph.append(str(x))
    if (count== 4 or count==5 or count==7):
        descriptioncontent.append(str(thefirstparagraph[1]))
    else:
        descriptioncontent.append(str(thefirstparagraph[0]))
    page_content=[]
del thefirstparagraph
del allparagraphs
del parse_page
del x
del BeautifulSoup

#display first paragraph descriptions
'''def print_page_descriptions():
    for count in range(len(descriptioncontent)):
        print(descriptioncontent[count])
        print("\n")'''


#create inverted word index
firstline=""
wordindex=dict()
for firstpage in range(len(descriptioncontent)):
    firstline=str(descriptioncontent[firstpage])
    bracket=["(", "[","  "]
    for bracket in firstline:
        if (re.search(r'\(.*\)',firstline)):
            firstline=firstline[0:firstline.index("(")] +" "+ firstline[firstline.index(")")+1:]
        if (re.search(r'\[.*\]',firstline)):
            firstline=firstline[0:firstline.index("[")] +" "+ firstline[firstline.index("]")+1:]
        firstline=re.sub(r'\s{2}','',firstline)
    firstline=re.sub(r"'s|\.|\," ,'',firstline)
    firstline=re.sub(r"\-",' ',firstline)
    firstline=firstline.lower()
    linesplit=firstline.split(" ")
    for word in range(len(linesplit)):
        if (not wordindex or not (linesplit[word] in wordindex)):
            wordindex[linesplit[word]]=[[firstpage,word]]
        else:
            oldwordindex=(wordindex[linesplit[word]])
            oldwordindex.append([firstpage,word])
            wordindex[linesplit[word]] = oldwordindex
del firstline
del oldwordindex
        
#clean index of small copulas
uselesswords={'is', 'its','a','in','and','are','any','an','as','at','the'}
for k in uselesswords:
    wordindex.pop(k,None)
del uselesswords

#make an index of occurrence frequency using the inverted index
wordcount=dict()
for k in wordindex:
    wordindexvaluelist=(wordindex[k])
    wordcount[k]=len(wordindexvaluelist)
    del wordindexvaluelist

print(wordcount)
print(wordindex)

#keyword country search
def country_search(keyword):
    keyword=keyword.lower()
    if keyword in wordindex:
        location=wordindex[keyword]
        filename=[]
        for locationcount in range(len(location)):
            filelocation=location[locationcount]
            filelocation=(str(countries[filelocation[0]]))+".html"
            if (filename=="" or not filelocation in filename):
                filename.append(filelocation)
        return ("Your searched word was found in: "+str(filename))
    else:
        return ('Your searched word was not in the index.')

print(country_search('is'))
print(country_search('Country'))

#levenshtein distance
def editdistance(keyword):
    keyword=keyword.lower()
    listofkeys=list(wordindex.keys())
    lowestdistance=100000 
    pairedword=""
    for word in listofkeys:
        if (lev.distance(keyword,word)<lowestdistance):
            lowestdistance=lev.distance(keyword,word)
            pairedword=word
    returnvalues=[keyword, pairedword,lowestdistance]
    return returnvalues 

results=editdistance("Toronta")
print ("The closest word to the searched key:"+results[0]+" is "+results[1]+ " with an edit distance of "+str(results[2]))

#fuzzy search
def fuzzy_search(keyword):
    results=editdistance(keyword)
    location=country_search(results[1])
    return location

print(fuzzy_search('Itali'))
    
