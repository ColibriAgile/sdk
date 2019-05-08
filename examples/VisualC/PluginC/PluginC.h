#pragma once

typedef void (__stdcall *ProcAssinarEvento)(wchar_t* umPlugin, wchar_t* umEvento);
typedef void (__stdcall *ProcCallBack)(wchar_t* umPlugin, wchar_t* umEvento, wchar_t* umContexto);
typedef wchar_t* (__stdcall *ProcObterConfigs)(wchar_t* umPlugin, int umaMaquina);
typedef void (__stdcall *ProcGravarConfig)(wchar_t* umPlugin, wchar_t* umaConfig, int umaMaquina, wchar_t* umValor);
typedef wchar_t* (__stdcall *ProcAlocarBuffer)(wchar_t* Buffer);
typedef void (__stdcall *ProcLiberarBuffer)(wchar_t* Buffer);
typedef void * (__stdcall *ProcObterFuncao)(wchar_t* nomeFuncao);
typedef int (__stdcall *ProcMostrarMensagem)(wchar_t* plugin, wchar_t* dados);
typedef wchar_t* (__stdcall *ProcMostrarTeclado)(wchar_t* plugin, wchar_t* dados);

#ifdef __cplusplus
extern "C" {
#endif
void __stdcall Ativar(int umaMaquina);
void __stdcall AtribuirObtencaoDeFuncoes(ProcObterFuncao _ObterFuncao);
void __stdcall Configurar(wchar_t* dictMaquinas);
void __stdcall ConfigurarDB(wchar_t* umServidor, wchar_t* umBanco, wchar_t* umUsuario, wchar_t* umaSenha, wchar_t* umProvedor);
void __stdcall Desativar(int umaMaquina);
wchar_t* __stdcall Notificar(wchar_t* evento, wchar_t* contexto);
wchar_t* __stdcall ObterErro();
wchar_t* __stdcall ObterMacro (wchar_t* umaMacro);
wchar_t* __stdcall ObterNome();
wchar_t* __stdcall ObterDadosFabricante();
wchar_t* __stdcall ObterDadosLicenca(wchar_t* info);
wchar_t* __stdcall ObterVersao();
void __stdcall RegistrarAssinaturas(ProcAssinarEvento AssinarEvento);
wchar_t* __stdcall VerificarVersao(wchar_t* informacao);
#ifdef __cplusplus
} // extern "C"
#endif
