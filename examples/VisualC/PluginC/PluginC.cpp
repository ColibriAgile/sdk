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


int __stdcall Atualizar(wchar_t** resultado)
{
	resultado = NULL;
	return 1;
}

int __stdcall Notificar(wchar_t* evento, wchar_t* informacao, wchar_t** resultado)
{
	*resultado = CopiarBuffer(L"");
	return 1;
}

wchar_t* __stdcall ObterErro()
{
	return CopiarBuffer(L"");
}

wchar_t* __stdcall ObterNome()
{
	return CopiarBuffer(L"PluginC");
}

wchar_t* __stdcall ObterVersao()
{
	return CopiarBuffer(L"1.0.0.0");
}

void __stdcall Ativar(int umaMaquina)
{
}

void __stdcall AtribuirObtencaoDeFuncoes(ProcObterFuncao _ObterFuncao)
{
	ObterFuncao = _ObterFuncao;
	CallBack = (ProcCallBack) ObterFuncao(L"CallBack");
	ObterConfigs = (ProcObterConfigs) ObterFuncao(L"ObterConfigs");
	GravarConfig = (ProcGravarConfig) ObterFuncao(L"GravarConfig");
	CopiarBuffer = (ProcCopiarBuffer) ObterFuncao(L"CopiarBuffer");
	LiberarBuffer = (ProcLiberarBuffer) ObterFuncao(L"LiberarBuffer");
}

void __stdcall Configurar(wchar_t* dictMaquinas)
{
}

void __stdcall ConfigurarDB(wchar_t* umServidor, wchar_t* umBanco, wchar_t* umUsuario, wchar_t* umaSenha, wchar_t* umProvedor)
{
}

void __stdcall Desativar(int umaMaquina)
{
}

void __stdcall RegistrarAssinaturas(ProcAssinarEvento AssinarEvento)
{
  // Este evento é gerado por ítens de interface (menu, botões) adicionados via ui.config
  AssinarEvento(L"PluginC", L"EventoDeUIDePlugin.FuncaoNoPluginCPP");
}

wchar_t* __stdcall ObterMacro (wchar_t* umaMacro)
{
	return NULL;
}

wchar_t* __stdcall VerificarVersao(wchar_t* informacao)
{
	return CopiarBuffer(L"");
}
