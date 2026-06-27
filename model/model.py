import copy

import networkx as nx
from websockets.headers import parse_extension_item

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.DiGraph()
        self.idMapN={}
        self._besc = []
        self.lung = 0

    def getMetodi(self):
        return DAO.getMetodi()
    def buildGraph(self,anno,metodo,s):
        nodi=DAO.getAllNodes(anno,metodo)
        for n in nodi:
            self.idMapN[n.Product_number]=n
        self._graph.add_nodes_from(nodi)
        self.addEdges(anno,metodo,self.idMapN,s)
    def addEdges(self,anno,metodo,idMap,s):
        archi=DAO.getAllEdges(anno,metodo,idMap,s)
        for a in archi:
            self._graph.add_edge(a.p1,a.p2)
    def getDettagli(self):
        return len(self._graph.nodes), len(self._graph.edges)
    def getTop5(self,anno,metodo):
        redittizi=[]
        for p in self._graph.nodes:
            if self._graph.out_degree(p)==0:
                redittizi.append(p)
        ordinati=sorted(redittizi,key=lambda x: self._graph.in_degree(x),reverse=True)
        top5=[]
        for o in ordinati:
            top5.append((o.Product_number,self._graph.in_degree(o),self.getRicavi(anno,metodo,o)))

        return top5[:5]
    def getRicavi(self,anno,metodo,o):
        return DAO.getRicavi(anno,metodo,o.Product_number)[0]
    def bestCammino(self,anno,metodo):
        self._besc=[]
        self.lung=0

        lista=[]
        for p in self._graph.nodes:
            if self._graph.in_degree(p)==0:
                lista.append(p)
        parziale=[]
        for p in lista:
            parziale.append(p)
            self.ricorsione(parziale)
            parziale.pop()

        ottimo=[]
        for p in self._besc:
            ottimo.append((p.Product_number,self.getRicavi(anno,metodo,p)))
        return ottimo,self.lung

    def ricorsione(self,parziale):
        if self._graph.out_degree(parziale[-1])==0:
            if len(parziale)>self.lung:
                self.lung=len(parziale)
                self._besc=copy.deepcopy(parziale)
            return
        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self.ricorsione(parziale)
                parziale.pop()
