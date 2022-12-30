import requests
import urllib.request

# title headers for UI
youtwobeArt="""
                   _                 _
                  | |               | |
 _   _  ___  _   _| |___      _____ | |__   ___
| | | |/ _ \| | | | __\ \ /\ / / _ \| '_ \ / _ \\
| |_| | (_) | |_| | |_ \ V  V / (_) | |_) |  __/
 \__, |\___/ \__,_|\__| \_/\_/ \___/|_.__/ \___|
  __/ |
 |___/
\n"""
goodbyeArt="""
 _
| |
| |__  _   _  ___
| '_ \| | | |/ _ \\
| |_) | |_| |  __/
|_.__/ \__, |\___|
        __/ |
       |___/
\n"""

# user interaction handler
class UI:
    def __init__(self):
        self.inn=""
        self.query=""
        self.state=0
        self.vids=[]
        self.body="1) search for a vid\n"
        self.body+="2) enter vid id\n"
        self.body+="\nyour choice: "
        self.header=youtwobeArt

    def run(self):
        clearConsole()
        print(self.header)
        self.inn=input(self.body)
        self.update()

    def update(self):
        if (self.state==0):
            if (self.inn=="1"):
                self.body="pop a title in here: "
                self.state=1
            elif (self.inn=="2"):
                self.body="pop an id in here: "
                self.state=4
        elif (self.state==1):
            self.body="results for: "+self.inn+"\n\n"
            # shenanigans with for loops and query stuff
            self.vids=getVids(self.inn)
            for i in range(0,len(self.vids)):
                self.body+=str(i)+". "+str(self.vids[i])+"\n"
            self.body+="\n"
            self.body+="1) watch one of them\n"
            self.body+="2) start over\n"
            self.body+="\nyour choice: "
            self.state=2
        elif (self.state==2):
            if (self.inn=="1"):
                self.body="which to watch?\n\n"
                # add options
                for i in range(0,len(self.vids)):
                   self.body+=str(i)+". "+repr(self.vids[i])+"\n"
                self.body+="\n"
                self.body+="\nyour choice: "
                self.state=3
            elif (self.inn=="2"):
                self.body="1) search for a vid\n"
                self.body+="2) enter vid id\n"
                self.body+="\nyour choice: "
                self.state=0
        elif (self.state==3):
            if (self.inn.isdigit() and int(self.inn)>=0 and int(self.inn)<len(self.vids)-1):
                #urllib.request.urlretrieve(self.vids[int(self.inn)].vidUrl, self.vids[int(self.inn)].title+".mp4")
                self.body="downloading "+self.vids[int(self.inn)].title+" for your viewing pleasure\n\n"
                self.body+=self.vids[int(self.inn)].vidUrl+"\n\n"
                self.body+="1) start over\n"
                self.body+="2) quit\n"
                self.body+="\nyour choice: "
                self.state=5
        elif (self.state==4):
            #urllib.request.urlretrieve(getVidUrl(self.inn), self.inn+".mp4")
            self.body="here it is:\n\n"
            self.body+=getVidUrl(self.inn)+"\n\n"
            self.body+="1) start over\n"
            self.body+="2) quit\n"
            self.body+="\nyour choice: "
            self.state=5
        elif (self.state==5):
            if (self.inn=="1"):
                self.body="1) search for a vid\n"
                self.body+="2) enter vid id\n"
                self.body+="\nyour choice: "
                self.state=0
            elif (self.inn=="2"):
                self.body="come back soon!"
                self.header=goodbyeArt
        else:
            self.exit()
        self.run()


# kinda self explanatory
class Video:
    def __init__(self, title, author, ID):
        self.title=title
        self.author=author
        self.ID=ID
        self.vidUrl=getVidUrl(ID)

    def __repr__(self):
        if (self.author!=""):
            return self.title+" ("+self.ID+") by: "+self.author
        else:
            return self.title+" ("+self.ID+")"


# methods that are just generally useful
# makes url usable bc youtube is wonk
def decodeUrl(inn):
    encodeds=["%3A","%2F","%3F","%3D","%26","%25","%2C"]
    decodeds=[":","/","?","=","&","%",","]
    r,i=0,0
    for r in range(0,2):
        for i in range(0,len(encodeds)):
            while inn.find(encodeds[i])>0:
                inn=inn[0:inn.find(encodeds[i])]+decodeds[i]+inn[inn.find(encodeds[i])+3:len(inn)]
    return inn

# prints 50 lines
def clearConsole():
    for i in range(0,50):
        print()

# gets options from query source code
def getVids(query):
    ret=[]
    page=requests.get("https://www.youtube.com/results?search_query="+query)
    source=str(page.content)
    while (source.find("a href=\"/watch?v")!=-1):
        vidSlice=source[source.find("a href=\"/watch?v"):source.find("a href=\"/watch?v")+500]
        IDSlice=vidSlice[17:28]
        titleSliceish=vidSlice[vidSlice.find("title")+7:len(vidSlice)]
        titleSlice=titleSliceish[0:titleSliceish.find("\"")]
        if (vidSlice.find("a href=\"/user/")!=-1):
            authorSliceish=vidSlice[vidSlice.find("a href=\"/user/")+14:len(vidSlice)]
            authorSlice=authorSliceish[0:authorSliceish.find("class")-2]
        else:
            authorSlice=""
        ret.append(Video(simplifyTitle(titleSlice), authorSlice, IDSlice))
        source=source[source.find(vidSlice)+500:len(source)]
    return ret

# take html code for ascii out of title
def simplifyTitle(titleSlice):
    while (titleSlice.find("&")!=-1):
        firstHalf=titleSlice[0:titleSlice.find("&")]
        secondHalfish=titleSlice[titleSlice.find("&"):len(titleSlice)]
        titleSlice=firstHalf+secondHalfish[secondHalfish.find(";")+1:len(secondHalfish)]
    while (titleSlice.find("\\x")!=-1):
        titleSlice=titleSlice[0:titleSlice.find("\\x")]+titleSlice[titleSlice.find("\\x")+4:len(titleSlice)]
    return titleSlice

# returns hosted link of video
def getVidUrl(ID):
    page=requests.get("https://www.youtube.com/watch?v="+ID)
    source=str(page.content)
    fmtSlice=source[source.find("url_encoded_fmt_stream_map"):len(source)]
    urlOnwardSlice=fmtSlice[fmtSlice.find("https"):len(fmtSlice)]
    encodedUrl=urlOnwardSlice[0:urlOnwardSlice.find("u0026")-2]
    # check for that wonky other kind of url
    if encodedUrl.count(",")>0:
        encodedUrl=encodedUrl[0:encodedUrl.find(",")]
    return decodeUrl(encodedUrl)

# this is it
uiy=UI()
uiy.run()
