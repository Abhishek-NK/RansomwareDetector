import os
from subprocess import check_output
import time

def kill_process():
        #get processes accessing file
        output = check_output("handle.exe -a C:\Users\IEUser\Documents", shell=True)

        #create an array of processes
        data = output.split("\n")

        #iterate through the array of processes
        for i in range(5, len(data)-1):
            process_split = data[i].split(" ")

            #whitelist of processes
            if (process_split[0] == "handle.exe"):
                pass
            elif (process_split[0] == "python.exe" and int(process_split[10]) == int(os.getpid())):
                pass
            else:
                #if the process isn't normal then log it and kill it
                file = open('C:\\Users\\IEUser\\Desktop\\log file\\log.txt', "a")
                file.write(data[i] + "\n")
                file.close()

                #kill the process trying to access honey file
                print "\n" + process_split[0]
                b = process_split[0]
                os.system("taskkill /f /im " + b)

        #count number of files in \Documents after attack
        counter1 = sum([len(files) for r, d, files in os.walk("C:\Users\IEUser\Documents")])

        #create list for all files in \Documents after attack
        list_files1 = os.listdir("C:\Users\IEUser\Documents")
        files1 = []
        for m in range(len(list_files1)):
            if ' ' in list_files1[m]:
                pass
            else:
                files1.append(list_files1[m])

        #check if the hashes match after attack
        encrypted_files = []
        flag_deleted = True
        for n in range(0, len(files)):
            for o in range(0, len(files1)):
                #compare name of file first
                if files[n] == files1[o]:
                    #flag to show the file hasn't been deleted
                    flag_deleted = False
                    #then check hash of files
                    hash_string1 = check_output("certUtil -hashfile " + files1[o] + " MD5", shell=True)
                    hash_output1 = hash_string1.split("\n")
                    hashes1 = hash_output1[1]

                    try:
                        if hashes[n] != hashes1:
                            #inform if a file's hash doesn't match the original (the file has been encrypted)
                            encrypted_files.append(files[n])
                            print("ENCRYPTED FILE: " + files[n])
                        else:
                            print("SAFE FILE: " + files[n])
                    except:
                        pass
                else:
                    pass

            #if the file wasn't found then it's been deleted.
            if flag_deleted == True:
                print("ENCRYPTED FILE: " + files[n])

#create path for the log file in Desktop
newpath = r'C:\\Users\\IEUser\\Desktop\\log file'
if not os.path.exists(newpath):
    os.makedirs(newpath)

#create honey file1
file = open("password.txt", "w")
file.write("baguette")
file.close()

#create honey file2
file = open("apassword.txt", "w")
file.write("cheese")
file.close()

#create honey file3
file = open("bpassword.txt", "w")
file.write("tomato")
file.close()

#count number of files in \Documents
counter = sum([len(files) for r, d, files in os.walk("C:\Users\IEUser\Documents")])
print(counter)

#create list for all files in \Documents
list_files = os.listdir("C:\Users\IEUser\Documents")
files = []
for l in range(len(list_files)):
    if ' ' in list_files[l]:
        pass
    else:
        files.append(list_files[l])

#produce hash for each file in \Documents
hashes = [0] * len(files)
for k in range(len(files)):
    hash_string = check_output("certUtil -hashfile " + files[k] + " MD5", shell=True)
    hash_output = hash_string.split("\n")
    hashes[k] = hash_output[1]
    print(files[k] + " " + hashes[k])

#produce hashes of the honey files
honey_hash1 = check_output("certUtil -hashfile password.txt MD5", shell=True).split("\n")[1]
honey_hash2 = check_output("certUtil -hashfile apassword.txt MD5", shell=True).split("\n")[1]
honey_hash3 = check_output("certUtil -hashfile bpassword.txt MD5", shell=True).split("\n")[1]


while True:

    #check that the malware hasn't deleted any honey files
    if os.path.isfile("apassword.txt") == False or os.path.isfile("bpassword.txt") == False or os.path.isfile("password.txt") == False:
        kill_process()

    #check that the malware hasn't created any files
    counter_check = sum([len(files) for r, d, files in os.walk("C:\Users\IEUser\Documents")])
    if counter != counter_check:
        kill_process()

    #recompute the hashes of the honey files
    check_honey1 = check_output("certUtil -hashfile password.txt MD5", shell=True).split("\n")[1]
    check_honey2 = check_output("certUtil -hashfile apassword.txt MD5", shell=True).split("\n")[1]
    check_honey3 = check_output("certUtil -hashfile bpassword.txt MD5", shell=True).split("\n")[1]

    #check that malware hasn't changed any files
    #check if the hash of any of the honey files changed, if a hash changed then kill processes
    if honey_hash1 != check_honey1 or honey_hash2 != check_honey2 or honey_hash3 != check_honey3:
        kill_process()

        honey_hash1 = check_honey1
        honey_hash2 = check_honey2
        honey_hash3 = check_honey3
