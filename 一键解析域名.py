import os,re,requests,json,time
headers={"User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0","Referer":"https://dns.alidns.com/resolve"}
googledns="https://8.8.8.8/resolve?name="
k=os.listdir(os.getcwd())
ovpnfiles=[]
for tempfilename in k:
    (filename, extension) = os.path.splitext(tempfilename)
    if extension==".ovpn":
        ovpnfiles.append(tempfilename)
    else:
        pass
#print(ovpnfiles)
cl=[]
remote="remote .+\d{4}"
remote2="\d{1,4}.\d{1,4}.\d{1,4}.\d{1,4}"
urlport="\d+"
for  i in ovpnfiles:
    with open(i,"r")as f:
        text=f.read()
        pipei=re.search(remote,text)
        if pipei!=None:
            #print(pipei.group())
            pipei2=re.search(remote2,pipei.group())
            if pipei2!=None:
                #print(pipei2.group())
                pass
            else:
                cl.append(i)
                url=pipei.group().replace(" ","")
                url=pipei.group().replace(" ","")
                url=pipei.group().replace("remote","")
                urlport=re.search("\d{4}",url)
                if urlport!=None:
                    #print(urlport.group())
                    #url=pipei.group().replace(urlport.group(),"")
                    url=url.replace(urlport.group(),"")
                    
                    #print(url)
                    googledns="https://8.8.8.8/resolve?name="
                    dnsresolve=googledns+str(url)
                    dnsresolve=dnsresolve.replace(" ","")#去除其中的空白
                    #print(dnsresolve)
                    response=requests.get(dnsresolve,headers=headers,timeout=10)
                    response=json.loads(response.text)
                    answer=response["Answer"][0]["data"]#这是请求来的解析结果
                    #print(url,answer)
                    with open(i,"w+")as writefiles:
                        answerw="  "+answer+"  "
                        newtext=text.replace(url,answerw)
                        writefiles.write(newtext)
                    #time.sleep(0.5)
                else:
                    print("其中没有端口号???")
        else:
            pass
#print(cl)
