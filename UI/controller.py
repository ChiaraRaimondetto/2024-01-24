import flet as ft
from markdown_it.rules_core import replace


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.metodo=None
        self.anno=None
    def handleProdotti(self,e):
        top5 = self._model.getTop5(self.anno, self.metodo)
        if top5 is not None:
            self._view.txt_result.controls.append(ft.Text(f"Di seuito i prodotii più redditizi:"))
            for p in top5:
                self._view.txt_result.controls.append(ft.Text(f"Prodotto: {p[0]}   Archi entranti:{p[1]}   Ricavo: {p[2]}"))
        else:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Non abbiamo trovato prodotti più redditizi di altri"))
            self._view.update_page()
            return
        self._view.update_page()

    def handleCreaGrafo(self,e):
        s=self._view.txt_s.value
        if self.anno is not None and self.metodo is not None and s is not None:
            try:
                floatS=float(s.replace(',', '.'))
                self._model.buildGraph(self.anno,self.metodo,floatS)
                n,a= self._model.getDettagli()
                if n is not None and s is not None:
                    self._view.txt_result.controls.clear()
                    self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato con {n} nodi e {a} archi"))
                else:
                    self._view.txt_result.controls.clear()
                    self._view.txt_result.controls.append(ft.Text(f"Non siamo riusciti a creare il grafo"))
                    self._view.update_page()
                    return

            except ValueError:
                self._view.txt_result.controls.clear()
                self._view.txt_result.controls.append("Inserire un valore numerico con il punto")
                self._view.update_page()
                return
        else:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append("Selezionare un anno, un metodo e un valore numerico con il punto")
            self._view.update_page()
            return
        self._view.btn_prodotti.disabled = False
        self._view.btn_cammino.disabled=False
        self._view.update_page()


    def handleCammino(self,e):
        ottimo,lung=self._model.bestCammino(self.anno,self.metodo)
        if ottimo is not None and lung is not None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Il cammino ottimo ha lunghezza {lung}\n"
                                                          f"Di seguito i nodi del cammino ottimo:"))
            for n in ottimo:
                self._view.txt_result.controls.append(ft.Text(f"Prodotto: {n[0]} Ricavo: {n[1]}"))
        else:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Non siamo riusciti a trovare il cammino ottimo"))
            self._view.update_page()
            return
        self._view.update_page()
    def fillDDMetodo(self):
        metodi=self._model.getMetodi()
        for m in metodi:
            self._view.ddmetodo.options.append(ft.dropdown.Option(data=m,text=m.Order_method_type,on_click=self.readMetodo))
    def readMetodo(self,e):
        if e.control.data is None:
            self.metodo=None
        else:
            self.metodo=e.control.data
    def fillDDYear(self):
        for i in range(2015,2019):
            self._view.ddyear.options.append(ft.dropdown.Option(data=i,text=i,on_click=self.readAnno))

    def readAnno(self, e):
        if e.control.data is None:
            self.anno = None
        else:
            self.anno = e.control.data