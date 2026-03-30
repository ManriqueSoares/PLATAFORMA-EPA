import flet as ft
from datetime import datetime

today = datetime.today()

from app.layout.raiz import raiz
from app.config.status import app_status
from app.layout.components.widgets import *

class HOME(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.padding = 0
        self.expand = True
        

        
        
        # ----------------------------------------- Função botões -----------------------------------------------
        BOTAO_OPEN_SIDBAR.on_click = self.open_sidbar
        BOTAO_ATIVIDADES.icon_button.on_click = lambda e: self.altera_janela(e, nome_page="Atividades", interface=self.container_atividades())
        BOTAO_GERAL.icon_button.on_click = lambda e: self.altera_janela(e, nome_page="Home", interface=self.container_geral())
        BOTAO_FILTRAR_DATA.on_click = self.open_janela_selecao_data
        BOTAO_SELECAO_DATA_INICIO_FILTRO.on_click = lambda e: self.page.open(ft.DatePicker(first_date=datetime(2026, 1, 1), last_date=datetime(2099, 12, 31), date_picker_entry_mode=ft.DatePickerEntryMode.CALENDAR, on_change=self.filtrar_data_inicio))
        BOTAO_SELECAO_DATA_FIM_FILTRO.on_click = lambda e: self.page.open(ft.DatePicker(first_date=datetime(2026, 1, 1), last_date=datetime(2099, 12, 31), date_picker_entry_mode=ft.DatePickerEntryMode.CALENDAR, on_change=self.filtrar_data_fim))
        #------------------------------------------ Containers para cada página --------------------------------

        # ----------------------------------------- Definindo interface -----------------------------------------
        self.sidbar = self.sidbar()
        self.center = self.container_center()

        # ----------------------------------------- Conteúdo principal -----------------------------------------
        self.content = self.build()


    def sidbar(self):
        return ft.Container(
            width=170,
            height=True,
            border_radius=ft.border_radius.only(top_right=20, bottom_right=20),
            animate=ft.Animation(500, ft.AnimationCurve.DECELERATE),
            padding=ft.padding.only(left=10, right=10, top=20),
            bgcolor=ft.Colors.with_opacity(0.70, ft.Colors.BLUE_900),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=True,
                        padding=ft.padding.only(left=10),
                        height=100,
                        alignment=ft.alignment.center,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                CONTAINER_SIGLA_USER,
                                ft.Column(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.START,
                                    controls=[
                                        NOME_USUARIO,
                                        TEXT_AREA
                                    ]
                                )
                            ]
                        )
                    ),
                    ft.Container(
                        width=True,
                        height=50,
                        alignment=ft.alignment.center,
                        content=BOTAO_OPEN_SIDBAR
                    ),
                    ft.Container(
                        expand=True,
                        padding=ft.padding.only(left=10, right=10),
                        alignment=ft.alignment.top_center,
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                BOTAO_GERAL,
                                BOTAO_ATIVIDADES,
                                BOTAO_INFORMACOES,
                                BOTAO_NOTAS
                            ]
                        )
                    ),
                    ft.Container(
                        width=True,
                        height=100,
                        content=None
                    )
                ]
            )
        )

    def container_center(self):
        return ft.Container(
            expand=True,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=True,
                        height=80,
                        padding=ft.padding.only(left=20, right=20),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                LOGO_AZUL,
                                BOTAO_NOTIFICACAO
                            ]
                        )
                    ),
                    ft.Container(
                        expand=True,
                        content=self.container_geral()
                    )
                ]
            )
        )

    # ----------------------------------------- Container Geral -----------------------------------------
    def container_geral(self):
        return ft.Container(
            expand=True,
            padding=10,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ## Nome Container
                    ft.Container(
                        width=True,
                        height=50,
                        padding=ft.padding.only(left=20, right=20),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[NOME_CONTAINER]
                        )
                    ),
                    ft.Container(
                        width=True,
                        height=50,
                        padding=ft.padding.only(left=30),
                        content = ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ENTRADA_CP_FILTRO_GERAL,
                                ft.VerticalDivider(width=10, color=ft.Colors.TRANSPARENT),
                                ENTRADA_CLIENTE_FILTRO_GERAL,
                                ft.VerticalDivider(width=10, color=ft.Colors.TRANSPARENT),
                                ENTRADA_RESPONSAVEL_FILTRO_GERAL,
                                ft.VerticalDivider(width=10, color=ft.Colors.TRANSPARENT),
                                BOTAO_FILTRAR_DATA,
                                ft.VerticalDivider(width=10, color=ft.Colors.TRANSPARENT),
                                BOTAO_LIMPAR_FILTROS,
                            ]
                        )
                    ),
                    ft.Divider(height=10, color="transparent"),
                    ft.Container(
                        expand=True,
                        padding=10,
                        content=ft.Column(
                            scroll="auto",
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
                            controls=[
                                ft.Row(
                                    scroll="auto",
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        DATATABLE_GERAL
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )

    # ----------------------------------------- Container Atividades -----------------------------------------
    def container_atividades(self):
        return ft.Container(
            expand=True,
            padding=10,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=True,
                        height=50,
                        padding=ft.padding.only(left=20, right=20),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[NOME_CONTAINER]
                        )
                    ),
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Tabs(
                                    scrollable=True,
                                    selected_index=0,
                                    animation_duration=800,
                                    divider_color="transparent",
                                    splash_border_radius=20,
                                    tabs=[
                                        ft.Tab(
                                            text="Em Aberto",
                                            content=ft.Column(
                                                scroll="auto",
                                                alignment=ft.MainAxisAlignment.START,
                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                controls=[
                                                    ft.Row(
                                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                        controls=[
                                                            DATATABLE_ATIVIDADES_EM_ABERTO
                                                        ]
                                                    )
                                                ]
                                            )
                                        ),
                                        ft.Tab(
                                            text="Em Andamento",
                                            content=ft.Column(
                                                scroll="auto",
                                                alignment=ft.MainAxisAlignment.START,
                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                controls=[
                                                    ft.Row(
                                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                        controls=[
                                                            DATATABLE_ATIVIDADES_EM_ANDAMENTO
                                                        ]
                                                    )
                                                ]
                                            )
                                        ),
                                        ft.Tab(
                                            text="Concluídas",
                                            content=ft.Column(
                                                scroll="auto",
                                                alignment=ft.MainAxisAlignment.START,
                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                controls=[
                                                    ft.Row(
                                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                        controls=[
                                                            DATATABLE_ATIVIDADES_FINALIZADAS
                                                        ]
                                                    )
                                                ]
                                                
                                            )
                                        )
                                    ]
                                ),
                                ft.Container(
                                    width=True,
                                    height=10,
                                    content=None
                                )
                            ]
                        )
                    )
                ]
            )
        )

    # ----------------------------------------- Função para abrir Sidbar -----------------------------------------
    def open_sidbar(self, e):
        if self.sidbar.width == 170:
            self.sidbar.width = 80
            self.sidbar.border_radius = ft.border_radius.only(top_right=5, bottom_right=5)
            NOME_USUARIO.visible = False
            TEXT_AREA.visible = False
            BOTAO_OPEN_SIDBAR.scale = 0.6
            BOTAO_GERAL.texto_button.visible = False
            BOTAO_ATIVIDADES.texto_button.visible = False
            BOTAO_INFORMACOES.texto_button.visible = False
            BOTAO_NOTAS.texto_button.visible = False
        else:
            self.sidbar.width = 170
            self.sidbar.border_radius = ft.border_radius.only(top_right=15, bottom_right=15)
            NOME_USUARIO.visible = True
            TEXT_AREA.visible = True
            BOTAO_OPEN_SIDBAR.scale = 0.8
            BOTAO_GERAL.texto_button.visible = True
            BOTAO_ATIVIDADES.texto_button.visible = True
            BOTAO_INFORMACOES.texto_button.visible = True
            BOTAO_NOTAS.texto_button.visible = True
            
        
        self.sidbar.update()

    def altera_janela(self, e, nome_page, interface):
        match nome_page:
            case "Home":
                NOME_CONTAINER.value = "Geral"
            case "Atividades":
                NOME_CONTAINER.value = "Atividades"
            case "Informações":
                NOME_CONTAINER.value = "Informações"
            case "Notas":
                NOME_CONTAINER.value = "Notas"        
        NOME_CONTAINER.value = nome_page
        self.center.content.controls[1].content = interface
        self.page.update()


    def open_janela_selecao_data(self, e):
        if app_status.janela_selecao_data == False:
            self.janela_selecao_data = JANELA_SELECAO_DATA(page=self.page)
            raiz.controls.append(
                ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                self.janela_selecao_data
                            ]
                        )
                    ]
                )
            )
            app_status.janela_selecao_data = True
            self.page.update()
        else:
            pass


    def filtrar_data_inicio(self, e):
        ENTRADA_DATA_INICIO_FILTRO.value = e.control.value.strftime("%d/%m/%Y")
        self.page.update()
    
    def filtrar_data_fim(self, e):
        ENTRADA_DATA_FIM_FILTRO.value = e.control.value.strftime("%d/%m/%Y")
        self.page.update()

    def build(self):
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ## Sidbar
                self.sidbar,
                ## Container Principal
                self.center
            ]
        )
    


