#include "Configuracion.h"
#include "IniFile.h"
#include "string.h"
#include <windows.h> 
#include <tchar.h>
#include <stdio.h> 


Configuracion::Configuracion()
{

}


Configuracion::~Configuracion()
{
}




int Configuracion::getPort(){

	string valor = file.GetValue("PUERTO", "programa", "configuracion.ini");
	return atoi(valor.c_str());
}



char* Configuracion::getRuta(){

	string valor = file.GetValue("RUTA", "programa", "configuracion.ini");
	char * result = new char[valor.size() + 1];
	std::copy(valor.begin(), valor.end(), result);
	result[valor.size()] = '\0';
	return result;
}

char* Configuracion::getIp(){

	string valor = file.GetValue("IPADDRESS", "programa", "configuracion.ini");
	char * result = new char[valor.size() + 1];
	std::copy(valor.begin(), valor.end(), result);
	result[valor.size()] = '\0';
	return result;
}

