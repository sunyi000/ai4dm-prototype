import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace
from rdflib.namespace import XSD,SKOS,OWL
from rdflib.term import URIRef
from config import Config
import urllib.parse

class Country:

    def __init__(self,g,file):
        self.df = pd.read_csv(file,sep="\t",quotechar='"')
        self.g = g

    def __init_graph(self):
        self.g.bind("cv-ai4dm",Config.cv_ai4dm)
        self.g.bind("skos",Config.skos)
        self.g.bind("xsd",Config.xsd)
        self.g.bind("owl",Config.owl)
        self.g.bind("rdf", Config.rdf)
        self.g.bind("rdfs",Config.rdfs)


    def generate_cv_code(self,vocab):
        self.__init_graph()
        self.g.add((URIRef(Config.cv_ai4dm + vocab), RDF.type, OWL.Ontology))
        self.g.add((URIRef(Config.cv_ai4dm + vocab), OWL.imports, URIRef('http://www.w3.org/2004/02/skos/core')))
        dfm = self.df[['code','name']].drop_duplicates()

        for index,row in dfm.iterrows():
            code = repr(row['code'])
            label = row['name']
            self.g.add((URIRef(Config.cv_ai4dm + code), RDF.type,SKOS.Concept))
            self.g.add((URIRef(Config.cv_ai4dm + code), SKOS.prefLabel, Literal(label,datatype=XSD.string)))
            self.g.add((URIRef(Config.cv_ai4dm + code), SKOS.hiddenLabel, Literal(code, datatype=XSD.string)))

        self.g.serialize(f'country-{vocab}.ttl',format='turtle')


    def create_triples(self,g):
        for i, row in self.df.iterrows():
            code = row['code']
            name = row['name']
            continent = row['continent']
            wikilink = row['wikipedia_link']

            instance_name = f"country-{code}"

            g.add((URIRef(Config.ai4dm_data + instance_name), RDF.type,URIRef(Config.ai4dm + "Country")))
            g.add((URIRef(Config.ai4dm_data + instance_name), SKOS.prefLabel, Literal(name,datatype=XSD.string)))
            g.add((URIRef(Config.ai4dm_data + instance_name), SKOS.hiddenLabel,Literal(code, datatype=XSD.string)))

            if code is not None:
                if isinstance(code,float):
                    code = "NA"
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasCountryCode"),
                       URIRef(Config.cv_ai4dm + code)))

            if continent is not None:
                if isinstance(continent,float):
                    continent = "NA"
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasContinent"),
                       URIRef(Config.cv_ai4dm + continent)))

            if wikilink is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasWikiLink"),
                       Literal(wikilink,datatype=XSD.anyURI)))



        return g

