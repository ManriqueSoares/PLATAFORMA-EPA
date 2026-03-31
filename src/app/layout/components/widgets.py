import flet as ft
from app.utils.export import Button_SidBar, DATATABLE_STATUS_ATIVIDADE

def on_hover_close_filter_data_button(e):
    if e.data == "true":
        BOTAO_CLOSE_JANELA_SELECAO_DATA_.bgcolor = ft.Colors.RED_200
        BOTAO_CLOSE_JANELA_SELECAO_DATA_.update()
    else:
        BOTAO_CLOSE_JANELA_SELECAO_DATA_.bgcolor = ft.Colors.RED_500
        BOTAO_CLOSE_JANELA_SELECAO_DATA_.update()

def on_hover_close_notas_button(e):
    if e.data == "true":
        BOTAO_CLOSE_JANELA_NOTAS.bgcolor = ft.Colors.RED_200
        BOTAO_CLOSE_JANELA_NOTAS.update()
    else:
        BOTAO_CLOSE_JANELA_NOTAS.bgcolor = ft.Colors.RED_500
        BOTAO_CLOSE_JANELA_NOTAS.update()


LOGO_AZUL = ft.Image(src="logo_azul.png", width=60, height=60)
DATATABLE_GERAL = ft.DataTable(
    expand=True,
    border=ft.border.all(1, ft.Colors.with_opacity(0.80, ft.Colors.BLUE_900)),
    border_radius=15,
    columns=[
        ft.DataColumn(ft.Text("CP", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_300)),
        ft.DataColumn(ft.Text("CLIENTE", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_300)),
        ft.DataColumn(ft.Text("CÁLCULO", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_300)),
        ft.DataColumn(ft.Text("RESP.", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_300)),
        ft.DataColumn(ft.Text("EBPA", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_300)),
        ft.DataColumn(ft.Text("RESP.", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_300)),
        ft.DataColumn(ft.Text("EBPM", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_300)),
        ft.DataColumn(ft.Text("RESP.", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_300)),
        ft.DataColumn(ft.Text("APROV.", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_300)),
        ft.DataColumn(ft.Text("RESP.", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_300)),
        ft.DataColumn(ft.Text("DATA FINAL", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_300)),
        ft.DataColumn(ft.Text("", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_300))
    ]
)
BOTAO_NOTIFICACAO = ft.IconButton(icon=ft.Icons.NOTIFICATIONS, icon_color=ft.Colors.BLUE_300)

SIGLA_USER = ft.Text(value="MS", size=20, color=ft.Colors.BLUE_900, weight=ft.FontWeight.W_600)
CONTAINER_SIGLA_USER = ft.Container(width=42, height=42, border_radius=10, alignment=ft.alignment.center, bgcolor=ft.Colors.with_opacity(0.90, ft.Colors.WHITE30), content=SIGLA_USER)
TEXT_AREA = ft.Text(value="Estudo PA", size=9, weight=ft.FontWeight.W_400, color=ft.Colors.with_opacity(0.90, ft.Colors.BLUE_300), animate_opacity=500)

BOTAO_OPEN_SIDBAR = ft.FloatingActionButton(icon=ft.Icons.MENU, scale=0.6, animate_scale=ft.Animation(500, ft.AnimationCurve.DECELERATE),
)
NOME_USUARIO = ft.Text(value="Manrique Soares", size=11, weight=ft.FontWeight.W_500, color=ft.Colors.with_opacity(0.95, ft.Colors.BLUE_200), animate_opacity=500)

BOTAO_GERAL = Button_SidBar(icone=ft.Icons.HOME, texto="Home")
BOTAO_ATIVIDADES = Button_SidBar(icone=ft.Icons.CALCULATE, texto="Atividades")
BOTAO_INFORMACOES = Button_SidBar(icone=ft.Icons.INFO, texto="Informações")
BOTAO_NOTAS = Button_SidBar(icone=ft.Icons.NOTE, texto="Notas")

NOME_CONTAINER = ft.Text(value="Geral", size=22, weight=ft.FontWeight.W_700, color=ft.Colors.BLUE_800)

ENTRADA_CP_FILTRO_GERAL = ft.TextField(label="CP", width=150, border_radius=15, border_color=ft.Colors.with_opacity(0.80, ft.Colors.BLUE_900), focus_color=ft.Colors.with_opacity(0.80, ft.Colors.BLUE_700))
ENTRADA_CLIENTE_FILTRO_GERAL = ft.Dropdown(label="Cliente", width=200, border_radius=15, border_color=ft.Colors.with_opacity(0.80, ft.Colors.BLUE_900), input_filter=True, enable_filter=True, editable=True,  options=[])

