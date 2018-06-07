from PyQt5.QtCore import QThread
from PyQt5.QtNetwork import QNetworkAccessManager,QNetworkRequest,QNetworkReply
from qtasync import CallbackEvent
from ftplib import FTP
import os
from PyQt5.QtCore import QUrl,QIODevice,QFile
import threading

def uploadThis( path, myFTP):
    print(path)
    files = os.listdir(path)
    os.chdir(path)
    for f in files:
        if os.path.isfile(path + r'\{}'.format(f)):
            fh = open(f, 'rb')
            myFTP.storbinary('STOR %s' % f, fh)
            fh.close()
        elif os.path.isdir(path + r'\{}'.format(f)):
            myFTP.mkd(f)
            myFTP.cwd(f)
            uploadThis(path + r'\{}'.format(f), myFTP)
    myFTP.cwd('..')
    os.chdir('..')


def onClickPushButton( myPath):
    print(myPath)
    print('hola')
    server = '127.0.0.1'
    username = 'cvr'
    password = '123456'
    my_ftp = FTP(server, username, password)
    # myPath = 'C:/Users/BDI/Documents/Jorge/samples'

    uploadThis(myPath, my_ftp)
    my_ftp.close()
    print('hola2')

class MyThread2(threading.Thread):

    def __init__(self, src):
        ###############
        # Add ftp connection here!
        self.ftp = FTP('127.0.0.1')  # connect to host, default port
        self.ftp.login('cvr','123456')  # user anonymous, passwd anonymous@
        ################
        self.src = src
        threading.Thread.__init__(self)

    def uploadThis(self,path):
        print(path)
        files = os.listdir(path)
        os.chdir(path)
        for f in files:
            if os.path.isfile(path + r'\{}'.format(f)):
                fh = open(f, 'rb')
                self.ftp.storbinary('STOR %s' % f, fh)
                fh.close()
            elif os.path.isdir(path + r'\{}'.format(f)):
                self.ftp.mkd(f)
                self.ftp.cwd(f)
                self.uploadThis(path + r'\{}'.format(f))
                self.ftp.cwd('..')
        os.chdir('..')

    def run(self):
        myPath = 'C:/Users/BDI/Documents/Jorge/samples'
        print(myPath)
        print('hola')
        server = '127.0.0.1'
        username = 'cvr'
        password = '123456'
        # myPath = 'C:/Users/BDI/Documents/Jorge/samples'

        self.uploadThis(myPath )
        self.ftp.close()
        print('hola2')

class MyThread(QThread):
    """ Runs a function in a thread, and alerts the parent when done.

    Uses a custom QEvent to alert the main thread of completion.

    """
    def __init__(self, parent, func, *args, **kwargs):
        super(MyThread, self).__init__(parent)
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.start()

    def uploadThis(self,path,myFTP):
        print(path)
        files = os.listdir(path)
        os.chdir(path)
        for f in files:
            if os.path.isfile(path + r'\{}'.format(f)):
                fh = open(f, 'rb')
                myFTP.storbinary('STOR %s' % f, fh)
                fh.close()
            elif os.path.isdir(path + r'\{}'.format(f)):
                myFTP.mkd(f)
                myFTP.cwd(f)
                self.uploadThis(path + r'\{}'.format(f),myFTP)
        myFTP.cwd('..')
        os.chdir('..')

    def run(self):
        try:
            myPath = 'C:/Users/BDI/Documents/Jorge/samples'
            print(myPath)
            print('hola')
            server = '127.0.0.1'
            username = 'cvr'
            password = '123456'
            my_ftp = FTP(server, username, password)
            # myPath = 'C:/Users/BDI/Documents/Jorge/samples'

            self.uploadThis(myPath, my_ftp)
            my_ftp.close()
            print('hola2')
            #result = self.func(*self.args, **self.kwargs)
            #onClickPushButton('C:/Users/BDI/Documents/Jorge/samples')
        except Exception as e:
            print("e is %s" % e)
            result = e
        #finally:
            #CallbackEvent.post_to(self.parent(), self.on_finished, result)

class Thread(QThread):
    def run(self):
        print ("Starting thread")
        self.manager = QNetworkAccessManager();
        self.manager.finished.connect(self.finished)
        print ("Opening file")
        self.f = QFile("/home/divius/test.tbz2")
        self.f.open(QIODevice.ReadOnly)
        self.request = QNetworkRequest(QUrl(
        "ftp://ibdftp:111111@127.0.0.1/test.tbz2"))
        print ("Putting request")
        self.manager.put(self.request, self.f)
        print ("Executing")
        code = self.exec_()
        print ("Done:", code)

    def finished(self, reply):
        print ("Finished", reply.error(), reply.error() == QNetworkReply.NoError)
        self.quit()