class JANELA_SELECAO_DATA(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.width = 400
        self.height = 200,
        self.border_radius = 15
        self.bgcolor = ft.Colors.with_opacity(0.60, ft.Colors.GREY_900)
        self.blur = 5

        BOTAO_CLOSE_JANELA_SELECAO_DATA_.on_click = lambda e: self.close_janela_selecao_data(e)
        
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=True,
                    padding=0,
                    height=40,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            ft.Container(padding=ft.padding.only(left=10,top=3), content=TITULO_JANELA_SELECAO_DATA),
                            BOTAO_CLOSE_JANELA_SELECAO_DATA_
                        ]
                    )
                ),
                ft.Container(
                    expand=True,
                    padding=ft.padding.only(left=20, right=20),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Row(
                                controls=[
                                    ENTRADA_DATA_INICIO_FILTRO,
                                    BOTAO_SELECAO_DATA_INICIO_FILTRO
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ENTRADA_DATA_FIM_FILTRO,
                                    BOTAO_SELECAO_DATA_FIM_FILTRO
                                ]
                            )
                        ]
                    )
                ),
                ft.Container(
                    width=True,
                    height=40,
                    padding=ft.padding.only(right=5, bottom=5),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                        controls=[
                            BOTAO_FILTRAR_DATA_CONFIRMAR_
                        ]
                    )
                )
            ]
        )
    
    def close_janela_selecao_data(self, e):
        raiz.controls.pop()
        app_status.janela_selecao_data = False
        self.page.update()
        