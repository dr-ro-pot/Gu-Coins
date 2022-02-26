import praw
import json
from operator import itemgetter
from time import sleep

#load the database
f=open('last.json')
lasttran=json.load(f)  
f.close() 
f=open('balance.json')
data=json.load(f)  
f.close()  
f=open('unsub.json')
unsub=json.load(f)  
f.close()  
f=open('process.json')
pro=json.load(f)  
f.close()  


#Register a reddit API
cl='client secret'
nam='client name'
cid='client id'
reddit = praw.Reddit(user_agent="gu-coin bot (by /u/Gu-Coin)",client_id=cid, client_secret=cl,    password="password",username="uname",)


stats=reddit.submission('t0i7fl')# the post we keep editing https://www.reddit.com/user/Gu-Coin/comments/t0i7fl/statistics_regarding_gucoins/
rich='''
**Top 100 richest**\n\n
| Rank | User | Balance | Last transaction|
|--------|------------|--------|--------|
''' #this is how we start a table in reddit markdown


def checkbalance(uname): #check how much money a user has, if its the 1st time the user is being listed, give him 100 gu coins
    global data
    for i in data:
        if i[0]==uname:
            return i[1]
    data+=[[uname,100,'']] #'Name' string ie the username, balance integer, last transaction string
    f=open('balance.json','w')
    json.dump(data,f)  
    f.close()  
    return (100)

def updatebalance(giver,reciever,value, link): #updates the balance of the user giving(user name), recieving(user name), the amount and the link to the comment
    global data
    
    for i in range(len(data)):
        if data[i][0]==giver:
            data[i][1]-=value
            data[i][2]='sent ' +str(value)+'💩 to u/'+reciever+ " [Link]("+link+')'
            giverval=data[i][1]
        if data[i][0]==reciever:
            data[i][1]+=value  
            data[i][2]='recieved ' +str(value)+'💩 from u/'+giver+" [Link]("+link+')'
            recieverval=data[i][1]        
    f=open('balance.json','w')
    json.dump(data,f)  
    f.close()  
    return( giver+' Gave '+str(value)+' Gu-Coins to '+reciever)

def getvalue(strings):# function returns integer from 'give 122 gu-coins' string it will return 122 as integer, -1 if no integer was found
    start=strings.find('give ')+5 
    end=strings.find(' gu-coin')
    try:
        return (int(strings[start:end]))
    except:
        return (-1)


def updatetable(): #function updates entire table based on data
    x=''
    global data
    data=sorted(data, key=itemgetter(1),reverse=True)
    for i in range(len(data)):
        if unsub.count(data[0])<=0:
            if i>99:
                break
            x+='|'+str(i+1)+'|'+data[i][0]+'|'+str(data[i][1])+'|'+str(data[i][2])+'|\n'
    stats.edit(rich+x+"\n\n"+lasttran[0])




def get_mathiko(comment): #kaslai reply garira cha tyo manche ko redditor instance dincha yesle
    if comment.is_root:
        x=comment.submission
    else:
        x=comment.parent()
    return x

updatetable()
while True: # run function for ever
    try: #ignore exception (eg poor internet) and keep running
        for comment in reddit.subreddit("nepal").stream.comments(): #get new comments on r/nepal
            print(comment.body) 
            if comment.body.lower().count('give')>0:
                print('xxx')
                if comment.body.lower().count('gu-coin')>0:
                    print('xxx')
                    print(comment.id, pro.count(comment.id)) 
                    if pro.count(comment.id)<=0: #we havent processed this comment before
                        print('xxx-')
                        x=getvalue(comment.body.lower())
                        print('sen',x)
                        if x>0:
                            
                            giver=comment.author
                            mathi=get_mathiko(comment)
                            reciever=mathi.author
                            giverbal=checkbalance(giver.name)
                            print('bal',giverbal)
                            if unsub.count(giver.name)<=0:
                                if unsub.count(reciever.name)<=0:
                                    checkbalance(reciever.name)
                            
                                    if giverbal>=x:
                                        y=updatebalance(giver.name,reciever.name,x,mathi.permalink)   
                                        pro+=[comment.id]                    
                                        f=open('process.json','w')
                                        json.dump(pro,f)  
                                        f.close()  
                                        lasttran[0]='u/'+giver.name+' sent '+ str(x)+ ' gu-coins to '+'u/'+reciever.name +' for +[Link]('+mathi.permalink+')'
                                        f=open('last.json','w')
                                        json.dump(lasttran,f)  
                                        f.close()  
                                        updatetable()
                                        sleep(5)
            if  comment.body.count('💩')>0: #if gu emoji in post we need to see if there's numbers attached to it'
                num='1234567890'
                w=comment.body.lower()
                w=w[w.find('💩')+len('💩'):len(w)]
                no=''
                for i in w: 
                    if num.find(i)==-1:
                        break
                    else:
                        no+=i
                if no!='':
                    print(comment.id, pro.count(comment.id))
                    if pro.count(comment.id)<=0:
                        print('xxx-')
                        x=int(no)
                        print('sen',x)
                        if x>0:
                            
                            giver=comment.author
                            mathi=get_mathiko(comment)
                            reciever=mathi.author
                            giverbal=checkbalance(giver.name)
                            print('bal',giverbal)
                            if unsub.count(giver.name)<=0:
                                if unsub.count(reciever.name)<=0:
                                    checkbalance(reciever.name)
                            
                                    if giverbal>=x:
                                        y=updatebalance(giver.name,reciever.name,x,mathi.permalink)   
                                        pro+=[comment.id]                    
                                        f=open('process.json','w')
                                        json.dump(pro,f)  
                                        f.close()  
                                        lasttran[0]='u/'+giver.name+' sent '+ str(x)+ ' gu-coins to '+'u/'+reciever.name +' for +[Link]('+mathi.permalink+')'
                                        f=open('last.json','w')
                                        json.dump(lasttran,f)  
                                        f.close()  
                                        updatetable()
                                        sleep(5)
                    


    except:
        a=0 # something random




                                
        



            

