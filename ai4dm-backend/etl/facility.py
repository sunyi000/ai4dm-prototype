import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace
from rdflib.namespace import XSD,SKOS,OWL
from rdflib.term import URIRef

from config import Config


class Facility:

    def __init__(self):
        pass

    def __init_graph(self):
        self.g = Graph()
        self.g.bind("cv-ai4dm",Config.cv_ai4dm)
        self.g.bind("skos",Config.skos)
        self.g.bind("xsd",Config.xsd)
        self.g.bind("owl",Config.owl)
        self.g.bind("rdf", Config.rdf)
        self.g.bind("rdfs",Config.rdfs)


    def generate_cv(self,vocab):
        self.__init_graph()
        self.g.add((URIRef(Config.cv_ai4dm + vocab), RDF.type, OWL.Ontology))
        self.g.add((URIRef(Config.cv_ai4dm + vocab), OWL.imports, URIRef('http://www.w3.org/2004/02/skos/core')))

        types = {
            "fire": "fire station",
            "ambulance": "ambulance",
            "hospital": "hospital",
            "police": "police station",
            "helicopter": "chartered flights",
            "hotel": "hotel close to airport"
        }

        for k,v in types.items():
            self.g.add((URIRef(Config.cv_ai4dm + k), RDF.type,SKOS.Concept))
            self.g.add((URIRef(Config.cv_ai4dm + k), SKOS.prefLabel, Literal(v,datatype=XSD.string)))
            self.g.add((URIRef(Config.cv_ai4dm + k), SKOS.hiddenLabel, Literal(k, datatype=XSD.string)))

        self.g.serialize(f'facility-type.ttl',format='turtle')



