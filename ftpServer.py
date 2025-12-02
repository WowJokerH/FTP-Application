import socket
import os
import time
import threading
import math

# Globals for connection and transfer tracking
active_connections = 0
active_connections_lock = threading.Lock()
transfer_status = {}
transfer_id_counter = 0
transfer_lock = threading.Lock()

def print_status():
    """Periodically print server status"""
    while True:
        time.sleep(10)  # Print every 10 seconds
        with active_connections_lock:
            conn_count = active_connections
        with transfer_lock:
            active_transfers = [tid for tid, info in transfer_status.items() if info['status'] == 'running']
            completed_transfers = [tid for tid, info in transfer_status.items() if info['status'] == 'completed']
        
        print('\n' + '='*50)
        print(f'服务器状态 [{time.strftime("%H:%M:%S")}]')
        print(f'活跃连接数: {conn_count}')
        print(f'正在传输: {len(active_transfers)}')
        print(f'已完成传输: {len(completed_transfers)}')
        if active_transfers:
            print('当前传输任务:')
            with transfer_lock:
                for tid in active_transfers[:5]:  # Show max 5
                    info = transfer_status[tid]
                    print(f"  [{tid}] {info['direction']} {info['file']} - {info['bytes']/1024:.1f}KB")
        print('='*50 + '\n')


class TransferThread(threading.Thread):
    def __init__(self, DTPsocket, filepath, mode, direction, client_addr, transfer_id, serverSocket=None, pasv=False):
        threading.Thread.__init__(self)
        self.DTPsocket = DTPsocket
        self.filepath = filepath
        self.mode = mode
        self.direction = direction
        self.client_addr = client_addr
        self.transfer_id = transfer_id
        self.serverSocket = serverSocket
        self.pasv = pasv

    def run(self):
        global transfer_status, transfer_lock
        try:
            if self.direction == 'upload':
                # write incoming data to file
                # open in binary or text as per mode
                if self.mode == 'I':
                    out = open(self.filepath, 'wb')
                else:
                    out = open(self.filepath, 'w')

                total = 0
                while True:
                    data = self.DTPsocket.recv(8192)
                    if not data:
                        break
                    out.write(data)
                    total += len(data)
                    with transfer_lock:
                        transfer_status[self.transfer_id]['bytes'] = total

                out.close()

            elif self.direction == 'download':
                if self.mode == 'I':
                    f = open(self.filepath, 'rb')
                else:
                    f = open(self.filepath, 'r')
                total = 0
                data = f.read(8192)
                while data:
                    if self.mode == 'I':
                        self.DTPsocket.send(data)
                    else:
                        self.DTPsocket.send((data+'\r\n').encode())
                    total += len(data)
                    with transfer_lock:
                        transfer_status[self.transfer_id]['bytes'] = total
                    data = f.read(8192)
                f.close()

            with transfer_lock:
                transfer_status[self.transfer_id]['status'] = 'completed'

        except Exception as e:
            with transfer_lock:
                transfer_status[self.transfer_id]['status'] = 'error'
                transfer_status[self.transfer_id]['error'] = str(e)
            print('Transfer error:', e)

        finally:
            try:
                self.DTPsocket.close()
            except Exception:
                pass
            if self.pasv and self.serverSocket:
                try:
                    self.serverSocket.close()
                except Exception:
                    pass

