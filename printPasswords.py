import sys
from HTMLFormHack import decryptHash, listToString

needToChangePasswordList = []

# Check if shadow file exists
try:
    shadowFile = open('/etc/shadow', 'r')
except FileNotFoundError:
    errorMessage = ("Error: Can't find/open shadow file.\n"
    "If you know /etc/shadow exists, then run this program with privileges:\n"
    "\t$ sudo python3 printPasswords.py")
    sys.exit(errorMessage)

print('User Password Security Report:')

userList, hashList = getUsersAndPasswords(shadowFile)
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

# -----------------------------------------------------------------------------
# functions
# -----------------------------------------------------------------------------

# Parse the usernames and SHA512-encrypted passwords from the shadow file
def getUsersAndPasswords (file):
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
