using System;
using System.Collections.Generic;

// O assembly do plugin deve ser Plugin.[NomeDoPlugin]
// O namespace aqui deve ser Plugin[NomeDoPlugin]
namespace PluginDotnet
{
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
            return "1.0.0.0";
        }

        public static string ObterDadosFabricante()
        {
            return "{\"fabricante\": { \"empresa\": \"Empresa\", \"desenvolvedor\": \"Equipe\", \"termos_da_licenca\": \"\", \"direitos_de_copia\": \"\", \"marcas_registradas\": \"\"}, \"suporte\": { \"email\": \"suporte@empresa.com\", \"url\": \"\", \"telefone\": \"(99)9999-9999\"}}";
        }

        /******************************************
         * 
         * Funções opcionais
         * 
         ******************************************/
        public static void Configurar(string maquinas)
        {
            FormConfig testDialog = new FormConfig();
            testDialog.ShowDialog();
            testDialog.Dispose();
            // Colibri.MostrarMensagem("{\"mensagem\":\"teste\", \"tipo\":\"aviso\"}");
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
            return "";
        }

        public static void RegistrarAssinaturas()
        {
            // Aqui você assina os eventos
            // Colibri.AssinarEvento("Evento.Nome");
        }

        public static string RegistrarPermissoes()
        {
            return "";
        }
    }
}