class serverThread(threading.Thread):
    
    def __init__(self, conn, addr,usersDB, currDir,IP, port):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.serverIP = IP
        self.serverPort = port
        self.baseWD = currDir
        self.cwd = self.baseWD
        self.rest = False
        self.PASVmode = False
        self.isLoggedIn = False
        self.users = usersDB
        self.validUser = False
        self.isConnected = True
        self.islist = False
        self.mode = 'I' #Default Mode
        self.allowDelete = True
    
    def run(self):

        self.isConnected = True
        # Welcome Message
        resp = '220 Welcome!'
        self.sendReply(resp)
        # Await for connection from clients
        while True:
            
            cmd = self.conn.recv(256).decode()
            
            if not cmd or not self.isConnected : break
            else:
                print('Recieved: ', cmd)
                try:
                    func = getattr(self,cmd[:4].strip().upper())
                    func(cmd)
                except Exception as err:
                    print('Error: ', err)
                    resp = '500 Syntax error, command unrecognized.'
                    self.sendReply(resp)
        
        self.conn.close()
        # decrement active connections
        try:
            global active_connections
            with active_connections_lock:
                active_connections -= 1
            print('Connection closed. Active connections:', active_connections)
        except Exception:
            pass
   
    def sendReply(self,reply):
        self.conn.send((reply + '\r\n').encode())
    
    def notLoggedInMSG(self):
        res = '530 Please login with USER and PASS.'
        self.sendReply(res)

    def paramError(self,cmd):
        res = '501 \'' + cmd[:-2] + '\': parameter not understood.' 
        self.sendReply(res)
    
    def resetState(self):
         
        # RESET STATE of affairs
        self.isLoggedIn = False
        self.validUser = False
        self.user = None


    def SYST(self,cmd):
        resp = '215 UNIX Type: L8.'
        self.sendReply(resp)
    
    def USER(self,cmd):
        
        #RESET STATE, Incase someone logs in while the other is still logged in
        self.resetState()

        # Extract username in the command
        self.user = cmd[5:-2]
        
        try:
            # Read users file
            with open(self.users, 'r') as f:
                users = f.readlines()
            
            # Check if user exists on the database
            for u in users:
                parts = u.strip().split()
                if len(parts) >= 2 and self.user == parts[0]:
                    self.validUser = True
                    resp = '331 User name okay, need password.'
                    self.sendReply(resp)
                    break
        except Exception as e:
            print(f"User auth error: {e}")
                
        if not self.validUser:    
            resp = '530 Invalid User.'
            self.sendReply(resp)
            self.validUser = False
    
    def PASS(self,cmd):
        
        # Check if user name is entered
        if self.validUser:
            password = cmd[5:-2]
            try:
                with open(self.users, 'r') as f:
                    pws = f.readlines()

                # Check if password matches user
                for p in pws:
                    parts = p.strip().split()
                    if len(parts) >= 2:
                        if self.user == parts[0] and password == parts[1]:
                            self.isLoggedIn = True
                            resp = '230 User logged in, proceed.'
                            self.sendReply(resp)
                            break
            except Exception as e:
                print(f"Pass auth error: {e}")

            if not self.isLoggedIn:
                resp = '530 Invalid password for '  + self.user
                self.sendReply(resp)
        else:
            self.notLoggedInMSG()
    
    def QUIT(self,cmd):

        # If the user is logged in, they are logged out
        if self.isLoggedIn:

            self.resetState()
            resp = '221 Logged out'
            self.sendReply(resp)
    
        else:

            resp = '221 Service closing control connection'
            self.sendReply(resp)
            self.isConnected = False
        

    def STRU(self,cmd):
         # Obsolete command
        stru = cmd[5]

        if stru == 'F':
            resp = '200 F.'
        else:
            resp = '504 Command obsolete'

        self.sendReply(resp)

    def MODE(self,cmd):
        
        # Obsolete command
        mode = cmd[5]

        if mode == 'S':
            resp = '200 MODE set to stream.'
        else:
            resp = '504 Command obsolete'

        self.sendReply(resp)

       
    def NOOP(self,cmd):

        # To check if the connection is alive
        resp = '200 OK.'
        self.sendReply(resp)
    
    def TYPE(self,cmd):

        # ASCII or Binary Mode
        mode = cmd[5]
        
        # Confirm I or A
        if mode.upper() == 'I':
            self.mode = mode
            resp = '200 Binary mode.'
            self.sendReply(resp)
        elif mode.upper() == 'A':
            self.mode = mode
            resp = '200 ASCII mode.'
            self.sendReply(resp)
        else:
            # Unknown parameter
            self.paramError(cmd)

    def PWD(self,cmd):
        
        # Cant't print working directory if not looged in
        if self.isLoggedIn:
            
            # The path relative to the root
            tempDir = '/' + self.cwd
            cwd = os.path.relpath(tempDir,'/')
            
            if cwd == '.':
                cwd = '/'
            else:
                cwd = '/' + cwd 
            resp = '257' + ' "' + cwd + '" is the current dir.'
            self.sendReply(resp)

        else:
            self.notLoggedInMSG()

    def CWD(self,cmd):

        if self.isLoggedIn: 
            # Get the directory
            chwd = cmd[4:-2]
         
            # Base directory?
            if chwd == '.' or chwd == '/':
                self.cwd = self.baseWD
                resp = '250 OK.'
                self.sendReply(resp)
            else:
                # Handle absolute path
                if chwd.startswith('/'):
                    # Absolute path from root
                    chwd = chwd[1:]  # Remove leading /
                    tempCwd = os.path.join(self.baseWD, chwd)
                else:
                    # Relative path from current dir
                    tempCwd = os.path.join(self.cwd, chwd)
                
                # Security check: ensure we don't go above baseWD
                abs_base = os.path.abspath(self.baseWD)
                abs_new = os.path.abspath(tempCwd)
                
                if not abs_new.startswith(abs_base):
                     resp = '550 Access denied.'
                     self.sendReply(resp)
                     return

                # Does the path exist?
                if os.path.exists(tempCwd) and os.path.isdir(tempCwd):
                    self.cwd = tempCwd
                    resp = '250 OK.'
                    self.sendReply(resp)
                else:
                    resp = '550 The system cannot find the file specified.'
                    self.sendReply(resp)
           
        else:
            self.notLoggedInMSG()

    def PASV(self,cmd):
        # Cant't try to establish connection without logging in
        if self.isLoggedIn:
            self.PASVmode = True

            self.serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.serverSocket.bind((self.serverIP,0))
            self.serverSocket.listen(1)

            ip, port = self.serverSocket.getsockname()
        
            # Condition IP with the RFC959 standard
            ip = ip.split('.')
            ip = ','.join(ip)
        
            # Condition the port with the RFC959 standard
            p1 = math.floor(port/256)
            p2 = port%256
            print('open...\nIP: ' + str(ip) +'\nPORT: '+ str(port))
        
            # Prepare the connection settings for take-off
            resp = '227 Entering Passive Mode (' + str(ip) + ',' + str(p1) + ',' +str(p2) + ').'
            self.sendReply(resp)

        else:
            self.notLoggedInMSG()

    def PORT(self,cmd):
        
        # Cant't try to establish connection without logging in
        if self.isLoggedIn:
    
            # check if Passive Mode
            if self.PASVmode:
                self.serverSocket.close()
                self.PASVmode = False

            # Split the connection settings
            conSettings = cmd[5:].split(',')
        
            # Generate the IP address from the connection settings 
            self.DTPaddr = '.'.join(conSettings[:4])

            # Generate the PORT from the connection settings
            # This is with respect to RFC959
            self.DTPport = ((int(conSettings[4])<<8)) + int(conSettings[5])
            
            print('Connected to :', self.DTPaddr, self.DTPport)
            # Acknowledge
            resp = '200 Got it.'
            self.sendReply(resp)

            self.DTPsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.DTPsocket.connect((self.DTPaddr,self.DTPport))

        else:
            self.notLoggedInMSG()

    def startDTPsocket(self):
        
        try:
            if self.PASVmode:
                self.DTPsocket, addr = self.serverSocket.accept()
                print('connect: ', addr)
                
        except socket.error:
            resp = '425 Cannot open Data Connection'
            self.sendReply(resp)

    def stopDTPsocket(self):

        self.DTPsocket.close()
        if self.PASVmode:
            self.serverSocket.close()
    
    def sendData(self, data):

        # Mode of sending?
        if not self.islist and self.mode == 'I':
            self.DTPsocket.send((data))   
        else:
            self.DTPsocket.send((data+'\r\n').encode())

    def toList(self,l):
        try:
            st = os.stat(l)
            fullmode ='rwxrwxrwx'
            mode = ''
            
            # Prep the directory listing with regards to RFC959
            for i in range(9):
                mode+=((st.st_mode>>(8-i))&1) and fullmode[i] or '-'
            
            d = (os.path.isdir(l)) and 'd' or '-'
            fhist = time.strftime(' %b %d %H:%M ',time.gmtime(st.st_mtime))
            return d + mode+ '\t1 user'+'\t group \t\t' + str(st.st_size) + '\t' + fhist + '\t' + os.path.basename(l)
        except Exception as e:
            print(f"Error getting stats for {l}: {e}")
            return None

    def LIST(self,cmd):
        
        # Can't list if not logged in
        if self.isLoggedIn:

            resp = '150 File status okay; about to open data connection.'
            self.sendReply(resp)
            print('list: ', self.cwd)
            
            # Ready the socket for data transfer
            self.startDTPsocket()

            # Get each file in the directory
            try:
                files = sorted(os.listdir(self.cwd))
                for l in files:
                    ll = self.toList(os.path.join(self.cwd,l))
                    if ll:
                        # Send as str/ASCII
                        self.islist = True
                        self.sendData(ll)
                        self.islist = False
            except Exception as e:
                print(f"List error: {e}")
            
            # Done
            self.stopDTPsocket()

            resp = '200 Listing completed.'
            self.sendReply(resp)

        else:
            self.notLoggedInMSG()

    def MKD(self,cmd):

        #Can't make new directory if not logged in
        if self.isLoggedIn:
            dirName = os.path.join(self.cwd,cmd[4:-2])
            try:
                os.mkdir(dirName)
                resp = '257 Directory created.'
                self.sendReply(resp)
            except FileExistsError:
                resp = '550 Directory already exists.'
                self.sendReply(resp)
            except Exception as e:
                resp = f'550 Cannot create directory: {str(e)}'
                self.sendReply(resp)
        else:
            self.notLoggedInMSG()

    def RMD(self,cmd):
        
        # Can't delete directory if not logged in
        if self.isLoggedIn:
            
            dirName = os.path.join(self.cwd,cmd[4:-2])

            # Check if specified path exists

            if os.path.exists(dirName):

                # Allow deletion if only deletion is allowed
                if self.allowDelete:
                    try:
                        # Use shutil.rmtree for recursive deletion
                        import shutil
                        shutil.rmtree(dirName)
                        resp = '250 Directory deleted.'
                        self.sendReply(resp)
                    except Exception as e:
                        resp = f'550 Error: {str(e)}'
                        self.sendReply(resp)
                else:
                    resp = '450 Not allowed.'
                    self.sendReply(resp)
            else:
                resp = '550 The system cannot find the file specified.'
                self.sendReply(resp)
        else:
            self.notLoggedInMSG()

    def DELE(self, cmd):
        # Delete file
        if self.isLoggedIn:
            fileName = os.path.join(self.cwd, cmd[5:-2])
            if os.path.exists(fileName):
                if self.allowDelete:
                    try:
                        os.remove(fileName)
                        resp = '250 File deleted.'
                        self.sendReply(resp)
                    except Exception as e:
                        resp = f'550 Error deleting file: {str(e)}'
                        self.sendReply(resp)
                else:
                    resp = '450 Not allowed.'
                    self.sendReply(resp)
            else:
                resp = '550 File not found.'
                self.sendReply(resp)
        else:
            self.notLoggedInMSG()

    def RNFR(self, cmd):
        if self.isLoggedIn:
            self.renameFrom = os.path.join(self.cwd, cmd[5:-2])
            if os.path.exists(self.renameFrom):
                resp = '350 Ready for RNTO.'
                self.sendReply(resp)
            else:
                resp = '550 File not found.'
                self.sendReply(resp)
        else:
            self.notLoggedInMSG()

    def RNTO(self, cmd):
        if self.isLoggedIn:
            if hasattr(self, 'renameFrom'):
                renameTo = os.path.join(self.cwd, cmd[5:-2])
                try:
                    os.rename(self.renameFrom, renameTo)
                    resp = '250 Rename successful.'
                    self.sendReply(resp)
                except Exception as e:
                    resp = f'550 Rename failed: {str(e)}'
                    self.sendReply(resp)
                finally:
                    del self.renameFrom
            else:
                resp = '503 Bad sequence of commands.'
                self.sendReply(resp)
        else:
            self.notLoggedInMSG()


      
    def STOR(self,cmd):

        # Cant store files if not logged in
        if self.isLoggedIn:

            # Create file path
            fileName = os.path.join(self.cwd,cmd[5:-2])
            print('Uploading: ', fileName)
            # Prepare transfer status and spawn transfer thread
            resp = '150 Opening data connection.'
            self.sendReply(resp)

            # Ready the socket for upload
            self.startDTPsocket()

            # register transfer
            global transfer_id_counter, transfer_status, transfer_lock
            with transfer_lock:
                transfer_id_counter += 1
                tid = transfer_id_counter
                transfer_status[tid] = {'client': self.addr, 'file': fileName, 'direction': 'upload', 'bytes': 0, 'status': 'running'}

            t = TransferThread(self.DTPsocket, fileName, self.mode, 'upload', self.addr, tid, getattr(self, 'serverSocket', None), self.PASVmode)
            t.start()
            # Wait until transfer completes to send final reply (FTP semantics)
            t.join()

            resp = '226 Transfer complete.'
            self.sendReply(resp)
            print('Upload success')
        
        else:
            self.notLoggedInMSG()

    def RETR(self,cmd):

        # Cant retrieve files if not logged in
        if self.isLoggedIn:
         
            fileName = os.path.join(self.cwd, cmd[5:-2])
            
            # For Filezilla
            if fileName[0] == '/':
                fileName = fileName[1:]
            
            # Check if file exist
            if os.path.exists(fileName):
                print('Downloading :', fileName)

                # Open data connection
                resp = '150 Opening file data connection.'
                self.sendReply(resp)

                # Ready the socket for download
                self.startDTPsocket()

                # register transfer
                global transfer_id_counter, transfer_status, transfer_lock
                with transfer_lock:
                    transfer_id_counter += 1
                    tid = transfer_id_counter
                    transfer_status[tid] = {'client': self.addr, 'file': fileName, 'direction': 'download', 'bytes': 0, 'status': 'running'}

                t = TransferThread(self.DTPsocket, fileName, self.mode, 'download', self.addr, tid, getattr(self, 'serverSocket', None), self.PASVmode)
                t.start()
                t.join()

                resp = '226 Transfer complete.'
                self.sendReply(resp)
            else:
                # File does not exist
                resp = '550 The system cannot find the file specified.'
                self.sendReply(resp)
        else:
            self.notLoggedInMSG()

        
