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


PLUGINC_API int calling Atualizar(PChar * retorno)
{
	return 1;
}

PLUGINC_API int calling Notificar(PChar evento, PChar informacao, PChar * retorno)
{
	*retorno = CopiarBuffer(L"");
	return 1;
}

PLUGINC_API PChar calling ObterErro()
{
	return CopiarBuffer(L"");
}

PLUGINC_API PChar calling ObterNome()
{
	return CopiarBuffer(L"PluginC");
}

PLUGINC_API PChar calling ObterVersao()
{
	return CopiarBuffer(L"1.0.0.0");
}

PLUGINC_API void calling Ativar(int umaMaquina)
{
}

PLUGINC_API void calling AtribuirObtencaoDeFuncoes(ProcObterFuncao _ObterFuncao)
{
	ObterFuncao = _ObterFuncao;
	CallBack = (ProcCallBack) ObterFuncao(L"CallBack");
	ObterConfigs = (ProcObterConfigs) ObterFuncao(L"ObterConfigs");
	GravarConfig = (ProcGravarConfig) ObterFuncao(L"GravarConfig");
	CopiarBuffer = (ProcCopiarBuffer) ObterFuncao(L"CopiarBuffer");
	LiberarBuffer = (ProcLiberarBuffer) ObterFuncao(L"LiberarBuffer");
}

PLUGINC_API void calling Configurar(PChar dictMaquinas)
{
}

PLUGINC_API void calling ConfigurarDB(PChar servidor, PChar nanco, PChar usuario, PChar senha, PChar provedor)
{
}

PLUGINC_API void calling Desativar(int umaMaquina)
{
}

PLUGINC_API void calling RegistrarAssinaturas(ProcAssinarEvento proc)
{
}

PLUGINC_API PChar calling ObterMacro (PChar umaMacro)
{
	return NULL;
}

PLUGINC_API PChar calling VerificarVersao(PChar informacao)
{
	return CopiarBuffer(L"");
}
