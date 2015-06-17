#define PLUGINC_API extern "C"
typedef wchar_t * PChar; // Wide char

typedef void (__stdcall *ProcAssinarEvento)(PChar umPlugin, PChar umIdentificador);
typedef void * (__stdcall *ProcObterFuncao)(PChar nomeCallBack);

typedef void (__stdcall *ProcCallBack)(PChar umPlugin, PChar umTipo, PChar umValor);
typedef PChar (__stdcall *ProcObterConfigs)(PChar umPlugin, PChar umaMaquina);
typedef void (__stdcall *ProcGravarConfig)(PChar umPlugin, PChar umaConfig, int global, PChar umValor);
typedef PChar (__stdcall *ProcCopiarBuffer)(PChar Buffer);
typedef void (__stdcall *ProcLiberarBuffer)(PChar Buffer);

PLUGINC_API int __stdcall Atualizar(PChar * retorno); 
PLUGINC_API int __stdcall Notificar(PChar evento, PChar informacao, PChar * retorno);
PLUGINC_API PChar __stdcall ObterErro();
PLUGINC_API PChar __stdcall ObterNome();
PLUGINC_API PChar __stdcall ObterVersao();
PLUGINC_API void __stdcall Ativar(int umaMaquina);
PLUGINC_API void __stdcall AtribuirObtencaoDeFuncoes(ProcObterFuncao _ObterFuncao);
PLUGINC_API void __stdcall ConfigurarDB(PChar servidor, PChar nanco, PChar usuario, PChar senha, PChar provedor);
PLUGINC_API void __stdcall Configurar(PChar dictMaquinas);
PLUGINC_API void __stdcall Desativar(int umaMaquina);
PLUGINC_API void __stdcall RegistrarAssinaturas(ProcAssinarEvento proc);
PLUGINC_API PChar __stdcall ObterMacro (PChar umaMacro);
PLUGINC_API PChar __stdcall VerificarVersao(PChar informacao);
