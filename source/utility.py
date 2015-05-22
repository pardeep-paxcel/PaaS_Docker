import socket
import string
import random
import re
import shutil
import os
import json

def removeDirIfExist(localRepoPath):
    if os.path.isdir(localRepoPath):
        print("dir exit going to remove it")
        shutil.rmtree(localRepoPath)
    else:
       print("dir doesnt exits")

def getAvailablePort():
    dummySocket = socket.socket()
    dummySocket.bind(('',0))
    availablePort = dummySocket.getsockname()[1]
    dummySocket.close()
    print('Avil',' ',availablePort)
    return availablePort

def getExposedPortNumber(dockerFilePath):
    exitFlag = False
    with open(dockerFilePath) as dockerFile:
        for line in dockerFile:
            for word in line.split():
                if exitFlag:
                    privatePortNumber = word
                    return privatePortNumber
                if 'EXPOSE' in line or 'expose' in line:
                    exitFlag=True

def getPorts(portsUsed,repoFullName):
    portToBeUsed = {}
    if len(portsUsed):
        portToBeUsed['publicPort'] = portsUsed[0]['PublicPort']
        portToBeUsed['privatePort'] = portsUsed[0]['PrivatePort']
    else:
        portToBeUsed['publicPort'] = getAvailablePort()
        portToBeUsed['privatePort'] = int(getExposedPortNumber(repoFullName+'/Dockerfile'))
    return portToBeUsed

def branchNameGenerator(size=6, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
    
def verifyBranchName(branchName):
    branchNameRegex = "^[a-z0-9_.-]+$"
    branchNameValidator = re.compile(branchNameRegex)
    if branchNameValidator.match(branchName):
        return branchName
    else:
        return branchNameGenerator() 
