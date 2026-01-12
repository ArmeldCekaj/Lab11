import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []
        self._choiceDDNode = None

    def fillDD(self):
        years = self._model.get_years()
        for y in years:
            self._view._ddyear.options.append(ft.dropdown.Option(str(y), data=y))
        self._view.update_page()
        colors = self._model.get_colors()
        for i in colors:
            self._view._ddcolor.options.append(ft.dropdown.Option(str(i), data=i))
            self._view.update_page()


    def handle_graph(self, e):
        year = self._view._ddyear.value
        color = self._view._ddcolor.value
        if year == "" or year is None:
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append(ft.Text("Selezionare un anno."))
            return
        if color == "" or color is None:
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append(ft.Text("Selezionare un colore."))
            return

        self._model.buildGraph(year, color)
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text("Grafo Correttamente creato "))
        self._view.txtOut.controls.append(ft.Text(f"N nodi  {nNodes}"))
        self._view.txtOut.controls.append(ft.Text(f"N archi {nEdges}"))
        top3archi, nodiripetuti = self._model.analyze()
        for t in top3archi:
            self._view.txtOut.controls.append(ft.Text(t))
        for n in nodiripetuti:
            self._view.txtOut.controls.append(ft.Text(n))
        allNodes = self._model._graph.nodes
        self.fillDDProduct(allNodes)
        self._view.update_page()




    def fillDDProduct(self, allNodes):
        for n in allNodes:
            self._view._ddnode.options.append(ft.dropdown.Option(data = n, key=n.Product, on_click=self.pickDDNode))

    def pickDDNode(self,e):
        self._choiceDDNode = e.control.data


    def handle_search(self, e):
        pass
