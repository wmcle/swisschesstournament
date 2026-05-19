import flet as ft
def main(page: ft.Page):
    dlg = ft.AlertDialog(title=ft.Text("Test"))
    def show_dlg(e):
        page.dialog = dlg
        dlg.open = True
        page.update()
    page.add(ft.ElevatedButton("Show", on_click=show_dlg))
ft.app(target=main)
