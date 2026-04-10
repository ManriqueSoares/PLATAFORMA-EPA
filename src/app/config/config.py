from datetime import datetime
import os

class CONFIGURACOES:
    def __init__(self):
        self.user = "Manrique Soares F"
        self.caminho_banco_dados =  r"Q:\GROUPS\WTD_GCV_TECNICO\WTD_GCV_PROJETOS\15_HORAS_PS\PROGRAMAÇÃO PROJETOS\backup"
        # self.caminho_banco_dados_programacao = self.caminho_banco_programacao_att(self.caminho_banco_dados)
        self.caminho_banco_dados_programacao = r"Q:\GROUPS\WTD_GCV_TECNICO\WTD_GCV_PROJETOS\15_HORAS_PS\PROGRAMAÇÃO PROJETOS\backup\09_04_2026_PROGRAMAÇÃO EB PM_PA_VBA.xlsm"
        self.caminho_banco_relatorio_ps_weg = r"\\Brjgs100\DFSWEG\APPS\SAP\EP0\ENG_WTD\Relatorio_PS_Eng\Relatórios\Current week"

    def caminho_banco_programacao_att(self, caminho):
        pass
        # try:
        #     data_hoje = datetime.now().strftime("%d_%m_%Y")
        #     nome_arquivo = f"{data_hoje}_PROGRAMAÇÃO EB PM_PA_VBA.xlsm"
        #     caminho_completo = os.path.join(caminho, nome_arquivo)
        #     print(f"Verificando caminho: {caminho_completo}")
        #     return caminho_completo if os.path.exists(caminho) else None
        # except Exception as e:
        #     print(f"Erro ao acessar caminho: {e}")
        #     return None
    
configuracoes = CONFIGURACOES()