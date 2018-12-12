///////////////////////////////////////////////////////////////////////////////
//
// This example demonstrates how to use a GrabberListener derived
// callback handler object to process events
//
// A class CListener is derived from GrabberListener. It is used to handle callbacks.
// The method CListener::frameReady() simulates a time expensive processing. Therefore,
// the method CListener::frameReady() is not called for every captured buffer. 
// The member CListener::m_pBufferWritten is used to record, which buffers were processed
// by CListener::frameReady().
// After snapImages() returns, the main function will save the buffers that were not
// processed. This sample shows that all buffers have been copied correctly to the
// MembufferCollection, although CListener::frameReady() was not called for every buffer.
//

#define _WIN32_WINNT 0x0500
#define BUFFERSIZE 1000
#include<WinSock2.h>
#include <stdio.h>
#include <iostream>
#include <conio.h>
#include <tisudshl.h>



#include "CmdHelper.h"
#include "Listener.h"
#include "Configuracion.h"

using namespace _DSHOWLIB_NAMESPACE;

// Specify the number of buffers to be used.
#define NUM_BUFFERS 1
#pragma comment(lib,"ws2_32.lib")
int capturePhoto(Grabber grabber,char* ruta,CListener *pListener,smart_ptr<FrameHandlerSink> pSink );
int sendData(SOCKET s,char* message);
int reciveData(SOCKET s,char* server_repaly, int* reciv_sie);
int conectar(struct sockaddr_in server,SOCKET s,char* server_repaly, int* reciv_sie);
void generarRuta(char*ruta, char*rutaBase,char* carpeta);
int main(int argc, char* argv[])
{
	
	WSADATA wsa;
	SOCKET s;
	struct sockaddr_in server;
	char server_repaly[500],carpeta[500];
	int reciv_sie;
	Configuracion conf;
	char rutaBase[200],ruta[200];
	
	Grabber grabber;
	CListener *pListener = new CListener();
	DShowLib::InitLibrary();
	atexit( ExitLibrary );
												
	if( !setupDeviceFromFile( grabber ) )
	{
		return -1;
	}
	
	// Assign the number of buffers to the cListener object.
	pListener->setBufferSize( NUM_BUFFERS );
	// Enable the overlay bitmap to display the frame counter in the live video.
	grabber.getOverlay()->setEnable( true );
	
	// Create a FrameTypeInfoArray data structure describing the allowed color formats.
	FrameTypeInfoArray acceptedTypes = FrameTypeInfoArray::createRGBArray();
	// Create the frame handler sink
	smart_ptr<FrameHandlerSink> pSink = FrameHandlerSink::create( acceptedTypes, NUM_BUFFERS );
	// enable snap mode (formerly tFrameGrabberMode::eSNAP).
	pSink->setSnapMode( true );
	// Apply the sink to the grabber.
	grabber.setSinkType( pSink );

	strcpy(rutaBase,conf.getRuta());

	printf("\nIniciando Socket..." );
	if(WSAStartup(MAKEWORD(2,2),&wsa)!=0){
		printf("\nError code: %d",WSAGetLastError());
		return 0;
	}
	printf("\nSocket Iniciado." );

	if((s= socket(AF_INET,SOCK_STREAM,0))== INVALID_SOCKET){
		printf("\nNo se pudo crear el Socket: %d",WSAGetLastError());
		return 0;
	}
	printf("\nSocket Creado." );
	server.sin_addr.s_addr=inet_addr(conf.getIp());
	server.sin_family=AF_INET;
	server.sin_port=htons(conf.getPort());

	if(conectar(server,s,server_repaly,&reciv_sie)){
		sendData(s,"FIREWIRE_CONECTAR");
		while(1){
			reciveData(s,server_repaly,&reciv_sie);
			puts(server_repaly);//CARPETA RUTA
			strcpy(carpeta,server_repaly);
			if(strstr(server_repaly,"CARPETA")){
				printf("\nCarpeta:");//CARPETA RUTA
				sendData(s,"FIREWIRE_CARPETA_OK");//FIREWIRE_CARPETA_OK
				while (1)
				{
					
					reciveData(s,server_repaly,&reciv_sie);
					if(!strcmp(server_repaly,"SERVER_TOMAR_FOTO")){
						generarRuta(ruta,rutaBase,carpeta);
						strcpy(pListener->ruta,ruta);
						grabber.startLive();				// Start the grabber.
						pSink->snapImages( NUM_BUFFERS );	// Grab NUM_BUFFERS images.
						grabber.stopLive();					// Stop the grabber.
						// Save the buffers for which CListener::frameReady() has not been called.
						// Since CListener::frameReady() calls Sleep(250), it cannot be called for
						// every buffer. Nevertheless, all buffers are copied to the MemBufferCollection.
						//pListener->m_BufferWritten.size()
						for( size_t i = 0; i <1 ; i++ )
						{
							//if( !pListener->m_BufferWritten[i] )
							//{
								std::cout << "Buffer " << i << " processed in main()." << std::endl;
								pListener->saveImage( pSink->getMemBufferCollection()->getBuffer( i ), i);
							//}
						}

						sendData(s,"FIREWIRE_IMAGEN_OK");//FIREWIRE_IMAGEN_OK
						grabber.removeListener(pListener);
						break;
					}
				}
				
			}
			server_repaly[0]='\0';
			
		
		}
		
	}

	closesocket(s);
	WSACleanup();
	// The CListener object must be unregistered for all events
	// before it may be destroyed.
	grabber.removeListener( pListener );

	// Now, it must be checked whether the CListener object has been unregistered
	// for all events.
	while( grabber.isListenerRegistered( pListener ) )
	{
		Sleep( 0 ); // Wait and give pending callbacks a chance to complete.
	}

	// Now, the application can be sure that no callback methods of pListener
	// will be called anymore. It is now safe to delete pListener.
	delete pListener;
	

	std::cout << "Press any key to continue!" << std::endl;
	std::cin.get();
	return 0;
}

int capturePhoto(Grabber grabber,char* ruta,CListener *pListener,smart_ptr<FrameHandlerSink> pSink ){
	

	
	

	return 0;
}

int sendData(SOCKET s,char* message){
	
	if(send(s,message,strlen(message),0)<0){
		puts("error en el envio.");
		return 0;
	}

	return 1;

}

int reciveData(SOCKET s,char* server_repaly, int* reciv_sie){
	int sie;
	// recivo la respuesta del servidor
	if((*reciv_sie=recv(s,server_repaly,BUFFERSIZE,0))==SOCKET_ERROR){
		puts("error al recivir respuesta");                                           	
	}
	sie=*reciv_sie;
	server_repaly[sie]='\0'; 
	return 1;
}

int conectar(struct sockaddr_in server,SOCKET s,char* server_repaly, int* reciv_sie){
	if(connect(s,(struct sockaddr *)&server,sizeof(server))<0){
		printf("\nError en conexion." );
		return 0;
	}
	return 1;
}

void generarRuta(char*ruta, char*rutaBase,char* carpeta){
	int cont=0;
	strcpy(ruta,rutaBase);
	while(*(ruta+cont)!='\0'){
		cont++;
	}
	*(ruta+cont)='\\';
	strcpy((ruta+(++cont)),(carpeta+8));
	printf("RUTA GENERADA: %s\n",ruta);
	
}