BOTAO_FILTRAR_DATA = ft.FloatingActionButton(icon=ft.Icons.DATE_RANGE, scale=0.8)

BOTAO_LIMPAR_FILTROS = ft.IconButton(icon=ft.Icons.DELETE_FOREVER, icon_color=ft.Colors.RED_400)

RESPONSAVEL_FILTRO_OPCOES = [
    "MANRIQUE SOARES F",
    "GUSTAVO PALERMO D",
]

ENTRADA_RESPONSAVEL_FILTRO_GERAL = ft.Dropdown(label="Resp", width=220, border_radius=15, border_color=ft.Colors.with_opacity(0.80, ft.Colors.BLUE_900), input_filter=True, enable_filter=True, options=[
    ft.dropdown.Option(responsavel) for responsavel in RESPONSAVEL_FILTRO_OPCOES
])


DATATABLE_ATIVIDADES_EM_ABERTO = DATATABLE_STATUS_ATIVIDADE(status="aberto")
DATATABLE_ATIVIDADES_EM_ANDAMENTO = DATATABLE_STATUS_ATIVIDADE(status="andamento")
DATATABLE_ATIVIDADES_FINALIZADAS = DATATABLE_STATUS_ATIVIDADE(status="finalizada")

TITULO_JANELA_SELECAO_DATA = ft.Text(value="Seleção de Data", size=16, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_700)

#BOTAO_CLOSE_JANELA_SELECAO_DATA = ft.IconButton(icon=ft.Icons.CLOSE, scale=0.8, icon_color=ft.Colors.BLUE_300)
BOTAO_CLOSE_JANELA_SELECAO_DATA_ = ft.Container(width=40, height=28, border_radius=ft.border_radius.only(bottom_left=5), alignment=ft.alignment.center_right, bgcolor=ft.Colors.RED_500, content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Column(alignment=ft.MainAxisAlignment.CENTER,controls=[ft.Icon(ft.Icons.CLOSE, size=11, color=ft.Colors.WHITE)])]), on_click=None, on_hover=on_hover_close_filter_data_button)

ENTRADA_DATA_INICIO_FILTRO = ft.TextField(label="Data Início", width=120, height=30, border_radius=15, border_color=ft.Colors.with_opacity(0.80, ft.Colors.BLUE_900), focus_color=ft.Colors.with_opacity(0.80, ft.Colors.BLUE_700), label_style=ft.TextStyle(size=11), text_style=ft.TextStyle(size=11), content_padding=ft.padding.only(bottom=5, left=10))
ENTRADA_DATA_FIM_FILTRO = ft.TextField(label="Data Fim", width=120, height=30, border_radius=15, border_color=ft.Colors.with_opacity(0.80, ft.Colors.BLUE_900), focus_color=ft.Colors.with_opacity(0.80, ft.Colors.BLUE_700), label_style=ft.TextStyle(size=11), text_style=ft.TextStyle(size=11), content_padding=ft.padding.only(bottom=5, left=10))

BOTAO_SELECAO_DATA_INICIO_FILTRO = ft.FloatingActionButton(icon=ft.Icons.DATE_RANGE, scale=0.6)
BOTAO_SELECAO_DATA_FIM_FILTRO = ft.FloatingActionButton(icon=ft.Icons.DATE_RANGE, scale=0.6)

#BOTAO_FILTRAR_DATA_CONFIRMAR = ft.ElevatedButton(text="Filtrar", width=100, icon=ft.Icons.CHECK, height=30, bgcolor=ft.Colors.BLUE_700, on_click=None)
BOTAO_FILTRAR_DATA_CONFIRMAR_ = ft.FloatingActionButton(icon=ft.Icons.CHECK, scale=0.5, bgcolor=ft.Colors.GREEN_500, on_click=None)

TITULO_JANELA_NOTAS = ft.Text(value="Notas", size=16, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_700)
BOTAO_CLOSE_JANELA_NOTAS = ft.Container(width=38, height=28, border_radius=ft.border_radius.only(bottom_left=5), alignment=ft.alignment.center_right, bgcolor=ft.Colors.RED_500, content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Column(alignment=ft.MainAxisAlignment.CENTER,controls=[ft.Icon(ft.Icons.CLOSE, size=11, color=ft.Colors.WHITE)])]), on_click=None, on_hover=on_hover_close_notas_button)
BOTAO_ENVIAR_EMAIL_NOTAS = ft.IconButton(icon=ft.Icons.EMAIL, icon_color=ft.Colors.BLUE_300)
BOTAO_ADICIONAR_NOTA = ft.ElevatedButton(text="Adicionar Nota", width=120, height=30, on_click=None)
TAB_NOTAS = ft.Tabs(selected_index=0, animation_duration=300,tabs=[]) 
