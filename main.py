import flet as ft
import db
import engine
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def main(page: ft.Page):
    page.title = "SP26 - Clone do Swiss Perfect 98"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window_width = 1000
    page.window_height = 800

    db.init_db()

    # --- ABA 1: JOGADORES ---
    name_input = ft.TextField(label="Nome do Jogador", expand=True)
    rating_input = ft.TextField(label="Rating", value="1200", width=120)
    
    players_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nº")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Rating")),
            ft.DataColumn(ft.Text("Pts")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[]
    )

    def edit_player_click(pid, current_name, current_rating):
        edit_name = ft.TextField(label="Nome", value=current_name)
        edit_rating = ft.TextField(label="Rating", value=str(current_rating))
        
        def save_edit(e):
            db.update_player(pid, edit_name.value, int(edit_rating.value) if edit_rating.value.isdigit() else 1200)
            dlg.open = False
            page.update()
            refresh_players_table()

        def cancel_edit(e):
            dlg.open = False
            page.update()
            
        dlg = ft.AlertDialog(
            title=ft.Text("Editar Jogador"),
            content=ft.Column([edit_name, edit_rating], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=cancel_edit),
                ft.FilledButton("Salvar", on_click=save_edit)
            ]
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def confirm_delete_click(pid, name):
        def perform_delete(e):
            db.delete_player(pid)
            dlg.open = False
            page.update()
            refresh_players_table()

        def cancel_delete(e):
            dlg.open = False
            page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text(f"Tem certeza que deseja excluir o jogador '{name}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancel_delete),
                ft.FilledButton("Sim, excluir", on_click=perform_delete)
            ]
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def refresh_players_table():
        players_table.rows.clear()
        try:
            standings_table.rows.clear()
        except NameError:
            pass # standings_table can be undefined on first load if we don't move the function down
            
        pos = 1
        for p in db.get_all_players():
            pid, name, rating, points = p[0], p[1], p[2], p[3]
            
            edit_btn = ft.IconButton(icon=ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, i=pid, n=name, r=rating: edit_player_click(i, n, r))
            del_btn = ft.IconButton(icon=ft.Icons.DELETE, tooltip="Excluir", on_click=lambda e, i=pid, n=name: confirm_delete_click(i, n))
            
            players_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(pid))),
                    ft.DataCell(ft.Text(name)),
                    ft.DataCell(ft.Text(str(rating))),
                    ft.DataCell(ft.Text(str(points))),
                    ft.DataCell(ft.Row([edit_btn, del_btn], spacing=0)),
                ])
            )
            
            try:
                standings_table.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(pos))),
                        ft.DataCell(ft.Text(str(pid))),
                        ft.DataCell(ft.Text(name)),
                        ft.DataCell(ft.Text(str(rating))),
                        ft.DataCell(ft.Text(str(points), weight=ft.FontWeight.BOLD)),
                    ])
                )
            except NameError:
                pass
            pos += 1
            
        page.update()

    def add_click(e):
        if name_input.value:
            rating = int(rating_input.value) if rating_input.value.isdigit() else 1200
            db.add_player(name_input.value, rating)
            name_input.value = ""
            refresh_players_table()

    tab_jogadores = ft.Column([
        ft.Row([name_input, rating_input, ft.FilledButton("Adicionar Jogador", on_click=add_click)]),
        ft.Divider(),
        players_table
    ], visible=True)

    # --- ABA 2: EMPARCEIRAMENTOS ---
    pairings_list = ft.Column(spacing=5)
    current_pairings = []
    
    def generate_round_click(e):
        players = db.get_all_players()
        if len(players) < 2:
            return
            
        pairings = engine.generate_pairings(players)
        pairings_list.controls.clear()
        current_pairings.clear()
        
        for pair in pairings:
            p1, p2 = pair[0], pair[1]
            if p2 is None:
                pairings_list.controls.append(ft.Text(f"{p1[1]} recebe o BYE (1 ponto)", text_align=ft.TextAlign.CENTER))
                current_pairings.append({"p1": p1[0], "p2": None, "dd": None})
            else:
                dd = ft.Dropdown(
                    options=[ft.dropdown.Option("?"), ft.dropdown.Option("1-0"), ft.dropdown.Option("0-1"), ft.dropdown.Option("1/2-1/2")],
                    value="?",
                    width=100
                )
                row = ft.Row([
                    ft.Text(f"{p1[1]}", width=150, text_align=ft.TextAlign.RIGHT),
                    dd,
                    ft.Text(f"{p2[1]}", width=150, text_align=ft.TextAlign.LEFT)
                ], alignment=ft.MainAxisAlignment.CENTER)
                pairings_list.controls.append(row)
                current_pairings.append({"p1": p1[0], "p2": p2[0], "dd": dd})
                
        page.update()

    def save_results_click(e):
        if not current_pairings:
            return
            
        for match in current_pairings:
            if match["p2"] is None:
                db.record_match(match["p1"], None, "bye")
            else:
                dd = match["dd"]
                if dd.value != "?":
                    db.record_match(match["p1"], match["p2"], dd.value)
                    
        current_pairings.clear()
        pairings_list.controls.clear()
        refresh_players_table()
        
        # Volta pra aba de jogadores para o árbitro ver a nova pontuação
        tab_emparceiramentos.visible = False
        tab_jogadores.visible = True
        page.update()

    tab_emparceiramentos = ft.Column([
        ft.Row([
            ft.FilledButton("Gerar Próxima Rodada", on_click=generate_round_click),
            ft.FilledButton("Salvar Resultados e Encerrar Rodada", on_click=save_results_click, style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_700))
        ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        pairings_list
    ], visible=False)

    # --- ABA 3: CLASSIFICAÇÃO ---
    standings_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Pos")),
            ft.DataColumn(ft.Text("Nº")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Rating")),
            ft.DataColumn(ft.Text("Pts")),
        ],
        rows=[]
    )

    tab_classificacao = ft.Column([
        ft.Row([ft.Text("Classificação Geral", size=20, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        standings_table
    ], visible=False)

    # --- NAVEGAÇÃO CUSTOMIZADA (Fake Tabs para evitar bugs da versão) ---
    def switch_tab(e):
        tab_name = e.control.data
        tab_jogadores.visible = (tab_name == "Jogadores")
        tab_emparceiramentos.visible = (tab_name == "Emparceiramentos")
        tab_classificacao.visible = (tab_name == "Classificação")
        page.update()

    nav_menu = ft.Row([
        ft.FilledButton("Jogadores", data="Jogadores", on_click=switch_tab),
        ft.FilledButton("Emparceiramentos", data="Emparceiramentos", on_click=switch_tab),
        ft.FilledButton("Classificação", data="Classificação", on_click=switch_tab)
    ], alignment=ft.MainAxisAlignment.CENTER)

    page.add(
        ft.Row([ft.Text("Inspirado em Swiss Perfect 98", size=24, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
        nav_menu,
        ft.Divider(),
        tab_jogadores,
        tab_emparceiramentos,
        tab_classificacao
    )
    
    refresh_players_table()

if __name__ == "__main__":
    ft.app(target=main)
