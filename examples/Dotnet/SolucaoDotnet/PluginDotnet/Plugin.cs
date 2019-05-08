using System;
using System.Collections.Generic;
using System.Reflection;
using System.Web.Script.Serialization;

// O assembly do plugin deve ser Plugin.[NomeDoPlugin]
// O namespace aqui deve ser Plugin[NomeDoPlugin]
namespace PluginDotnet
{
  class DadosDoFabricante
  {
    public class Fabricante
    {
      public string empresa;
      public string desenvolvedor;
      public string termos_da_licenca;
      public string direitos_de_copia;
      public string marcas_registradas;
    }
    
    public class Suporte
    {
      public string email;
      public string url;
      public string telefone;
    }
    
    public Fabricante fabricante;
    public Suporte suporte;
    
    public DadosDoFabricante()
    {
      fabricante = new Fabricante();
      suporte = new Suporte();
    }
    
    public string ToJson()
    {
      JavaScriptSerializer serializer = new JavaScriptSerializer();

      return serializer.Serialize(this);
    }
  }

  public class Plugin
  {
    /******************************************
      * 
      * Funções obrigatórias
      * 
      ******************************************/
    public static string ObterNome()
    {
      return "Dotnet";
    }

    public static string ObterVersao()
    {
      return Assembly.GetExecutingAssembly().GetName().Version.ToString();
    }

    public static string ObterDadosFabricante()
    {
      DadosDoFabricante dados = new DadosDoFabricante();
      dados.fabricante.empresa = "Nome da Empresa";
      dados.fabricante.desenvolvedor = "Equipe";
      dados.fabricante.termos_da_licenca = "blablabla";
      dados.suporte.email = "suporte@email.com";
      dados.suporte.telefone = "98745-6547";
      
      return dados.ToJson();
    }

    public static string ObterDadosLicenca(string info)
    {
      return "{\"chave_extensao\": \"obter_no_marketplace\"}";
    }

    /******************************************
     * 
     * Funções opcionais
     * 
     ******************************************/
    public static void Configurar(string maquinas)
    {
      Colibri.MostrarMensagem("teste", Colibri.TipoMensagem.aviso, "Titulo", "sim", "direita");
      FormConfig testDialog = new FormConfig();
      testDialog.ShowDialog();
      testDialog.Dispose();
    }

    public static void ConfigurarDB(string servidor, string banco, string usuario, string senha, string provedor)
    {
    }

    public static void Ativar(int umaMaquina)
    {
    }

    public static void Desativar(int umaMaquina)
    {
    }
    
    public static void ObterMacro(string umaMacro)
    {
    }
    
    public static string Notificar(string sEvento, string sContexto)
    {
      // Aqui você é notificado dos eventos
      Colibri.MostrarMensagem("Teste", Colibri.TipoMensagem.aviso);
      
      return "";
    }
    
    public static void RegistrarAssinaturas()
    {
      // Aqui você assina os eventos
      Colibri.AssinarEvento("EventoDeSistema.PluginsCarregados");
    }

    public static string RegistrarPermissoes()
    {
      return "";
    }
  }
}
