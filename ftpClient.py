# client.py

import socket
import math
import sys
import time
import os
from threading import Semaphore

# Global semaphore for concurrent transfer control
MAX_CONCURRENT_TRANSFERS = 3
transfer_semaphore = Semaphore(MAX_CONCURRENT_TRANSFERS)
        
class FTPclient:
    def __init__(self, clientName):

        self.IPsocket = None
        self.DTPsocket = None
        self.errorResp = False
        self.alive = False
        self.loggedIn = False
        self.user = None
        self.remotedirList = []
        self.collectMSG = []
        self.statusMSG = ' '
        self.clientName = clientName
        self.transfer_progress = 0  # For progress tracking
        self.total_files = 0
        self.completed_files = 0
        self.progress_callback = None  # Callback for UI updates
        self.pwd = '/' # Track current working directory
        
    def initConnection(self, serverIPname, serverIPport):

        self.serverIPname = serverIPname
        self.serverIPport = serverIPport
       
        self.IPsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Try to connect to server
        try:

            self.IPsocket.connect((self.serverIPname, self.serverIPport))
            print(self.IPsocket.recv(8192).decode())

        except:

            errMSG = '连接失败 ' + self.serverIPname
            self.statusMSG = errMSG
            print(errMSG)
            self.errorResp = True
            time.sleep(3)
            return

        self.alive = True
        
        print('已连接到服务器 ;)')
    
    def getStatus(self):
        
        return self.statusMSG

    def login(self, userName, password):

        # enter username
        cmd = 'USER ' + userName
        self.send(cmd)
        self.printServerReply(self.getServerReply())

        if not self.errorResp:
            # enter password
            cmd = 'PASS ' + password
            self.send(cmd)
            self.printServerReply(self.getServerReply())

            if not self.errorResp:
                self.loggedIn = True
                self.user = userName
                msg =('登录成功\n')
                print(msg)
                self.statusMSG = msg
                

    def send(self, cmd):
        # Sending commands to server
        self.IPsocket.send((cmd + '\r\n').encode())
        # Dont print or log the password
        if cmd[:4] != 'PASS':
            print('Client: ', cmd)
            self.collectMSG.append('Client: ' + cmd)

    def getServerReply(self):

        resp = self.IPsocket.recv(8192).decode()
        self.collectMSG.append('Server: ' + resp)

        # Notify if this an error
        if resp[0] != '5' and resp[0] != '4':
            self.errorResp = False
        else:
            self.errorResp = True
        return resp

    def printServerReply(self, resp):
        
        print('Server :', resp)
    
    def setMode(self, mode):
        
        # Set mode of data transfer
        if mode.upper() == 'I' or mode.upper() == 'A':
            self.mode = mode
            cmd = 'TYPE '  + mode
            self.send(cmd)
            self.printServerReply(self.getServerReply())

        else:
            msg = ('客户端 : 错误 未知模式')
            self.statusMSG = msg
            print(msg)
    
    def getComm(self):
        return self.collectMSG
    
    def clearComm(self):
        self.collectMSG.clear()


    def startPassiveDTPconnection(self):

        # Ask for a passive connection
        cmd = 'PASV'
        self.send(cmd)
        resp = self.getServerReply()
        self.printServerReply(resp)

        if not self.errorResp:

            firstIndex = resp.find('(')
            endIndex = resp.find(')')

            # Obtain the server DTP address and Port
            addr = resp[firstIndex+1:endIndex].split(',')
            self.serverDTPname = '.'.join(addr[:-2])
            self.serverDTPport = (int(addr[4]) << 8) + int(addr[5])
            print(self.serverDTPname, self.serverDTPport)

            try:
                # Connect to the server DTP
                self.DTPsocket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                self.DTPsocket.connect(
                    (self.serverDTPname, self.serverDTPport))
                self.statusMSG = '被动连接成功，准备接收'
                print('被动连接成功，准备接收\n')
                
                self.dataConnectionAlive = True

            except:

                print('连接失败 ', self.serverDTPname)
                self.statusMSG = '连接失败 '+ self.serverDTPname
                self.dataConnectionAlive = False
                time.sleep(3)
                return

    def getList(self):
        
        self.remotedirList = []
        # Cant't get list if disconnected
        if self.dataConnectionAlive and self.alive:

            cmd = 'LIST'
            self.send(cmd)
            self.printServerReply(self.getServerReply())
            
            print('\n正在接收数据...\n')
            self.statusMSG = '正在接收数据...'

            full_data = b""
            while True:
                # Get the directory list
                data = self.DTPsocket.recv(1024)
                if not data:
                    break
                full_data += data

            # Decode and split into lines
            try:
                decoded_data = full_data.decode('utf-8')
            except UnicodeDecodeError:
                # Fallback to latin-1 if utf-8 fails
                decoded_data = full_data.decode('latin-1')

            lines = decoded_data.split('\r\n')
            for line in lines:
                if line.strip():
                    print(line)
                    self.remotedirList.append(line)

            print('目录列表获取完成!\n')
            self.statusMSG ='目录列表获取完成!'
            self.DTPsocket.close()
            self.printServerReply(self.getServerReply())
    
    def downloadFile(self,fileName):
        
        # Send download command
        cmd = 'RETR ' +  fileName
        self.send(cmd)
        self.printServerReply(self.getServerReply())
        
        # Dont continue if there is an error 
        if not self.errorResp:
            
            # Create Downloads folder if not exist
            downloadFolder = 'Downloads'
            if not os.path.exists(downloadFolder):
                os.makedirs(downloadFolder)
            
            # Mode of data transfer
            if self.mode == 'I':
                outfile = open(downloadFolder + '/' + fileName, 'wb')
            else:
                outfile = open(downloadFolder + '/' + fileName, 'w')
            
            # Get them packets :D
            print('正在接收数据...')
            self.statusMSG = '正在接收数据...'
            
            while True:
                data = self.DTPsocket.recv(8192)
                if not data:
                    break
                outfile.write(data)
            outfile.close()
            # Done
            print('传输成功')
            self.statusMSG = '传输成功'
            self.DTPsocket.close()
            self.printServerReply(self.getServerReply())

    def downloadFileTo(self, fileName, localPath):

        # Similar to downloadFile but writes to provided localPath
        cmd = 'RETR ' +  fileName
        self.send(cmd)
        self.printServerReply(self.getServerReply())

        if not self.errorResp:
            # Ensure local directory exists
            local_dir = os.path.dirname(localPath)
            if local_dir and not os.path.exists(local_dir):
                os.makedirs(local_dir, exist_ok=True)

            if self.mode == 'I':
                outfile = open(localPath, 'wb')
            else:
                outfile = open(localPath, 'w')

            print('正在接收数据...')
            self.statusMSG = '正在接收数据...'

            while True:
                data = self.DTPsocket.recv(8192)
                if not data:
                    break
                outfile.write(data)
            outfile.close()
            print('传输成功')
            self.statusMSG = '传输成功'
            self.DTPsocket.close()
            self.printServerReply(self.getServerReply())


    def upload_folder(self, local_path, remote_base='/'):
        """
        Recursively upload a local folder to remote_base on the server.
        remote_base should be the full path including the folder name to create.
        E.g., to upload 'work' folder to '/uploads', remote_base = '/uploads/work'
        """
        if not os.path.exists(local_path):
            print('错误: 本地路径不存在')
            return

        # Normalize paths
        local_path = os.path.abspath(local_path)
        remote_base = remote_base.rstrip('/')
        if not remote_base:
            remote_base = '/'
        
        # Count total files first for progress
        self.total_files = sum([len(files) for _, _, files in os.walk(local_path)])
        self.completed_files = 0

        # Ensure remote_base directory is created by navigating step by step
        self.changeWD('/')
        if remote_base != '/':
            parts = [p for p in remote_base.strip('/').split('/') if p]
            current_path = ''
            for p in parts:
                current_path += '/' + p
                self.changeWD(current_path)
                if self.errorResp:
                    # Directory doesn't exist, create it
                    # Go back to parent
                    parent_path = '/' + '/'.join(current_path.strip('/').split('/')[:-1])
                    if parent_path == '//':
                        parent_path = '/'
                    self.changeWD(parent_path)
                    self.makeDir(p)
                    self.changeWD(current_path)

        # Now we are in remote_base, upload all contents
        for dirpath, dirnames, filenames in os.walk(local_path):
            rel = os.path.relpath(dirpath, local_path)
            
            # Determine current remote directory
            if rel != '.':
                # Build absolute remote path
                if remote_base == '/':
                    remote_dir = '/' + rel.replace(os.sep, '/')
                else:
                    remote_dir = remote_base + '/' + rel.replace(os.sep, '/')
                
                # Ensure all parent directories exist
                # Split the relative path and create each level
                rel_parts = rel.split(os.sep)
                current_remote = remote_base
                
                for part in rel_parts:
                    parent_remote = current_remote
                    if current_remote == '/':
                        current_remote = '/' + part
                    else:
                        current_remote = current_remote.rstrip('/') + '/' + part
                    
                    # Try to navigate to this directory
                    self.changeWD(current_remote)
                    if self.errorResp:
                        # Directory doesn't exist, go back to parent and create it
                        self.changeWD(parent_remote)
                        self.makeDir(part)
                        self.changeWD(current_remote)
                        if self.errorResp:
                            print(f'警告: 无法创建或访问目录 {current_remote}')
            else:
                # Root of upload - ensure we are at remote_base
                self.changeWD(remote_base)

            # Upload files in this directory
            for fname in filenames:
                local_file = os.path.join(dirpath, fname)
                # Acquire semaphore for concurrent control
                transfer_semaphore.acquire()
                try:
                    # Always use passive by default
                    self.startPassiveDTPconnection()
                    if not getattr(self, 'dataConnectionAlive', False):
                        print('无法打开数据连接: ', local_file)
                        continue
                    self.uploadFile(local_file)
                    self.completed_files += 1
                    if self.progress_callback:
                        progress = int((self.completed_files / self.total_files) * 100)
                        self.progress_callback(progress, f'{self.completed_files}/{self.total_files}')
                finally:
                    transfer_semaphore.release()

    def download_folder(self, remote_base='/', local_path='Downloads'):
        """Recursively download a remote directory into local_path."""
        # Ensure local path exists
        os.makedirs(local_path, exist_ok=True)

        # Navigate to remote directory
        self.changeWD('/')
        self.changeWD(remote_base)
        if self.errorResp:
            print(f'错误: 无法访问远程目录 {remote_base}')
            return

        # List current remote directory
        self.startPassiveDTPconnection()
        self.getList()
        
        # Parse directory listing (tab-delimited format)
        entries = []
        for line in self.remotedirList:
            if not line.strip():
                continue
            
            # Split by tab - format: perms \t links user \t group \t \t size \t date \t filename
            parts = line.split('\t')
            if len(parts) >= 7:
                perms = parts[0].strip()
                filename = parts[6].strip()
                
                # Skip . and ..
                if filename in ['.', '..']:
                    continue
                
                is_dir = perms.startswith('d')
                entries.append((filename, is_dir))

        # Count files for progress
        file_count = sum(1 for name, is_dir in entries if not is_dir)
        if not hasattr(self, 'total_files') or self.total_files == 0:
            self.total_files = file_count
            self.completed_files = 0

        # Process each entry
        for filename, is_dir in entries:
            if is_dir:
                # Directory -> recurse
                if remote_base == '/':
                    child_remote = '/' + filename
                else:
                    child_remote = remote_base.rstrip('/') + '/' + filename
                    
                child_local = os.path.join(local_path, filename)
                os.makedirs(child_local, exist_ok=True)
                
                # Save current path and recurse
                original_path = self.pwd
                self.download_folder(child_remote, child_local)
                # Return to current directory
                self.changeWD(original_path)
            else:
                # File -> download
                transfer_semaphore.acquire()
                try:
                    self.startPassiveDTPconnection()
                    if not getattr(self, 'dataConnectionAlive', False):
                        print('无法打开数据连接: ', filename)
                        continue
                    local_file = os.path.join(local_path, filename)
                    self.downloadFileTo(filename, local_file)
                    self.completed_files += 1
                    if self.progress_callback:
                        progress = int((self.completed_files / self.total_files) * 100) if self.total_files > 0 else 100
                        self.progress_callback(progress, f'{self.completed_files}/{self.total_files}')
                finally:
                    transfer_semaphore.release()
            
    
    def uploadFile(self,filePath):

        #Check if file path is valid
        if os.path.exists(filePath):
            # Get the file name
            fileName = os.path.basename(filePath)

            # Send Command
            cmd = 'STOR ' + fileName
            self.send(cmd)
            self.printServerReply(self.getServerReply())
        
            # Continue if there are no errors reported
            if not self.errorResp:
                print('正在上传 ' + fileName + ' 到服务器...')
                self.statusMSG = '正在上传 ' + fileName + ' 到服务器...'

                if self.mode == 'I':
                    uFile = open(filePath, 'rb')
                else:
                    uFile = open(filePath, 'r')
                
                # Send packets of the file
                data =  uFile.read(8192)

                while data:

                    if self.mode == 'I':
                        self.DTPsocket.send(data)
                    else:
                        self.DTPsocket.send(data.encode())
                    data = uFile.read(8192)

                uFile.close()
                print('上传成功')
                self.statusMSG = ' 上传成功'
                self.DTPsocket.close()
                self.printServerReply(self.getServerReply())
                
        else:
            print('错误: 无效路径!')
            self.statusMSG = '错误: 无效路径!'
            self.DTPsocket.close()
            
    def returnDirList(self):

        return self.remotedirList
    
    def changeWD(self,dir_):

        # Change working directory
        cmd = 'CWD ' + dir_
        self.send(cmd)
        self.printServerReply(self.getServerReply())
        
        if not self.errorResp:
            if dir_.startswith('/'):
                # Absolute path
                self.pwd = dir_
            elif dir_ == '/' or dir_ == '.':
                self.pwd = '/'
            elif dir_ == '..':
                if self.pwd != '/':
                    self.pwd = os.path.dirname(self.pwd.rstrip('/'))
                    if not self.pwd: 
                        self.pwd = '/'
            else:
                # Relative path
                if self.pwd == '/':
                    self.pwd = '/' + dir_
                else:
                    self.pwd = self.pwd.rstrip('/') + '/' + dir_
    
    def makeDir(self,folderName):
        
        # Create a new directory on server
        cmd = 'MKD ' + folderName
        self.send(cmd)
        self.printServerReply(self.getServerReply())
    
    def remDir(self,folderName):

        # Delete directory on server
        cmd = 'RMD ' + folderName
        self.send(cmd)
        self.printServerReply(self.getServerReply())
        
    def deleteFile(self, fileName):
        # Delete file on server
        cmd = 'DELE ' + fileName
        self.send(cmd)
        self.printServerReply(self.getServerReply())

    def rename(self, oldName, newName):
        # Rename file/dir on server
        cmd = 'RNFR ' + oldName
        self.send(cmd)
        self.printServerReply(self.getServerReply())
        
        if not self.errorResp:
            cmd = 'RNTO ' + newName
            self.send(cmd)
            self.printServerReply(self.getServerReply())

    def logout(self):
        
        #Close connection
        cmd = 'QUIT'
        self.send(cmd)
        self.printServerReply(self.getServerReply())
        self.statusMSG = '已登出，连接关闭'
        
    def checkConnection(self):
        
        cmd = 'NOOP'
        self.send(cmd)
        self.printServerReply(self.getServerReply())
