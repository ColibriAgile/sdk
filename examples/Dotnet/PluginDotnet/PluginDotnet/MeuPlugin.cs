using System;
using System.Collections.Generic;


namespace PluginDotnet
{
    public class MeuPlugin
    {
        public static string ObterNome()
        {
            return "Dotnet";
        }

        public static string ObterVersao()
        {
            return "1.0.0.0";
        }

        public static string ObterDadosFabricante()
        {
            return "{\"fabricante\": { \"empresa\": \"Empresa\", \"desenvolvedor\": \"Equipe\", \"termos_da_licenca\": \"\", \"direitos_de_copia\": \"\", \"marcas_registradas\": \"\"}, \"suporte\": { \"email\": \"suporte@empresa.com\", \"url\": \"\", \"telefone\": \"(99)9999-9999\"}}";
        }
        public static void Configurar(string maquinas)
        {
            FormConfig testDialog = new FormConfig();
            testDialog.ShowDialog();
            testDialog.Dispose();

            Colibri.MostrarMensagem("{\"mensagem\":\"teste\", \"tipo\":\"aviso\"}");
            Colibri.GravarConfig("Teste", 1, "merda");
            Colibri.ObterConfigs(1);


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
            return "";
        }

        public static void RegistrarAssinaturas()
        {
            Colibri.AssinarEvento("Evento.Nome");
        }

        public static string RegistrarPermissoes()
        {
            return "";
        }
    }
}
