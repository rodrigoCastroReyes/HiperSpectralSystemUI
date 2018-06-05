from ftplib import FTP
import os
from rx import Observable
from rx.concurrency import ThreadPoolScheduler
from rx.concurrency import NewThreadScheduler
from threading import current_thread
import multiprocessing, time, random
from PyQt5 import QtCore
from rx.concurrency import QtScheduler

class FtpClient(object):

    def __init__(self):
        print("in init")

    def intense_calculation(self,value):
        # sleep for a random short duration between 0.5 to 2.0 seconds to simulate a long-running calculation
        time.sleep(random.randint(5,20) * .1)
        print(value)
        self.onClickPushButton(value)
        return value

    def rx_ython(self):
        # calculate number of CPU's and add 1, then create a ThreadPoolScheduler with that number of threads
        optimal_thread_count = multiprocessing.cpu_count() + 1
        #pool_scheduler = ThreadPoolScheduler(optimal_thread_count)
        pool_scheduler = NewThreadScheduler()
        #pool_scheduler = QtScheduler(QtCore)
        # Create Process 1

        Observable.from_(["C:/Users/BDI/Documents/Jorge/samples"]) \
            .observe_on(pool_scheduler) \
            .subscribe_on(pool_scheduler) \
            .map(lambda s: self.intense_calculation(s)) \
            .subscribe(on_next=lambda i: print("PROCESS 1: {0} {1}".format(current_thread().name, i)),
                       on_error=lambda e: print(e),
                       on_completed=lambda: print("PROCESS 1 done!"))
        '''
        Observable.from_(["C:/Users/BDI/Documents/Jorge/samples"]) \
            .flat_map(lambda s: Observable.just(s, pool_scheduler).map(lambda s: intense_calculation(s))) \
            .subscribe(on_next=lambda i: print("PROCESS 1: {0} {1}".format(current_thread().name, i)),
                       on_error=lambda e: print(e),
                       on_completed=lambda: print("PROCESS 1 done!"))'''

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

    def onClickPushButton(self,myPath):
        print(myPath)
        print('hola')
        server = '127.0.0.1'
        username = 'cvr'
        password = '123456'
        my_ftp = FTP(server, username, password)
        #myPath = 'C:/Users/BDI/Documents/Jorge/samples'

        self.uploadThis(myPath,my_ftp)
        my_ftp.close()
        print('hola2')