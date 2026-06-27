from gc import disable

import flet as ft

class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Lab11-Simulazione esame"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None

        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        # 1. Titolo del tema d'esame
        self._title = ft.Text("Esame 24/01/2024 - Turno Unico", color="blue", size=24, weight=ft.FontWeight.BOLD)
        self._page.controls.append(self._title)

        # 2. Creazione dei componenti di input (Dropdown e TextField)
        self.ddyear = ft.Dropdown(label="Anno", width=200)
        self._controller.fillDDYear()
        self.ddmetodo = ft.Dropdown(label="Metodo", width=200)
        self._controller.fillDDMetodo()
        self.txt_s = ft.TextField(label="S", width=200)

        # 3. Creazione dei Bottoni
        self.btn_crea_grafo = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleCreaGrafo, width=200)
        self.btn_prodotti = ft.ElevatedButton(text="Calcola Prodotti Redditizi",
                                              on_click=self._controller.handleProdotti, width=200,disabled=True)
        self.btn_cammino = ft.ElevatedButton(text="Calcola Cammino", on_click=self._controller.handleCammino, width=200,disabled=True)

        # 4. Organizzazione del Layout (Affianchiamo input e bottoni)
        # Creiamo una riga principale che contiene a sinistra la colonna dei controlli e a destra quella dei bottoni
        input_layout = ft.Row(
            controls=[
                # Colonna Sinistra: Input numerici/scelte
                ft.Column(
                    controls=[
                        self.ddyear,
                        self.ddmetodo,
                        self.txt_s
                    ],
                    spacing=10
                ),
                # Colonna Destra: Bottoni delle azioni
                ft.Column(
                    controls=[
                        self.btn_crea_grafo,
                        self.btn_prodotti,
                        self.btn_cammino
                    ],
                    spacing=10
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=50  # Spazio generoso tra la colonna degli input e quella dei bottoni
        )

        self._page.controls.append(input_layout)

        # 5. Area di Output per i risultati (Già presente nel tuo codice, distanziata dal layout sopra)
        self._page.controls.append(ft.Container(height=20))  # Un piccolo spazio vuoto divisorio
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)

        # 6. Render finale della pagina
        self._page.update()


    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()