using System;
using System.Collections.Generic;

// O assembly do plugin deve ser Plugin.[NomeDoPlugin]
// O namespace aqui deve ser Plugin[NomeDoPlugin]
namespace PluginDotnet
{
  public class Colibri
  {
    public static Dictionary<String, Object> dictFuncoes;

    public static void AssinarEvento(string evento)
    {
      ((Action<string>)dictFuncoes["AssinarEvento"])(evento);
    }
    public static void Callback(string evento, string contexto)
    {
      ((Action<string, string>)dictFuncoes["Callback"])(evento, contexto);
    }
    public static void GravarConfig(string config, int maquinaId, string valor)
    {
      ((Action<string, int, string>)dictFuncoes["GravarConfig"])(config, maquinaId, valor);
    }
    public enum TipoMensagem
    {
      aguarde,
      aviso,
      info,
      erro,
      sucesso,
      pergunta
    }
    public static int MostrarMensagem(string mensagem, TipoMensagem tipo, string titulo = "", string botaoPadrao = "nao", string alinhamento = "esquerda", string id = "")
    {
      string dados = $"{{\"mensagem\":\"{mensagem}\", \"tipo\":\"{tipo.ToString()}\", \"titulo\":\"{titulo}\", \"alinhamento\": \"{alinhamento}\", \"id\": \"{id}\"}}";
      return MostrarMensagem(dados);
    }
    public static int MostrarMensagem(string dados) 
    {
      return ((Func<string, int>)dictFuncoes["MostrarMensagem"])(dados);
    }
    public static string MostrarTeclado(string dados)
    {
      return ((Func<string, string>)dictFuncoes["MostrarTeclado"])(dados);
    }
    public static string ObterConfigs(int maquina)
    {
      return ((Func<int, string>)dictFuncoes["ObterConfigs"])(maquina);
    }
    public static int VerificarPermissao(string GUID, int elevar)
    {
      return ((Func<string, int, int>)dictFuncoes["VerificarPermissao"])(GUID, elevar);
    }
  }
}
