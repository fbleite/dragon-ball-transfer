from __future__ import print_function
from __future__ import division
import paramiko
import os

LOCAL_DRAGON_BALL = '/Users/fbleite/Downloads/DragonBall/'
REMOTE_DRAGON_BALL = '/home/pi/DragonBall/'
numberOfFilesToTransfer = 5

sftpURL   =  '192.168.178.25'
sftpUser  =  'pi'
sftpPass  =  'raspberry'

def printTotals(transferred, toBeTransferred):
    percentage = (transferred/toBeTransferred) * 100
    black = '#' * int(percentage)
    space = " " * (100 - int(percentage))
    bar = black + space
    print ("|{0}| {1:.2f}%".format(bar, percentage), end="\r")

ssh = paramiko.SSHClient()
# automatically add keys without requiring human intervention
ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
ssh.connect(sftpURL, username=sftpUser, password=sftpPass)
ftp = ssh.open_sftp()
ftp.chdir(REMOTE_DRAGON_BALL)

print ('Procurando o ultimo episodio no pi')
lastEpisode = 0
for i in ftp.listdir():
    if lastEpisode < int(i[:i.find('-')]): lastEpisode = int(i[:i.find('-')])

for i in ftp.listdir():
    if lastEpisode != int(i[:i.find('-')]):
        print ('Removendo arquivo: ' + REMOTE_DRAGON_BALL + i)
        ftp.remove(REMOTE_DRAGON_BALL + i)

print ("{}: {}".format("Ultimo episodio armazenado", lastEpisode))

localDBDir = os.listdir(LOCAL_DRAGON_BALL)
print ('Novos episodios a serem transferidos:')
for DBFile in localDBDir:
    if (DBFile.find('mkv') != -1):
        currentLocalFile = int(DBFile[:DBFile.find('-')])
        if  currentLocalFile > lastEpisode and currentLocalFile <= (lastEpisode + numberOfFilesToTransfer):
            print ("Transferindo Arquivo: {}".format(DBFile))
            ftp.put(LOCAL_DRAGON_BALL + DBFile, REMOTE_DRAGON_BALL + DBFile, callback=printTotals)
            print("\n")
           # print ("Deletando o arquivo no diretorio local             ")
           # os.remove(LOCAL_DRAGON_BALL + DBFile)



somevarhere=1
