#-*- coding: utf-8 -*-
import urllib2
import os
import time
from bs4 import BeautifulSoup

curpath = './'
dropspath = 'drops/'
resspath = 'resources/'
errorlog = 'err.log'

def catfile(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
    headers = {'User-Agent':user_agent}
    request = urllib2.Request(url,None,headers)
    response = urllib2.urlopen(request)
    return response.read()

def getimg(url,path):
    try:
        #urllib.urlretrieve(url,path)
        response = urllib2.urlopen(url,timeout = 5)
        imagefile = open(path,'wb')
        content = response.read()
        imagefile.write(content)
        imagefile.close()
    except:
        logfile = open(curpath+errorlog,'a')
        curtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        error = 'Download ' + url + ' failed !' + '\r\n'
        logfile.write(curtime + ' : ' + error)
        logfile.close()

def savefile(filepath,filename,content):
    try:
        f = file(filepath + filename,'wb')
        f.write(content)
        f.close()
    except:
        pass

def parsepaper(url):
    while url != None:
        content = catfile(url)
        soup = BeautifulSoup(content,'html.parser')
        divs = soup.find_all('div',class_='post')
        nextp = soup.find('a',class_='nextpostslink')
        try:
            url = nextp.get('href')
        except:
            url = None
        for div in divs:
            title = div.h2.a.get('title').replace('Permanent Link to ','')
            print title
            href = div.h2.a.get('href')
            paper = catfile(href)
            parseres(paper,title)

def script_has_src(tag):
    return tag.name == 'script' and tag.has_attr('src')

def link_has_href(tag):
    return tag.name == 'link' and tag.has_attr('href')

def image_has_src(tag):
    if tag.has_attr('id'):
        if tag['id'] == 'captcha_img':
            return False
    return tag.name == 'img' and tag.has_attr('src')

#保存资源文件 包括外部css js image
def parseres(content,title):
    soup = BeautifulSoup(content,'html.parser')
    respath = resspath + title.replace(':','_')
    if os.path.exists(curpath + dropspath + respath):
        print 'All complete !'
        exit()
    os.makedirs(curpath + dropspath + respath)
    base = soup.base
    base['href'] = '.'
    jss = soup.find_all(script_has_src)
    for js in jss:
       jsurl = js.get('src')
       jsname = jsurl.split('/')[-1].split('?')[0]
       js['src'] = curpath + respath + '/' + jsname
       #print jsname
       jsfile = catfile(jsurl)
       savefile(curpath + dropspath + respath+'/',jsname,jsfile)
    links = soup.find_all(link_has_href)
    for link in links:
        linkurl = link.get('href')
        linkname = linkurl.split('/')[-1].split('?')[0]
        link['href'] = curpath + respath + '/' + linkname
        #print linkname
        linkfile = catfile(linkurl)
        savefile(curpath + dropspath + respath + '/',linkname,linkfile)
    images = soup.find_all(image_has_src)
    for image in images:
        imageurl = image.get('src')
        imagename = imageurl.split('/')[-1].split('?')[0]
        image['src'] = curpath + respath + '/' + imagename
        #print imagename
        getimg(imageurl,curpath + dropspath + respath + '/' + imagename)
    savefile(curpath + dropspath,title.replace(':','_')+'.html',str(soup))
 
if __name__=='__main__':
    parsepaper('http://drops.wooyun.org/')
    print 'complete !' 
