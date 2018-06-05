import asyncio
import aioftp
import os

from aioftpclient import aioftp

'''
async def get_mp3(host, port, login, password):
    async with aioftp.ClientSession(host, port, login, password) as client:
        for path, info in (await client.list(recursive=True)):
            print(path)
            await client.download(path)
            #if info["type"] == "file" and path.suffix == ".mp3":
            #    await client.download(path)


loop = asyncio.get_event_loop()
tasks = (get_mp3("127.0.0.1", 21, "cvr", "123456"),)
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
'''

def prueba2():
    path = 'C:/Users/BDI/Documents/Jorge/samples/vc10'
    client = aioftp.Client()
    client.connect("127.0.0.1")
    client.login("cvr", "123456")
    print(path)
    files = os.listdir(path)
    os.chdir(path)
    for f in files:
        print(r'\{}'.format(f))
        print(os.path.split(os.path.split(r'\{}'.format(f))[0])[1])
        client.upload(os.path.split(os.path.split(r'\{}'.format(f))[0])[1], "/", write_into=True)


def prueba():
    path = 'C:/Users/BDI/Documents/Jorge/samples/vc10'
    client = aioftp.ClientSession('127.0.0.1', 21, "cvr", "123456")
    print(path)
    files = os.listdir(path)
    os.chdir(path)
    for f in files:
        print(r'\{}'.format(f))
        print(os.path.split(os.path.split(r'\{}'.format(f))[0])[1])
        client.upload(os.path.split(os.path.split(r'\{}'.format(f))[0])[1], "/", write_into=True)

async def subir_datos():
    path='C:/Users/BDI/Documents/Jorge/samples/vc10'
    async with aioftp.ClientSession('127.0.0.1', 21, "cvr", "123456") as client:
        print(path)
        files = os.listdir(path)
        os.chdir(path)
        for f in  files:
            print(r'\{}'.format(f))
            print(os.path.split(os.path.split(r'\{}'.format(f))[0])[1])
            await client.upload(os.path.split(os.path.split(r'\{}'.format(f))[0])[1],"/", write_into=True)
    '''print("hola")
    try:
        await client.quit()
    except ConnectionResetError:
        print("hola2")
        '''

def casa():
    loop = asyncio.get_event_loop()
    tasks = (subir_datos(),)

    #ftp = Aioftp()
    loop.run_until_complete(asyncio.wait(tasks))
    s = input()
    print("You typed", s)
    loop.close()
