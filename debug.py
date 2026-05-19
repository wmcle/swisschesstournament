import flet as ft
import logging
logging.basicConfig(level=logging.DEBUG, filename="flet_debug.log")
import db
import engine
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
def main(page: ft.Page):
    print("Iniciando main...")
    page.title = "SP26 - Gerenciador de Torneios"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    page.window_width = 900
    page.window_height = 700
    db.init_db()
    name_input = ft.TextField(label="Nome", expand=True)
    rating_input = ft.TextField(label="Rating", value="1200", width=120)
    btn = ft.FilledButton("Adicionar Jogador", icon="person_add", height=50)
    players_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("ID"))], rows=[])
    try:
        page.add(ft.Row([ft.Icon("emoji_events", size=40, color=ft.Colors.AMBER), ft.Text("Torneios")]))
        print("Page add ok")
    except Exception as e:
        print(f"Error page add: {e}")
ft.app(target=main)
