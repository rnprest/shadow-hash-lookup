import sys
from HTMLFormHack import decryptHash, listToString

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

# Parse the usernames and SHA512-encrypted passwords from the shadow file
def getUsersAndPasswords(file):
    users = [] # Contains all users from the shadow file
    hashes = [] # Limit uses of decryptHash function call by combining all hashes
    for line in file:
        if '$6$' in line:
            beforeHashIndex = line.find(':')
            afterHashIndex = line.find(':', beforeHashIndex+1)
            username = line[:beforeHashIndex]
            passwordHash = line[beforeHashIndex+4:afterHashIndex]
            users.append(username)
            hashes.append(passwordHash)
    return users, hashes

# -----------------------------------------------------------------------------
# Code
# -----------------------------------------------------------------------------

needToChangePasswordList = []

# Check if shadow file exists
try:
    shadowFile = open('/etc/shadow', 'r')
except FileNotFoundError:
    errorMessage = "Error: Can't find shadow file"
    sys.exit(errorMessage)

print('User Password Security Report:')

userList, hashList = getUsersAndPasswords(shadowFile)
print(f'userList = {userList}')
print(f'hashList = {hashList}')

hashes = listToString(hashList)
print(f'\nthe hashes string = {hashes}')

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
