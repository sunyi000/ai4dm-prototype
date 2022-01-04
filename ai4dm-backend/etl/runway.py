import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace
from rdflib.namespace import XSD,SKOS,OWL
from rdflib.term import URIRef
import urllib
from config import Config

class Runway:

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
        self.g.bind("ai4dm-data",Config.ai4dm_data)


    def generate_cv(self,vocab):
        self.__init_graph()
        self.g.add((URIRef(Config.cv_ai4dm + vocab), RDF.type, OWL.Ontology))
        self.g.add((URIRef(Config.cv_ai4dm + vocab), OWL.imports, URIRef('http://www.w3.org/2004/02/skos/core')))
        dfm = list(self.df[vocab].unique())
        dfm = ["NA" if not isinstance(x,str) else x for x in dfm]

        for index,m in enumerate(dfm):
            self.g.add((URIRef(Config.cv_ai4dm + m), RDF.type,SKOS.Concept))
            self.g.add((URIRef(Config.cv_ai4dm + m), SKOS.prefLabel, Literal(m,datatype=XSD.string)))
            self.g.add((URIRef(Config.cv_ai4dm + m), SKOS.hiddenLabel, Literal(index, datatype=XSD.integer)))

        self.g.serialize(f'runway-{vocab}.ttl',format='turtle')

    def create_triples(self,g):
        for i, row in self.df.iterrows():
            airport_ref = row['airport_ref']
            airport_ident = row['airport_ident']
            length = row['length_ft']
            width = row['width_ft']

            surface = row['surface']
            lighted = row['lighted']
            iata = row["airport_iata"] if isinstance(row["airport_iata"],str) and row['airport_iata']!="" else ""
            aircrafts = row["aircraft_id"].split(",")


            instance_name = f"runway-{airport_ident}"

            g.add((URIRef(Config.ai4dm_data + instance_name), RDF.type,URIRef(Config.ai4dm + "Runway")))
            g.add((URIRef(Config.ai4dm_data + instance_name), SKOS.prefLabel, Literal(instance_name,datatype=XSD.string)))
            g.add((URIRef(Config.ai4dm_data + instance_name), SKOS.hiddenLabel,Literal(airport_ref, datatype=XSD.string)))

            if length is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasRunwayLength"),
                       Literal(length,datatype=XSD.float)))

            if width is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasWidth"),
                       Literal(width,datatype=XSD.float)))

            if lighted is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasLighted"),
                       Literal(lighted,datatype=XSD.boolean)))

            if surface is not None and isinstance(surface,str):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasSurface"),
                       URIRef(Config.cv_ai4dm+urllib.parse.quote(surface))))

            if iata !="":
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "isRunwayOf"),
                       URIRef(Config.ai4dm_data+f"airport-{iata}")))
            else:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "isRunwayOf"),
                       URIRef(Config.ai4dm_data+f"airport-{airport_ident}")))

            if len(aircrafts)>0:
                for a in aircrafts:
                    g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "capableOfLanding"),
                           URIRef(Config.ai4dm_data + f"aircraft-{a}")))



        return g



