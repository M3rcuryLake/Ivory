import frontmatter
import markdown
import sys
import os
from timeit import timeit
import datetime
from shutil import copy
from random import randrange
from math import ceil
import glob


posttemp, mdtemp, tree_files, exclusivepages, postlist= [],[],[],[],[]
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
    print("[*] serving at port", PORT)
    print(f"[*] Go to http://localhost:{PORT}/ to view your server...")
    print("[*] press Ctrl+C to exit")
    os.system(f"cd {DIRECTORY} && python3 -m http.server {PORT}")

def NewPage():
    f=open('./markdown/'+sys.argv[2]+'.md', 'w')
    f.write('''---
title: %s
date: %s
---''' % (input('Proper Title for the Post: '),
 datetime.now().strftime('%B %d,%Y'),
 frontmatter.load('siteconfig.ivory.md').get("title"),
 frontmatter.load('siteconfig.ivory.md').get('author')))




def Build():
    #INITIALISATION
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
    tree_files=mdtemp.copy()
    for item in posttemp:
        erfrd="post/"+item
        tree_files.append(erfrd)
        
     #EXCLUSIVE PAGES '_index.html , _about.html' etc
    for item in os.listdir('layouts/'):
        if item.startswith('_'):
            copy("layouts/"+item, "./public/")
            print('copied', item, 'to /public/')
            os.rename('public/'+item, 'public/'+item.strip('_'))



    #VARIABLES
    baseURL=frontmatter.load('siteconfig.ivory.md').get('baseURL')
    stylesPermalink=f'{baseURL}stylesheet.css'    
    author=frontmatter.load('siteconfig.ivory.md').get('author')
    site=frontmatter.load('siteconfig.ivory.md').get('site')
#--------------------------------------------------
    listPermalink=f"../post/index.html" #fix this shit
#--------------------------------------------------



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
    if os.path.exists("./public/post/")==False:
    	os.mkdir("./public/post/")
    #CHECKPOINT
    print('\nPOST DIRECTORY PAGES:',posttemp,'\nROOT DIRECTORY PAGES:', (mdtemp),'\n')
 
 
    #BASE
    for item in tree_files:
    	#DEC VARS
        file_matter=frontmatter.load('./markdown/'+item)
        postcontent=markdown.markdown(file_matter.content)
        wordcount=len(postcontent.split())
        Summary=" ".join(postcontent.split()[:70])
        readingTime=ceil((len(postcontent.split())*0.5)/60)
        Title=file_matter.get('title')
        date=file_matter.get('date')
        index=list()
        q=0
        
    
        #HEAD,HEADER,FOOTER,ROOT PAGE & POST PAGE        
        for list_ord in ["head","header","footer"]:
        	plate_file=open(f'./layouts/{list_ord}.html', 'r')
        	index.append(plate_file.read().format(Content=postcontent, Title=Title, Site=site, date=date, sitePermalink=baseURL, listPermalink=listPermalink, Summary=Summary, author=author, stylesPermalink=stylesPermalink, wordCount=wordcount, readingTime=readingTime))	
        head,header,footer=index[0],index[1],index[2]
        
        if item.startswith('post/')==False:
        	artc_file=open('./layouts/root_single.html', 'r')
        	rootpagearticle=artc_file.read().format(Content=postcontent, Title=Title, Site=site, date=date, sitePermalink=baseURL, listPermalink=listPermalink, Summary=Summary, author=author, stylesPermalink=stylesPermalink, wordCount=wordcount, readingTime=readingTime)
                        
        if item.startswith('post/') and item != 'post/index.md':
         	artc_file=open('./layouts/post_single.html','r')
         	postpagearticle=artc_file.read().format(Content=postcontent, Title=Title, Site=site, date=date, sitePermalink=baseURL, listPermalink=listPermalink, Summary=Summary, author=author, stylesPermalink=stylesPermalink, wordCount=wordcount, readingTime=readingTime)
            
            
         
        #LIST PAGE
        if item=='post/index.md':
            l_page_i=open('./layouts/list.html','r').read().split('\n')
            l_page_j=l_page_i[(l_page_i.index('{loopStart}')+1):(l_page_i.index('{loopEnd}'))]
            list_page_temp=("\n".join(l_page_j))
            space=''

            #GETTING THE NEWEST FILE...(use manual frontmatter checking)	
            latestfile=[]
            list_of_files = glob.glob('markdown/post/*.md')
            for xs in posttemp:
                latest_file = max(list_of_files, key=os.path.getctime)
                latestfile.append(latest_file)
                list_of_files.remove(latest_file)      
            for ie in latestfile:
                postlist.append(ie.lstrip("markdown/post"))    
            postlist.pop(postlist.index("index.md"))
            
            for i in postlist:
                post_page=frontmatter.load("markdown/post/"+i)
                Summary=markdown.markdown(" ".join(post_page.content.split()[:70]))
                wordcount=len(post_page.content.split())
                readingTime=ceil((len(post_page.content.split())*0.5)/60)
                postTitle=post_page.get('title')
                date=post_page.get('date')
                space=space+list_page_temp.format(postLocation=i[:-3]+'.html', postTitle=postTitle, Title=Title, date=date, Summary=Summary, author=author, wordCount=wordcount, readingTime=readingTime)+'\n' 
            path = open('./layouts/list.html','r').read()
            text = path.replace('{loopStart}\n'+list_page_temp+'\n{loopEnd}',space)
            listpagearticle=(text.format(Content=postcontent, Title=Title, Site=site , date=date, sitePermalink=baseURL, listPermalink=listPermalink, author=author))

    
        #WRITE
        base=open('layouts/base.html', 'r').read()
        base_body=open('./public/'+item[:-3]+".html",'w')
        if item.startswith('post/'):
            if item=='post/index.md':
                base_body.write(base.format(head=head,header=header, article=listpagearticle, footer=footer))
            else:
                base_body.write(base.format(head=head,header=header, article=postpagearticle, footer=footer))
        else: 
            base_body.write(base.format(head=head,header=header, article=rootpagearticle, footer=footer))

    #SITEMAP
    smap=open("./sitemap_template","r").read()
    smap_list=smap.split('\n')
    smap_crop=smap_list[(smap_list.index('{loopStart}')+1):(smap_list.index('{loopEnd}'))]
    smap_croptext=("\n".join(smap_crop))
    space=''
    for i in tree_files[::-1]: 
        zxc=frontmatter.load('./markdown/'+i)
        space=space+smap_croptext.format(location=baseURL+i[:-3]+'.html', Date=zxc.get('date'))+'\n' 
    sitemap = smap.replace('{loopStart}\n'+smap_croptext+'\n{loopEnd}',space)
    open('./public/sitemap.xml','w').write(sitemap)


    #MAKING TWCSS WORK
    print('running npx tailwind css scripts to get this working....')
    os.system("npx tailwindcss -i ./src/input.css -o ./public/stylesheet.css")
     
def help():
    print(r'''
    Made By Ankit Mukherjee (@M3rcurylake)
    _________________________________________

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
    Visit my blog : https://m3rcurylake.pages.dev/
    
    
    ''')
if (sys.argv[1] == '--finalise'): Build();Serve()
if (sys.argv[1] == '--serve'): Serve() 
if (sys.argv[1] == '--create'): Create()
if (sys.argv[1] == '--newPage'): NewPage()
if (sys.argv[1] == '--build'): Build(); print(f'Building took {timeit()*100000}ms') 
if (sys.argv[1] == '--help'):help()
