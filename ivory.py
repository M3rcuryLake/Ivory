import frontmatter
import markdown
import sys
import os
from timeit import timeit
import datetime
from shutil import copy
import http.server
from socketserver import TCPServer
from random import randrange
from math import ceil
import glob


posttemp, mdtemp, cdir, exclusivepages, postlist= [],[],[],[],[]
if len(sys.argv) < 1 and len(sys.argv)>2:
    sys.exit('''too few arguments\n---help menu---\nTODO''')
    
def Create():
    title=input('site name: ')
    baseURL=input("[*] Enter the BaseURL of your Site (enter your domain name or leave on '/'): ")
    author=input('[*] Authors Name: ')

    tempd=f'''---\nsite: {title}\nbaseURL: {baseURL}\ntitle: {title}\nauthor: {author}\n---'''
    open('siteconfig.ivory.md','w').write(tempd)

def Serve():
    if len(sys.argv)>3:
        if sys.argv[2]=='-p':
            if int(sys.argv[3])<1000 or int(sys.argv[3])>9999:
                exit("[!] enter a port between 1000 and 9999!....exiting")
            else:
                PORT=int(sys.argv[3])
    if len(sys.argv)<3:
        PORT =randrange(1000,9999)
        print(f'[!] No port mentioned....taking it as {PORT}')
    
    
    DIRECTORY = "./public/"
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=DIRECTORY, **kwargs)

    with TCPServer(("", PORT), Handler) as httpd:
        print("[*] serving at port", PORT)
        print(f"[*] Go to http://localhost:{PORT}/ to view your server...")
        print("[*] press Ctrl+C to exit")
        httpd.serve_forever()
       

def NewPage():
    f=open('./markdown/'+sys.argv[2]+'.md', 'w')
    f.write('''---
title: %s
date: %s
---''' % (input('Proper Title for the Post: '), datetime.now().strftime('%B %d,%Y'), frontmatter.load('siteconfig.ivory.md').get("title"), frontmatter.load('siteconfig.ivory.md').get('author')))

def Build():
    for file in os.listdir('./markdown/post'):
        if file.endswith('.md'):
            posttemp.append(file)
        else:
            continue
    for file in os.listdir('./markdown'):
        if file.endswith('.md'):
             mdtemp.append(file)
        else:
            continue
    cdir=mdtemp.copy()
    for item in posttemp:
        erfrd="post/"+item
        cdir.append(erfrd)


    baseURL=frontmatter.load('siteconfig.ivory.md').get('baseURL')
    author=frontmatter.load('siteconfig.ivory.md').get('author')
    site=frontmatter.load('siteconfig.ivory.md').get('site')
    
#--------------------------------------------------
    listPermalink=f"../post/index.html" #fix this shit
