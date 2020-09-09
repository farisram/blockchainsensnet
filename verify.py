import json

def verifyblock(): #fungsi verifikasi hashcode
    with open('database.txt', 'r') as f:
        a = json.loads(f.read())
        for n in range(len(a)):
            # print(a[n][2])
            # print(a[n-1][3])
            if (a[n][0]) == 1:
                print("First block...")
            elif (a[n][2]) == (a[n-1][3]):
                print("Block verified...")
            elif (a[n][2]) != (a[n-1][3]):
                print("Block is false...")
            else:
                print("Unknown error...")
            
verifyblock()