class FTPserver(threading.Thread):

    # The lookout class, waits for contact from client

    def __init__(self,usersDB,homeDir,IP,Port):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.serverIP = IP
        self.serverPort = Port
        self.sock.bind((self.serverIP, self.serverPort))
        self.usersDB = usersDB
        self.homeDir = homeDir
        threading.Thread.__init__(self)
    
    def run(self):
        self.sock.listen(5)
        while True:
            connectionSocket, addr = self.sock.accept()
            thread = serverThread(connectionSocket, addr,self.usersDB, self.homeDir,self.serverIP,self.serverPort)
            thread.daemon = True
            thread.start()
            # increment active connections
            global active_connections
            with active_connections_lock:
                active_connections += 1
            print('New connection from', addr, 'Active connections:', active_connections)
    
    def stop(self):
        self.sock.close()

def Main():
    
    serverPort = 2121  # Changed to non-privileged port for Windows development

    try:
        # Try to get the local IP address that connects to the internet
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.connect(("8.8.8.8", 80))
        serverIP = server.getsockname()[0]
        server.close()
    except Exception:
        # Fallback to localhost if no internet connection
        serverIP = '127.0.0.1'

    # Database for users
    users = './users.txt'

    # Default directory
    homeDir = '.'

    # Make new thread for each new connection

    cThread = FTPserver(users,homeDir,serverIP,serverPort)
    cThread.daemon = True
    cThread.start()

    # Start status monitoring thread
    statusThread = threading.Thread(target=print_status, daemon=True)
    statusThread.start()

    # Wait for contact
    print('FTP服务器运行中:', serverIP, ':', serverPort)
    print('提示: 服务器状态每10秒自动显示')
    input('按回车键结束...\n')
    cThread.stop()
    
    
Main()