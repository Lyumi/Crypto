from secretsharing import PlaintextToHexSecretSharer

plaintext = []
secretlist = []


for x in range (1,6):
    lines = open('plaintext-'+str(x)+'.txt').read()
    plaintext.append(lines.splitlines()[1:])

for i in range (4):
    secretlist.append([])
    for j in range(5):
        secretlist[i].append(plaintext[j][i])
    print(PlaintextToHexSecretSharer.recover_secret(secretlist[i]))