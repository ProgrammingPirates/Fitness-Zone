from twilio.rest import Client
import os

thefile = open('user.txt','r')
a=thefile.readline()+thefile.readline()+thefile.readline()+thefile.readline()
b=thefile.readline()
c=0
d=0
e=0
num=""
for i in b:
   if(i==':'):
       c+=2
       break
   else:
       c+=1
for i in b:
    if(d==c or e==1):
        e=1
        num+=i
    else:
        d+=1
#a->body,num->number     
ACCOUNT_SID = "#" 
AUTH_TOKEN = "#" 
client = Client(ACCOUNT_SID, AUTH_TOKEN) 

message = client.messages.create(
         to=num,
         body=a,
         from_='#'
     )
print(message.sid)
