import requests
import time

## This function will emulate a web broswer to sumbit the MD5Decrypt form and gather a response
## This approach avoids using API keys (because we were unsuccessful in obtaining them)
## Please limit use of this function because the website restricts the number of calls user per hour

## Updated: Now allows for multiple hashes
## @Pre: String: Hash/Hashes separated by a newline

def decryptHash( hash_value ):
    data = {
        "hash": hash_value,
        # "captcha####":"", This will be added dynamically based
        # "ahah####":"", This will be added dynamically based
        "decrypt":" Decrypter"
       }

    r = requests.get("https://md5decrypt.net/Sha512/")
    response = r.text

    time.sleep(2) # Waits for server to validate keys and prevent DDos

    ## Parses Get HTML response the ahah key
    localkey =  response[response.find("ahah"):response.find("/>",response.find("ahah") )].split("\" value=\"")
    localkey[1] = localkey[1].strip("\"")
    data[localkey[0]] = localkey[1]

    ## Parses Get HTML response the Captcha number
    localkey = response[response.find("name=\"captcha"):response.find("\" place",response.find("name=\"captcha") )].split("\" value=\"")
    localkey[0] = localkey[0].strip("name=\"")
    data[localkey[0]] =""

    ## Sends a request with hash and key
    r = requests.post("https://md5decrypt.net/en/Sha512/#answer", data=data)
    response = r.text

    hash = data["hash"]
    hashes = hash.split()

    decryptedHashes = []

    ## Parses Post HTML response to from the answer
    for x in range(0, len(hashes)):
        decrypted = response[response.find(hashes[x]): response.find("</b>", response.find(hashes[x]))]
        if decrypted.find("[ Unfound ]" ) != -1:
            decryptedHashes.append("Unfound")
        else:
            decrypted = decrypted.split("<b>")
            decryptedHashes.append(decrypted[1])

    # print(decryptedHashes)
    return decryptedHashes


def listToString (list):
    separator = "\n"
    return separator.join(list)

if __name__ == '__main__':

    hashlist = []
    hashlist.append("9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043")
    hashlist.append("3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1eb8b85103e3be7ba613b31bb5c9c36214dc9f14a42fd7a2fdb84856bca5c44c2")
    hashlist.append("40b3cfbc401ac193651eba2cecf6b8a62c967bdd9450834b5aa1f71de09c33e5bcfeba7bff222835bf67b2118a25d7b17b530c74b805467251746c5e03528d8b")
    hashes = listToString(hashlist)
    decryptHash(hashes)