#--------------------------------------------------

    stylesPermalink=f'{baseURL}stylesheet.css'

    #COPY STATIC FILES
    for file_name in os.listdir('./static'):
        source = './static/' + file_name
        destination = './public/' + file_name 
        if os.path.isfile(source):
            copy(source, destination)
            print('copied', file_name, 'to /public/')




    #for rebooting on build
    if os.path.exists('./public'):
        for item in mdtemp:
            if os.path.exists('./public/'+item[:-3]+'.html'):
                os.remove('./public/'+item[:-3]+'.html')
        for item in posttemp:
            if os.path.exists('./public/post/'+item[:-3]+'.html'):
                os.remove('./public/post/'+item[:-3]+'.html')



    print('⭐ \nPOST DIRECTORY PAGES:',posttemp,'\n⭐ ROOT DIRECTORY PAGES:', (mdtemp),'\n')


    #BASE
    print(cdir)

    for item in cdir:
        #HEAD
        fsr=frontmatter.load('./markdown/'+item)
        with open('./public/'+item[:-3]+".html", 'w') as fsx:
            frex=open('./layouts/head.html', 'r').read()
            head=(frex.format(Title=fsr.get('title'), sitePermalink=baseURL, stylesPermalink=stylesPermalink, Site=fsr.get('site')))
        #HEADER
        fsr=frontmatter.load('./markdown/'+item)
        frex=open('./layouts/header.html','r').read()
        header=(frex.format(Title=fsr.get('title'), Site=site, date=fsr.get('date'), sitePermalink=baseURL, listPermalink=listPermalink, author=author))

        #FOOTER
        fsr=frontmatter.load('./markdown/'+item)
        with open('./public/'+item[:-3]+".html", 'a')  as fsx:
            frex=open('./layouts/footer.html','r').read()
            footer=(frex.format(Title=fsr.get('title'), Site=site, date=fsr.get('date'), sitePermalink=baseURL, listPermalink=listPermalink, author=author))
    
        #ROOT PAGE
        if item.startswith('post/')==False:
            fsr=frontmatter.load('./markdown/'+item)
            postcontent=markdown.markdown(fsr.content)
            wordcount=len(postcontent.split())
            Summary=" ".join(postcontent.split()[:70])
            readingTime=ceil((len(postcontent.split())*0.5)/60)
            frex=open('./layouts/root_single.html', 'r').read()
            rootpagearticle=(frex.format(Content=postcontent, Title=fsr.get('title'), Site=site, date=fsr.get('date'), sitePermalink=baseURL, listPermalink=listPermalink, Summary=Summary, author=author, wordCount=wordcount, readingTime=readingTime))

        #POST PAGE
        if item.startswith('post/') and item != 'post/index.md':
            fsr=frontmatter.load('./markdown/'+item)
            postcontent=markdown.markdown(fsr.content)
            wordcount=len(postcontent.split())
            Summary=" ".join(postcontent.split()[:70])
            readingTime=ceil((len(postcontent.split())*0.5)/60)
            frex=open('./layouts/post_single.html','r').read()
            postpagearticle=(frex.format(Content=postcontent, Title=fsr.get('title'), Site=site, date=fsr.get('date'), sitePermalink=baseURL , listPermalink=listPermalink, Summary=Summary, author=author, wordCount=wordcount, readingTime=readingTime))

        #LIST PAGE
        if item=='post/index.md':
            aew=open('./layouts/list.html','r').read().split('\n')
            ertemp=aew[(aew.index('{loopStart}')+1):(aew.index('{loopEnd}'))]
            lerw=("\n".join(ertemp))
            aer=''
            lq=[]
            list_of_files = glob.glob('markdown/post/*.md')
            posttemp.remove('index.md')

            for xs in posttemp:
                zx=frontmatter.load('markdown/post/'+xs)
                #zx.get('date').strftime('%d-%m-%y')
                latest_file = max(list_of_files, key=os.path.getctime)
                lq.append(latest_file)
                list_of_files.remove(latest_file)

            for ie in lq:
                print(ie)
                postlist.append(ie.lstrip("markdown/post/"))
                
            for i in postlist:
                fsr=frontmatter.load('markdown/post/index.md')
                zxc=frontmatter.load("markdown/post/"+i)
                summary=markdown.markdown(" ".join(zxc.content.split()[:70]))
                wordcount=len(zxc.content.split())
                readingTime=ceil((len(zxc.content.split())*0.5)/60)
                aer=aer+lerw.format(postLocation=i[:-3]+'.html', postTitle=zxc.get('title'), date=zxc.get('date'), Summary=summary, author=author, wordCount=wordcount, readingTime=readingTime)+'\n' 
            path = open('./layouts/list.html','r').read()
            text = path.replace('{loopStart}\n'+lerw+'\n{loopEnd}',aer)
            listpagearticle=(text.format(Content=postcontent, Title=fsr.get('title'), Site=site , date=fsr.get('date'), sitePermalink=baseURL, listPermalink=listPermalink, author=author))

    
        #WRITE
        base=open('layouts/base.html', 'r').read()
        with open('./public/'+item[:-3]+".html", 'a')  as fsx:
            if item.startswith('post/'):
                if item=='post/index.md':
                    fsx.write(base.format(head=head,header=header, article=listpagearticle, footer=footer))
                else:
                    fsx.write(base.format(head=head,header=header, article=postpagearticle, footer=footer))
                    pass
            else:
                fsx.write(base.format(head=head,header=header, article=rootpagearticle, footer=footer))


    #EXCLUSIVE PAGES '_index.html , _about.html' etc
    for item in os.listdir('layouts/'):
        if item.startswith('_'):
            copy("layouts/"+item, "./public/")
            print('copied', item, 'to /public/')
            os.rename('public/'+item, 'public/'+item.strip('_'))

    #SITEMAP
    smap='''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
      <loc>"{baseURL}"</loc>
      <lastmod>2022-07-27T02:24:08.242Z</lastmod>
      <priority>0.6</priority>
    </url>
{loopStart}
    <url>
      <loc>"{location}"</loc>
      <lastmod>"{Date}"</lastmod>
      <priority>"0.6"</priority>
    </url>
{loopEnd}
</urlset>    
'''
    aew=smap.split('\n')
    xser=aew[(aew.index('{loopStart}')+1):(aew.index('{loopEnd}'))]
    lerw=("\n".join(xser))
    aer=''
    for i in cdir[::-1]: 
        zxc=frontmatter.load('./markdown/'+i)
        aer=aer+lerw.format(location=baseURL+i[:-3]+'.html', Date=zxc.get('date'))+'\n' 
    sitemap = smap.replace('{loopStart}\n'+lerw+'\n{loopEnd}',aer)
    open('./public/sitemap.xml','w').write(sitemap)



    print('⭐ running npx tailwind css scripts to get this working....')
    os.system("npx tailwindcss -i ./src/input.css -o ./public/stylesheet.css")
     
def help():
    print(r'''
    Made By Ankit Mukherjee 🔥 (@M3rcurylake)
    _________________________________________


         _________
        / ======= \
       / __________\
      | ___________ |
      | | -       | |
      | |         | |
      | |_________| |________________________
      \= ___________/    Caffeine: 12975mg   )
      / """"""""""" \                       /
     / ::::::::::::: \                  :!-'
    (_________________)


    COMMANNDS:

    --finalise              :  build the site and serve it at once (use for preview only)
    --serve                 :  open the site to a localhost server with a random port for preview
    --serve -p 8000         :  open the site to a localhost server with given port
    --create                :  create a new project
    --newPage               :  creates a new page inside the project
    --build                 :  builds the site for static hosting services  
    --help                  :  display this prompt


    EXAMPLES:

    [*]  python3 ivory.py --finalise
    [*]  python3 ivory.py --serve  / python3 ivory.py --serve {port}
    [*]  python3 ivory.py --create
    [*]  python3 ivory.py --newPage post or python3 ivory.py post/post
    [*]  python3 ivory.py --build

    create exclusive pages (without using default themes) just by appending '_' before the filename 
    (eg: _about.html)

    Happy playing around with this tool :)
    Visit my blog 🌏 : https://m3rcurylake.pages.dev/
    
    
    ''')
if (sys.argv[1] == '--finalise'): Build();Serve()
if (sys.argv[1] == '--serve'): Serve() 
if (sys.argv[1] == '--create'): Create()
if (sys.argv[1] == '--newPage'): NewPage()
if (sys.argv[1] == '--build'): Build(); print(f'Building took {timeit()*100000}ms') 
if (sys.argv[1] == '--help'):help()
