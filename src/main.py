import flet as ft

from app.layout.raiz import raiz
from app.layout.pages.home_page import HOME, JANELA_NOTAS
from app.services.loading_datatable import (
    run_datatable_primeiro_envio, 
    run_datatable_atividades_em_aberto
)
def main(page: ft.Page):

    home = HOME(page)
    raiz.controls.append(
        home
    )

    page.title = "Estudos Parte Ativa"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window.width = 1100
    page.window.height = 700
    page.add(
        ft.Container(
            expand=True,
            content=raiz
        )
    )
    run_datatable_primeiro_envio()
    run_datatable_atividades_em_aberto()

    page.update()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
