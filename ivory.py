import frontmatter
import markdown
import sys
import os
from timeit import timeit
from datetime import datetime
from shutil import copy
import http.server
from socketserver import TCPServer
from random import randrange



if len(sys.argv) < 1 and len(sys.argv)>2:
    sys.exit('''too few arguments\n---help menu---\nTODO''')


posttemp=[]
mdtemp=[]
lr=[]
pr=[]




def Create():
    open('siteconfig.ivory', 'w').write(sys.argv[2])

def Serve():

    if len(sys.argv)<3:
        PORT =randrange(1000,9999)
        print(f'no port mentioned....taking it as {PORT}')
        DIRECTORY = "./public/"


        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=DIRECTORY, **kwargs)


        with TCPServer(("", PORT), Handler) as httpd:
            print("serving at port", PORT)
            print(f"Go to http://localhost:{PORT}/ to view your server...")
            print("press Ctrl+C to exit")
            httpd.serve_forever()

    if sys.argv[2]=='-p':
        if int(sys.argv[3])<1000 or int(sys.argv[3])>9999:
            exit("enter a port between 1000 and 9999!....exiting")
        else:
            PORT=int(sys.argv[3])


    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=DIRECTORY, **kwargs)


    with TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        print(f"Go to http://localhost:{PORT}/ to view your server...")
        print("press Ctrl+C to exit")
        httpd.serve_forever()
       




def NewPage():
    f=open('./markdown/'+sys.argv[2]+'.md', 'w')
    f.write('''---\ntitle: %s\ndate: %s\nsite: %s\n---''' % str(input('Proper Title for the Post: '), str(datetime.now().strftime('%d-%m-%Y')), str(open('siteconfig.ivory', 'r').read())))



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



    print('POST DIRECTORY PAGES:',posttemp,' ROOT DIRECTORY PAGES:', mdtemp)


    #HEAD ONLY
    for item in mdtemp:
        fsr=frontmatter.load('./markdown/'+item)
        with open('./public/'+item[:-3]+".html", 'w') as fsx:
            frex=open('./layouts/head.html', 'r').read()
            fsx.write(frex.format(Title=fsr.get('title'), Site=fsr.get('site') ))
    for item in posttemp:
        fsr=frontmatter.load('./markdown/post/'+item)
        with open('./public/post/'+item[:-3]+".html", 'w') as fsx:
            frex=open('./layouts/posthead.html', 'r').read()
            fsx.write(frex.format(Title=fsr.get('title'), Site=fsr.get('site') ))



    #ROOT PAGES
    for item in mdtemp:
        if item == 'list.md':
            continue
        else:
            fsr=frontmatter.load('./markdown/'+item)
            postcontent=markdown.markdown(fsr.content)
            with open('./public/'+item[:-3]+".html", 'a')  as fsx:
                frex=open('./layouts/index_single.html', 'r').read()
                fsx.write(frex.format(postcontent=postcontent, Title=fsr.get('title'), Site=fsr.get('site'), date=fsr.get('date')))




    #POST PAGES
    posttemp.remove('index.md')
    for item in posttemp:
        fsr=frontmatter.load('./markdown/post/'+item)
        postcontent=markdown.markdown(fsr.content)
        with open('./public/post/'+item[:-3]+".html", 'a')  as fsx:
            frex=open('./layouts/post_single.html','r').read()
            fsx.write(frex.format(postcontent=postcontent, Title=fsr.get('title'), Site=fsr.get('site'), date=fsr.get('date')))

   


    #LIST PAGE
    with open('./layouts/list.html','r') as input_data:
        for line in input_data:
            if line.startswith('[loop.start]'):
                break
        for line in input_data:
            if line.startswith('[loop.end]'):
                break
            ler=line.strip()

            


    aer=''
    lerw=ler+'\n'
    for item in posttemp[::-1]: 
        zxc=frontmatter.load('./markdown/post/'+item)
        summary=" ".join(zxc.content.split()[:70])
        aer=aer+lerw.format(itemLocation=item[:-3]+'.html', itemTitle=zxc.get('title'), date=zxc.get('date'), Summary=summary)  
    path = open('./layouts/list.html','r').read()
    text = path.replace('[loop.start]\n'+ler+'\n[loop.end]',aer)
    open('./public/post/index.html','a').write(text.format(Title=fsr.get('title'), Site=fsr.get('site')))
    
    if (sys.argv[1]!='--finalise'):
        print('running npx tailwind css scripts to get this working....')
        os.system("cd public && npx tailwindcss -i ./src/input.css -o stylesheet.css")
    else:
        pass

def help():
    print(r'''
    Made By Ankit Mukherjee (@M3rcurylake)
    ______________________________________


         _________
        / ======= \
       / __________\
      | ___________ |
      | | -       | |
      | |         | |
      | |_________| |________________________
      \= ___________/    Caffeine: 12975mg   )
      / """"""""""" \                       /
     / ::::::::::::: \                  =D-'
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

    Happy playing around with this tool :)
    Visit my blog : https://m3rcurylake.pages.dev/


    ''')


if (sys.argv[1] == '--finalise'): Build();Serve()
if (sys.argv[1] == '--serve'): Serve() 
if (sys.argv[1] == '--create'): Create()
if (sys.argv[1] == '--newPage'): NewPage()
if (sys.argv[1] == '--build'): Build(); print(f'Building took {timeit()*100000}ms') 
if (sys.argv[1] == '--help'):help()
