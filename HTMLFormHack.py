import requests
import time

## This function will emulate a web broswer to sumbit the MD5Decrypt form and gather a response 
## This approach avoids using API keys (because we were unsuccessful in obtaining them)
## Please limit use of this function because the website restricts the number of calls user per hour 

def decryptHash( hash_value ):
    data = {
        "hash": hash_value,
        # "captcha####":"", This will be added dynamically based 
        # "ahah####":"", This will be added dynamically based
        "decrypt":" Décrypter"
       }
    
    r = requests.get("https://md5decrypt.net/Sha512/")
    response = r.text

    time.sleep(2) #Waits for server to validate keys and prevent DDos 

    ## Parses Get HTML response the ahah key 
    localkey =  response[response.find("ahah"):response.find("/>",response.find("ahah") )].split("\" value=\"")
    localkey[1] = localkey[1].strip("\"")
    data[localkey[0]] = localkey[1]

    ## Parses Get HTML response the Captcha number
    localkey = response[response.find("name=\"captcha"):response.find("\" place",response.find("name=\"captcha") )].split("\" value=\"")
    localkey[0] = localkey[0].strip("name=\"")
    data[localkey[0]] =""

    ## Sends a requested with hash and key 
    r = requests.post("https://md5decrypt.net/en/Sha512/#answer", data=data)
    response = r.text
   
    ## Parses Post HTML response to from the answer 
    decrypted = response[response.find(data["hash"]): response.find("</b>", response.find(data["hash"]))]
    hash = data["hash"]
    decrypted = decrypted.split("<b>")
    
    print(decrypted[1])
    return decrypted[1]

#TODO Write a function to accept a string of hashes and then parse the response this will help prevent calling the url frequently 


if __name__ == '__main__':

    decryptHash("3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1eb8b85103e3be7ba613b31bb5c9c36214dc9f14a42fd7a2fdb84856bca5c44c2" )
   