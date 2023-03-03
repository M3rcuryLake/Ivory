import frontmatter
import markdown
import sys
import os
from datetime import datetime
from shutil import copy
import http.server
from socketserver import TCPServer
import random



if len(sys.argv) < 1 and len(sys.argv)>2:
    sys.exit('''too few arguments\n---help menu---\nTODO''')


posttemp=[]
mdtemp=[]
lr=[]
pr=[]




def Create():
    open('siteconfig.ivory', 'w').write(sys.argv[2])

def serve():
    PORT =random.randrange(1000,9999)
    DIRECTORY = "./public/"


    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=DIRECTORY, **kwargs)


    with TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        print(f"Go to http://localhost:{PORT}/ to view your server...")
        httpd.serve_forever()
        httpd.server_close()
       




def NewPage():
    f=open('./markdown/'+sys.argv[2]+'.md', 'w')
    f.write('''---\ntitle: %s\ndate: %s\nsite: %s\n---''' % (str(input('Proper Title for the Post: ')), str(datetime.now().strftime('%Y-%m-%d')), str(open('siteconfig.ivory', 'r').read())))



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
            print('copied', file_name)




    #for rebooting on build
    if os.path.exists('./public'):
        for item in mdtemp:
            if os.path.exists('./public/'+item[:-3]+'.html'):
                os.remove('./public/'+item[:-3]+'.html')
        for item in posttemp:
            if os.path.exists('./public/post/'+item[:-3]+'.html'):
                os.remove('./public/post/'+item[:-3]+'.html')



    print('PAGES: ',posttemp, mdtemp)


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
                fsx.write(frex.format(postcontent=postcontent, Title=fsr.get('title'), Site=fsr.get('site'), date=frontmatter.load('./markdown/'+item).get('date')))




    #POST PAGES
    posttemp.remove('index.md')
    for item in posttemp:
        fsr=frontmatter.load('./markdown/post/'+item)
        postcontent=markdown.markdown(fsr.content)
        with open('./public/post/'+item[:-3]+".html", 'a')  as fsx:
            frex=open('./layouts/post_single.html','r').read()
            fsx.write(frex.format(postcontent=postcontent, Title=fsr.get('title'), Site=fsr.get('site'), date=frontmatter.load('./markdown/post/'+item).get('date')))

   


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
        aer=aer+lerw.format(itemlocation=item[:-3]+'.html', item=item[:-3], date=frontmatter.load('./markdown/post/'+item).get('date'))  
    path = open('./layouts/list.html','r').read()
    text = path.replace('[loop.start]\n'+ler+'\n[loop.end]',aer)
    open('./public/post/index.html','a').write(text.format(Title=fsr.get('title'), Site=fsr.get('site')))



if (sys.argv[1] == 'serve'): serve() 
if (sys.argv[1] == 'Create'): Create()
if (sys.argv[1] == 'NewPage'): NewPage()
if (sys.argv[1] == 'Build'): Build() 
