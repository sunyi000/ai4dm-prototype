import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace
from rdflib.namespace import XSD,SKOS,OWL
from rdflib.term import URIRef
import math
from config import Config

class Region:

    def __init__(self,g,file=None):
        self.df = pd.read_csv(file,sep="\t",quotechar='"')
        self.g = g

    def __init_graph(self):
        self.g.bind("cv-ai4dm",Config.cv_ai4dm)
        self.g.bind("skos",Config.skos)
        self.g.bind("xsd",Config.xsd)
        self.g.bind("owl",Config.owl)
        self.g.bind("rdf", Config.rdf)
        self.g.bind("rdfs",Config.rdfs)
        self.g.bind("ai4dm", Config.ai4dm)
        self.g.bind("cv", Config.cv)
        self.g.bind("ai4dm-data", Config.ai4dm_data)


    def generate_cv_continent(self):
        vocab = 'continent'
        self.__init_graph()
        self.g.add((URIRef(Config.cv_ai4dm + vocab), RDF.type, OWL.Ontology))
        self.g.add((URIRef(Config.cv_ai4dm + vocab), OWL.imports, URIRef('http://www.w3.org/2004/02/skos/core')))
        dfm = list(self.df[vocab].unique())
        dfm = ["NA" if not isinstance(x,str) else x for x in dfm]

        for index,m in enumerate(dfm):
            self.g.add((URIRef(Config.cv_ai4dm + m), RDF.type,SKOS.Concept))
            self.g.add((URIRef(Config.cv_ai4dm + m), SKOS.prefLabel, Literal(m,datatype=XSD.string)))
            self.g.add((URIRef(Config.cv_ai4dm + m), SKOS.hiddenLabel, Literal(index, datatype=XSD.integer)))

        self.g.serialize(f'region-{vocab}.ttl',format='turtle')

    def generate_cv_code(self):
        self.__init_graph()
        self.g.add((URIRef(Config.cv_ai4dm + 'code'), RDF.type, OWL.Ontology))
        self.g.add((URIRef(Config.cv_ai4dm + 'code'), OWL.imports, URIRef('http://www.w3.org/2004/02/skos/core')))
        dfm = self.df[['code', 'name']].drop_duplicates()

        for index, row in dfm.iterrows():
            code = repr(row['code'])
            label = row['name']
            self.g.add((URIRef(Config.cv_ai4dm + code), RDF.type, SKOS.Concept))
            self.g.add((URIRef(Config.cv_ai4dm + code), SKOS.prefLabel, Literal(label, datatype=XSD.string)))
            self.g.add((URIRef(Config.cv_ai4dm + code), SKOS.hiddenLabel, Literal(code, datatype=XSD.string)))

        self.g.serialize(f'region-code.ttl', format='turtle')

    def create_triples(self,g):
        for i, row in self.df.iterrows():
            region_code = row['code']
            name = row['name']
            continent = row['continent']
            country = row['iso_country']
            wikilink = row['wikipedia_link']

            instance_name = f"region-{region_code}"

            g.add((URIRef(Config.ai4dm_data + instance_name), RDF.type,URIRef(Config.ai4dm + "Region")))
            g.add((URIRef(Config.ai4dm_data + instance_name), SKOS.prefLabel, Literal(name,datatype=XSD.string)))
            g.add((URIRef(Config.ai4dm_data + instance_name), SKOS.hiddenLabel,Literal(region_code, datatype=XSD.string)))

            if region_code is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasRegionCode"),
                       URIRef(Config.cv_ai4dm + region_code)))

            if country is not None:
                if isinstance(country,float):
                    country = "NA"
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "isRegionOf"),
                         URIRef(Config.ai4dm_data + "country-"+country)))

            if continent is not None:
                if isinstance(continent,float):
                    continent = "NA"

                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasContinent"),
                       URIRef(Config.cv_ai4dm + continent)))


            if wikilink is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasWikiLink"),
                       Literal(wikilink,datatype=XSD.anyURI)))



        return g




