#define PLUGINC_API extern "C" // __declspec(dllexport)
#define calling __stdcall
typedef wchar_t * PChar; // Wide char

typedef void (calling *ProcAssinarEvento)(PChar umPlugin, PChar umIdentificador);
typedef void * (calling *ProcObterFuncao)(PChar nomeCallBack);

typedef void (calling *ProcCallBack)(PChar umPlugin, PChar umTipo, PChar umValor);
typedef PChar (calling *ProcObterConfigs)(PChar umPlugin, PChar umaMaquina);
typedef void (calling *ProcGravarConfig)(PChar umPlugin, PChar umaConfig, int global, PChar umValor);
typedef PChar (calling *ProcCopiarBuffer)(PChar Buffer);
typedef void (calling *ProcLiberarBuffer)(PChar Buffer);

PLUGINC_API int calling Atualizar(PChar * retorno); 
PLUGINC_API int calling Notificar(PChar evento, PChar informacao, PChar * retorno);
PLUGINC_API PChar calling ObterErro();
PLUGINC_API PChar calling ObterNome();
PLUGINC_API PChar calling ObterVersao();
PLUGINC_API void calling Ativar(int umaMaquina);
PLUGINC_API void calling AtribuirObtencaoDeFuncoes(ProcObterFuncao _ObterFuncao);
PLUGINC_API void calling Configurar(PChar dictMaquinas);
PLUGINC_API void calling Desativar(int umaMaquina);
PLUGINC_API void calling RegistrarAssinaturas(ProcAssinarEvento proc);
PLUGINC_API PChar calling VerificarVersao(PChar informacao);
