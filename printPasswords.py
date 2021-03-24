import sys
from HTMLFormHack import *

# Error handling
if len(sys.argv) != 2:
    errorMessage = """Error: Please see correct syntax below
    \t$ python3 printPasswords.py shadowCopy"""
    sys.exit(errorMessage)

userList = [] # Contains all users from the shadow file
hashList = [] # Limit uses of decryptHash function call by combining all hashes
needToChangePasswordList = []
shadowFile = open(sys.argv[1], 'r')

print('User Password Security Report:')
for line in shadowFile:
    if '$6$' in line:
        beforeHashIndex = line.find(':')
        afterHashIndex = line.find(':', beforeHashIndex+1)
        username = line[:beforeHashIndex]
        passwordHash = line[beforeHashIndex+4:afterHashIndex]
        userList.append(username)
        hashList.append(passwordHash)

hashes = listToString(hashList)
decryptedHashes = decryptHash(hashes)

# Print whether each user's password hash was found
for (user, decrypted) in zip(userList, decryptedHashes):
    result = ''
    greenCheck = '✅ '
    redX = '❌ '
    if (decrypted == "Unfound"):
        result = greenCheck + 'Unfound Hash'
    else:
        result = redX + decrypted
        needToChangePasswordList.append(user)
    print(f'{user}: {result}')

# Print the users that need to change their passwords
print('\nThe following users need to change their passwords:')
for user in needToChangePasswordList:
    print(user)


