// PluginC.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"
#include "PluginC.h"

ProcCallBack CallBack;
ProcObterConfigs ObterConfigs;
ProcGravarConfig GravarConfig;
ProcCopiarBuffer CopiarBuffer;
ProcLiberarBuffer LiberarBuffer;
ProcObterFuncao ObterFuncao;


PLUGINC_API int __stdcall Atualizar(PChar * retorno)
{
	return 1;
}

PLUGINC_API int __stdcall Notificar(PChar evento, PChar informacao, PChar * retorno)
{
	*retorno = CopiarBuffer(L"");
	return 1;
}

PLUGINC_API PChar __stdcall ObterErro()
{
	return CopiarBuffer(L"");
}

PLUGINC_API PChar __stdcall ObterNome()
{
	return CopiarBuffer(L"PluginC");
}

PLUGINC_API PChar __stdcall ObterVersao()
{
	return CopiarBuffer(L"1.0.0.0");
}

PLUGINC_API void __stdcall Ativar(int umaMaquina)
{
}

PLUGINC_API void __stdcall AtribuirObtencaoDeFuncoes(ProcObterFuncao _ObterFuncao)
{
	ObterFuncao = _ObterFuncao;
	CallBack = (ProcCallBack) ObterFuncao(L"CallBack");
	ObterConfigs = (ProcObterConfigs) ObterFuncao(L"ObterConfigs");
	GravarConfig = (ProcGravarConfig) ObterFuncao(L"GravarConfig");
	CopiarBuffer = (ProcCopiarBuffer) ObterFuncao(L"CopiarBuffer");
	LiberarBuffer = (ProcLiberarBuffer) ObterFuncao(L"LiberarBuffer");
}

PLUGINC_API void __stdcall Configurar(PChar dictMaquinas)
{
}

PLUGINC_API void __stdcall ConfigurarDB(PChar servidor, PChar nanco, PChar usuario, PChar senha, PChar provedor)
{
}

PLUGINC_API void __stdcall Desativar(int umaMaquina)
{
}

PLUGINC_API void __stdcall RegistrarAssinaturas(ProcAssinarEvento proc)
{
}

PLUGINC_API PChar __stdcall ObterMacro (PChar umaMacro)
{
	return NULL;
}

PLUGINC_API PChar __stdcall VerificarVersao(PChar informacao)
{
	return CopiarBuffer(L"");
}
