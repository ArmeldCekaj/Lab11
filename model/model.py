from database.DAO import DAO
import networkx as nx
class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
    def get_years(self):
        return DAO.get_years()
    def get_colors(self):
        return DAO.get_colors()

    def buildGraph(self, year, color):
        self._idMap = DAO.get_nodes(self._idMap, color)
        self._graph.add_nodes_from(list(self._idMap.values()))
        edges = DAO.getAllEdges(self._idMap, year, color)
        for e in edges:
            if e.node1 in self._graph and e.node2 in self._graph:
                self._graph.add_edge(e.node1, e.node2, weight=e.weight)

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def analyze(self):
        result = []
        for node1 in self._graph.nodes:
            for node2 in self._graph.nodes:
                if self._graph.has_edge(node1, node2) and (
                node2.Product, node1.Product, self._graph[node1][node2]['weight']) not in result:
                    result.append((node1.Product, node2.Product, self._graph[node1][node2]['weight']))
        result.sort(key=lambda x: x[2], reverse=True)
        result_tot = []
        for i in range(0, 3):
            result_tot.append(result[i])
        nodi_ripetuti = []
        for result in result_tot:
            name_to_count1 = result[0]
            count1 = sum(name_to_count1 in t for t in result_tot)
            name_to_count2 = result[1]
            count2 = sum(name_to_count2 in t for t in result_tot)
            if count1 > 1 and name_to_count1 not in nodi_ripetuti:
                nodi_ripetuti.append(name_to_count1)
            if count2 > 1 and name_to_count2 not in nodi_ripetuti:
                nodi_ripetuti.append(name_to_count2)
        return result_tot, nodi_ripetuti



