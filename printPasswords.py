import sys

# Error handling
if len(sys.argv) != 2:
    errorMessage = """Error: Please see correct syntax below
    \t$ python3 printPasswords.py shadowCopy"""
    sys.exit(errorMessage)

shadowFile = open(sys.argv[1], 'r')

for line in shadowFile:
    if '$6$' in line:
        print(line)
        beforeHashIndex = line.find(':')
        afterHashIndex = line.find(':', beforeHashIndex+1)
        username = line[:beforeHashIndex]
        passwordHash = line[beforeHashIndex+4:afterHashIndex]

        print(f'The username is {username}')
        print(f'The password hash is {passwordHash}')
