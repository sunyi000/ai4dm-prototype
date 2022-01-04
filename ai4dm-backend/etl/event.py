import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace
from rdflib.namespace import XSD,SKOS,OWL
from rdflib.term import URIRef
import numpy as np
from config import Config

class Event:

    def __init__(self,graph,file=None):
        self.df = pd.read_csv(file, sep="\t", quotechar='"')
        self.g = graph

    def __init_graph(self):
        self.g.bind("cv-ai4dm",Config.cv_ai4dm)
        self.g.bind("skos",Config.skos)
        self.g.bind("xsd",Config.xsd)
        self.g.bind("owl",Config.owl)
        self.g.bind("rdf", Config.rdf)
        self.g.bind("rdfs",Config.rdfs)
        self.g.bind("ai4dm", Config.ai4dm)
        self.g.bind("cv", Config.cv)
        self.g.bind("cv", Config.ai4dm_data)


    def create_triples(self,g):
        for i, row in self.df.iterrows():
            event_date = row['event_date']
            event_type = row['event_type']
            region = row['region']
            event_name = row['event_name']
            aircraft_id = row['aircraft_id']
            event_id=row['event_id']

            instance_name = f"event-{event_id}"

            g.add((URIRef(Config.ai4dm_data + instance_name), RDF.type,URIRef(Config.ai4dm + "Event")))
            g.add((URIRef(Config.ai4dm_data + instance_name), SKOS.prefLabel, Literal(event_id,datatype=XSD.string)))
            g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasEventID"),
                                                           Literal(event_id, datatype=XSD.string)))

            if event_date is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "eventDate"),
                         Literal(event_date,datatype=XSD.date)))

            if event_type is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasEventType"),
                         URIRef(Config.cv_ai4dm + event_type)))

            if event_name is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "eventName"),
                         Literal(event_name,datatype=XSD.string)))

            if region is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasRegion"),
                         URIRef(Config.ai4dm_data +"region-"+region)))

            if aircraft_id is not None:
                ai = aircraft_id.split(",")
                if len(ai)>0:
                    for a in ai:
                        g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "isAircraftEventOf"),
                         URIRef(f"{Config.ai4dm_data}aircraft-{a}" )))


        return g






