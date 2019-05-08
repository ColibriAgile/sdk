// PluginC.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"
#include "PluginC.h"

ProcCallBack CallBack;
ProcObterConfigs ObterConfigs;
ProcGravarConfig GravarConfig;
ProcAlocarBuffer AlocarBuffer;
ProcLiberarBuffer LiberarBuffer;
ProcObterFuncao ObterFuncao;
ProcMostrarMensagem MostrarMensagem;
ProcMostrarTeclado MostrarTeclado;


wchar_t* __stdcall Notificar(wchar_t* evento, wchar_t* contexto)
{
	return AlocarBuffer(L"");
}

wchar_t* __stdcall ObterNome()
{
	return AlocarBuffer(L"PluginC");
}

wchar_t* __stdcall ObterDadosFabricante()
{
	wchar_t * dados = 
	   L"{\"fabricante\":{"
       L"\"empresa\":\"Nome da empresa\","
       L"\"desenvolvedor\":\"Equipe\","
       L"\"termos_da_licenca\":\"\","
       L"\"direitos_de_copia\":\"\","
       L"\"marcas_registradas\":\"X® é marca registrada da empresa Y\""
       L"}, \"suporte\":{"
       L"\"email\":\"suporte@empresa.com\","
       L"\"url\":\"\","
       L"\"telefone\":\"(99)9999-9999\""
       L"}}";
	return AlocarBuffer(dados);
}

wchar_t* __stdcall ObterDadosLicenca(wchar_t* info)
{
	return AlocarBuffer(L"{\"chave_extensao\": \"obter_no_marketplace\"}");
}


wchar_t* __stdcall ObterVersao()
{
	return AlocarBuffer(L"1.0.0.0");
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
	AlocarBuffer = (ProcAlocarBuffer) ObterFuncao(L"AlocarBuffer");
	LiberarBuffer = (ProcLiberarBuffer) ObterFuncao(L"LiberarBuffer");
	MostrarMensagem = (ProcMostrarMensagem) ObterFuncao(L"MostrarMensagem");
	MostrarTeclado = (ProcMostrarTeclado) ObterFuncao(L"MostrarTeclado");
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
	return AlocarBuffer(L"");
}

wchar_t* __stdcall VerificarVersao(wchar_t* informacao)
{
	return AlocarBuffer(L"");
}
