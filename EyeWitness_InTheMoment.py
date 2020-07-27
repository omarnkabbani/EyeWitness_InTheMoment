import nltk
from nltk import ngrams
import numpy as np
import re

#function to remove URLs
def remove_urls (vTEXT):
    vTEXT =re.sub(r'http\S+', '', vTEXT)
    return(vTEXT)

person=['person','rider','guy','guys','kids','dude','driver','someone','woman','lady','women','ladies','girl','girls','passenger']
location_vehicle=['platform','station','stop','stn','bus','train','ctrain'] #replace ctrain with streetcar
locationbigram=["on the","in the","m on","im on","at the","on my","on train","front of","guy on","on this","train at","the back","on bus","off at","by the","in front","the front"]
locationbigrampost=["m on","am on","im on"]
#timebigram=["now","currently"]
personal=["my train","my bus","my ctrian","i just","we just","behind me","beside me"] #replace ctrain with streetcar
issue=["there s","there is","with a","there are"]
just=["just left","just saw","just happened","just watched","just witnessed","just now","currently at","currently in","now at"]
negativepast=["last night","last week","last time","yesterday","remembered","remember","this morning","this afternoon","once","earlier","one time","when i","there was","there were","ago","when there","if there","think there","thought there","know there","imagine there","today"]
negativecontinuous=["always","constantly","everytime","every time","everyday","every day","every morning","every night","trains","buses","drivers","a bus","and now","sometimes","whenever","unless"]
negativeintention=["will","want","thought","wanted","if i","would","gonna","gon na","i should","if you","what if","so if","when will","tonight"]
negativegeneralcomplaintannouncement=["you guys","you are","you re","is no","how","rt","why is","why are","hey guys"]

file=open("Input.txt","r")
lines=file.readlines()
file.close()
corpus=[]
for line in lines:
    line=remove_urls(line) #remove URLs
    line=re.sub(r'[^\w]', ' ', line) #remove symbols
    line=line.lower()

    corpus.append(line) #put the processed tweets in corpus 

tok_corp=[nltk.word_tokenize(sent) for sent in corpus]

bigrams=[]
tempbigrams=[]
for tweet in corpus:
    _bigrams=ngrams(tweet.split(),2)
    __bigrams=list(_bigrams)
    for bigram in __bigrams:
        bigram_=bigram[0]+" "+bigram[1]
        tempbigrams.append(bigram_)
    bigrams.append(tempbigrams)
    tempbigrams=[]
loading=0
vector=[]
f=open("Output.txt","w")
for i in np.arange(len(tok_corp)):
    print("Processing:",loading)
    loading=loading+1
    justposition=0
    counterperson=0
    counterlocation_vehicle=0
    counterlocationbigrampost=0
    counterlocation_vehicleissue=0
    counterpersonal=0
    counterissue=0
    counterjust=0
    counterjustpast=0
    counternegativepersonalpast=0
    counternegativepast=0
    counternegativecontinuous=0
    counternegativeintention=0
    counternegativegeneralcomplaintannouncement=0
    POS=nltk.pos_tag(tok_corp[i])
    for keyword in location_vehicle:
        if (keyword in tok_corp[i]):
            location_vehicleposition=tok_corp[i].index(keyword)
            for keyword_ in locationbigram:
                if (keyword_ in bigrams[i]):
                    locationbigramposition=tok_corp[i].index(keyword_.split(" ")[0])
                    if (location_vehicleposition-locationbigramposition<=3) and (location_vehicleposition-locationbigramposition>0):
                        counterlocation_vehicle=1
            for keyword__ in locationbigrampost:
                if (keyword__ in bigrams[i]):
                    location_vehicleposition=tok_corp[i].index(keyword)
                    locationbigrampostposition=tok_corp[i].index(keyword__.split(" ")[0])
                    if (locationbigrampostposition-location_vehicleposition<3) and (locationbigrampostposition-location_vehicleposition>0):
                        counterlocationbigrampost=counterlocationbigrampost+1
            try:
                if "VBZ" in nltk.pos_tag(tok_corp[i])[location_vehicleposition+1]:
                    counterlocation_vehicleissue=counterlocation_vehicleissue+1
            except:
                pass
    for keyword in personal:
        if (keyword in bigrams[i]):
            counterpersonal=counterpersonal+1
    for keyword in issue:
        if (keyword in bigrams[i]):
            counterissue=1      
    for keyword in just:
        if (keyword in bigrams[i]):
            counterjust=counterjust+1
    if [j for j, x in enumerate(tok_corp[i]) if (x == "just")]!=[]:
        templist=[j for j, x in enumerate(tok_corp[i]) if (x == "just")]
        for justposition in templist:
            try:
                if ("VBD" in nltk.pos_tag(tok_corp[i])[justposition+1]) or ("VBN" in nltk.pos_tag(tok_corp[i])[justposition+1]):
                    counterjustpast=1
            except:
                pass
    for keyword in person:
        if (keyword in tok_corp[i]):
            counterperson=1
    if [j for j, x in enumerate(tok_corp[i]) if (x == "i" or x=="we")]!=[]:
        templist=[j for j, x in enumerate(tok_corp[i]) if (x == "i" or x=="we")]
        for personalposition in templist:
            try:
                if ("VBD" in nltk.pos_tag(tok_corp[i])[personalposition+1]):
                    counternegativepersonalpast=counternegativepersonalpast+1
            except:
                pass
    for keyword in negativepast:
        if (keyword in tok_corp[i]) or (keyword in bigrams[i]):
            counternegativepast=counternegativepast+1
    for keyword in negativecontinuous:
        if (keyword in tok_corp[i]) or (keyword in bigrams[i]):
            counternegativecontinuous=counternegativecontinuous+1
    for keyword in negativeintention:
        if (keyword in tok_corp[i]) or (keyword in bigrams[i]):
            counternegativeintention=counternegativeintention+1
    for keyword in negativegeneralcomplaintannouncement:
        if (keyword in tok_corp[i]) or (keyword in bigrams[i]):
            counternegativegeneralcomplaintannouncement=counternegativegeneralcomplaintannouncement+1
    tempvector=[counterperson,counterlocation_vehicle,counterlocationbigrampost,counterlocation_vehicleissue,counterpersonal,counterissue,counterjust,counterjustpast,counternegativepersonalpast,counternegativepast,counternegativecontinuous,counternegativeintention,counternegativegeneralcomplaintannouncement]
    out= ", ".join(map(str, tempvector))
    f.write(out+"\n")

f.close()
'''
    if [j for j in person if j in tok_corp[i]]!=[]:
        tempdistance1=tempdistance2=tempdistance3=tempdistance4=np.nan
        personlocation=tok_corp[i].index([j for j in person if j in tok_corp[i]][0])
        if counterlocation_vehicle>0 or counterlocationbigrampost>0 or counterlocation_vehicleissue>0:
            tempdistance1=abs(location_vehicleposition-personlocation)
        if counterpersonal>0:
            tempdistance2=abs(personalposition-personlocation)
        if counterissue>0:
            tempdistance3=abs(issueposition-personlocation)
        if counterjust>0 or counterjustpast>0:
            tempdistance4=abs(justposition-personlocation)
        meanlist=np.array([tempdistance1,tempdistance2,tempdistance3,tempdistance4])
        if np.isnan(tempdistance1)==True and np.isnan(tempdistance2)==True and np.isnan(tempdistance3)==True and np.isnan(tempdistance4)==True:
            counterperson=40
        else:
            counterperson=np.nanmean(meanlist)
'''