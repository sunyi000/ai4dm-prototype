import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace
from rdflib.namespace import XSD,SKOS,OWL
from rdflib.term import URIRef
import numpy as np
from config import Config

class Flight:

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


    def generate_cv(self,vocab):
        self.__init_graph()
        self.g.add((URIRef(Config.cv_ai4dm + vocab), RDF.type, OWL.Ontology))
        self.g.add((URIRef(Config.cv_ai4dm + vocab), OWL.imports, URIRef('http://www.w3.org/2004/02/skos/core')))

        types = {
            "commercial-passenger": "commercial passenger flights",
            "non-commercial": "non-commercial flights",
            "spo": "specialised operation flights",
            "commercial-cargo": "commercial cargo flights",
            "chartered": "chartered flights"
        }

        for k,v in types.items():
            self.g.add((URIRef(Config.cv_ai4dm + k), RDF.type,SKOS.Concept))
            self.g.add((URIRef(Config.cv_ai4dm + k), SKOS.prefLabel, Literal(v,datatype=XSD.string)))
            self.g.add((URIRef(Config.cv_ai4dm + k), SKOS.hiddenLabel, Literal(k, datatype=XSD.string)))

        self.g.serialize(f'flight-type.ttl',format='turtle')

    def create_triples(self,g):
        for i,row in self.df.iterrows():
            airline_code = row['airline_code']
            airline_id = row['airline_id']
            origin_code = row['origin_code']
            oring_id =row['origin_id']
            dest_code = row['dest_code']
            dest_id = row['dest_id']
            stops = row['stops']
            flight_no = row['flight_no']
            plane_type = row['plane_type']
            flight_type=row['flight_type']
            aircraft_id = row['aircraft_id']

            instance_name = f"flight-{flight_no}"

            g.add((URIRef(Config.ai4dm_data + instance_name), RDF.type,URIRef(Config.ai4dm + "Flight")))
            g.add((URIRef(Config.ai4dm_data + instance_name), SKOS.prefLabel, Literal(flight_no,datatype=XSD.string)))
            g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasFlightNo"),
                                                           Literal(flight_no, datatype=XSD.string)))

            if flight_type !="":
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasFlightType"),
                       URIRef(Config.cv_ai4dm + flight_type)))

            if origin_code !="" and origin_code is not None:
                an = f"airport-{origin_code}"
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasOrigin"),
                       URIRef(f"{Config.ai4dm_data}{an}")))

            if dest_code !="" and origin_code is not None:
                an = f"airport-{dest_code}"
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasDestination"),
                       URIRef(f"{Config.ai4dm_data}{an}")))

            if aircraft_id !="" and aircraft_id is not None:
                an = f"aircraft-{aircraft_id}"
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasAircraft"),
                       URIRef(f"{Config.ai4dm_data}{an}")))

            if airline_code !="" and airline_code is not None:
                an = f"airline-{airline_code}"
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "isFlightOf"),
                       URIRef(f"{Config.ai4dm_data}{an}")))

            if stops !="" and stops is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasStops"),
                       Literal(stops,datatype=XSD.integer)))

        return g






