import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace
from rdflib.namespace import XSD,SKOS,OWL,FOAF
from rdflib.term import URIRef
from config import Config
import urllib.parse

class Person:

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


    def create_triples(self,g):
        for i, row in self.df.iterrows():
            pid = row['person_id']
            name = urllib.parse.quote(row['name'])
            bp = f"region-{row['birth_place']}"
            am = urllib.parse.quote(f"institution-{row['alma_mater']}")
            nationality = f"country-{row['nationality']}"
            employer = f"airline-{row['employer']}"

            if isinstance(row['board_flight'],str):
                bf = row['board_flight'].split(",")
            else:
                bf =[]

            instance_name = f"person-{name}"

            g.add((URIRef(Config.ai4dm_data + instance_name), RDF.type,FOAF.Person))
            g.add((URIRef(Config.ai4dm_data + instance_name), FOAF.name, Literal(name,datatype=XSD.string)))
            g.add((URIRef(Config.ai4dm_data + instance_name), SKOS.prefLabel, Literal(name,datatype=XSD.string)))

            if isinstance(pid,(int,str)):
                g.add((URIRef(Config.ai4dm_data + instance_name), SKOS.hiddenLabel,Literal(pid, datatype=XSD.string)))

            if bp is not None and isinstance(bp,str):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasBirthPlace"),
                       URIRef(Config.ai4dm_data + bp)))

            if am is not None and isinstance(am,str):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "isAlumniOf"),
                       URIRef(Config.ai4dm_data +am )))

            if nationality is not None and isinstance(am,str):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasNationality"),
                       URIRef(Config.ai4dm_data +nationality)))

            if employer is not None and isinstance(am,str):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasEmployer"),
                       URIRef(Config.ai4dm_data +employer)))

            if len(bf)>0:
                for f in bf:
                    g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "boardFlight"),
                       URIRef(Config.ai4dm_data +"flight-"+f)))


        return g

