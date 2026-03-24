import flet as ft

class Button_SidBar(ft.Container):
    def __init__(self, icone, texto):
        super().__init__()
        self.width = True
        self.height = 45
        self.func = None
        self.on_hover = lambda e: self.highlight(e)
        self.border_radius = 15
        self.icon_button = ft.IconButton(icon=icone, icon_color=ft.Colors.BLUE_100, icon_size=20, on_click=self.func, style=ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=7)}, overlay_color={"": "transparent"}))
        self.texto_button = ft.Text(value=texto, color=ft.Colors.BLUE_100, size=12, animate_opacity=500)
        self.content = ft.Row(
            controls=[
                self.icon_button,
                self.texto_button
            ]
        )
    
    def highlight(self, e):
        if e.data == "true":
            self.bgcolor = ft.Colors.with_opacity(0.30, ft.Colors.BLUE_100)
            self.update()
        else:
            self.bgcolor = None
            self.update()


class DATATABLE_STATUS_ATIVIDADE(ft.DataTable):
    def __init__(self, status):
        columns = [
            ft.DataColumn(ft.Text("CP", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_300)),
            ft.DataColumn(ft.Text("CLIENTE", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_300)),
            ft.DataColumn(ft.Text("ATIVIDADE", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_300)),
            ft.DataColumn(ft.Text("DIAGRAMA", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_300)),
            ft.DataColumn(ft.Text("DATA FINAL", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_300)),
            ft.DataColumn(ft.Text("Action", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_300)),
        ]
        super().__init__(columns=columns, rows=[])
        self.status = status
        self.expand = True
        self.border = ft.border.all(1, ft.Colors.with_opacity(0.80, ft.Colors.BLUE_900))
        self.border_radius = 15