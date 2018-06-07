#pragma once
#include "IniFile.h"
#include "string.h"

class Configuracion
{
public:
	Configuracion();
	~Configuracion();

	char* getIp();
	int getPort();
	char* getRuta();


private:
	CIniFile file;

};

