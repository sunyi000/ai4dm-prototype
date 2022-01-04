import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace
from rdflib.namespace import XSD,SKOS,OWL
from rdflib.term import URIRef
import numpy as np
from config import Config

class Aircraft:

    def __init__(self,graph,file):
        self.df = pd.read_csv(file,sep="\t",quotechar='"')
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
        self.g.bind("-data", Config.ai4dm_data)

    def generate_cv(self,vocab):
        self.__init_graph()
        self.g.add((URIRef(Config.cv_ai4dm + vocab), RDF.type, OWL.Ontology))
        self.g.add((URIRef(Config.cv_ai4dm + vocab), OWL.imports, URIRef('http://www.w3.org/2004/02/skos/core')))
        dfm = list(self.df[vocab].unique())

        for index,m in enumerate(dfm):
            m_u = m.replace(".", "")
            m_u = m_u.replace(" ","_")
            self.g.add((URIRef(Config.cv_ai4dm+m_u), RDF.type,SKOS.Concept))
            self.g.add((URIRef(Config.cv_ai4dm + m_u), SKOS.prefLabel, Literal(m,datatype=XSD.string)))
            self.g.add((URIRef(Config.cv_ai4dm + m_u), SKOS.hiddenLabel, Literal(index, datatype=XSD.integer)))

        self.g.serialize(f'flight-{vocab}.ttl',format='turtle')

    def create_triples(self,g):
        for i,row in self.df.iterrows():
            aircraft_id = int(row['aircraft_id'])
            instance_name =f"aircraft-{aircraft_id}"
            manufacturer = row['manufacturer'].replace(" ","_")
            model = row['model'].replace(" ","_")
            pc = row['physical_class']
            noe = row['no_of_engines']
            ac = row['approach_speed']
            wingtip = row['wingtip'].replace(" ","_")
            wingspan = row['wingspan']
            l = row['length']
            th = row['tail_height']
            mtow = row['MTOW']
            max_ramp = row['max_ramp']
            gc = row['gear_config']
            icao = row['icao']
            wc =row['wake_category']
            pa = row['parking_area']
            iata = row['iata']
            airline = row['airline']


            g.add((URIRef(Config.ai4dm_data + instance_name), RDF.type,URIRef(Config.ai4dm + "Aircraft")))
            g.add((URIRef(Config.ai4dm_data + instance_name), SKOS.hiddenLabel, Literal(aircraft_id, datatype=XSD.integer)))
            g.add((URIRef(Config.ai4dm_data + instance_name), SKOS.prefLabel, Literal(instance_name,datatype=XSD.string)))
            g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasManufacturer"),
                   URIRef(Config.cv_ai4dm + manufacturer)))
            g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "aircraftModel"),
                   Literal(model, datatype=XSD.string)))
            g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasPhysicalClass"),
                   URIRef(Config.cv_ai4dm + pc)))
            if isinstance(noe,(int)):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasEngineCount"),
                    Literal(noe, datatype=XSD.integer)))
            if isinstance(ac, (int, float)):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasApproachSpeed"),
                    Literal(ac, datatype=XSD.float)))
            g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasWingtip"),
                    URIRef(Config.cv_ai4dm + wingtip)))
            if isinstance(wingspan, (int, float)):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasWingSpan"),
                    Literal(wingspan, datatype=XSD.float)))
            if isinstance(l, (int, float,str)):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasAircraftLength"),
                    Literal(l, datatype=XSD.float)))
            if isinstance(mtow, (int, float)):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasMTOW"),
                    Literal(mtow, datatype=XSD.float)))
            if isinstance(max_ramp, (int, float)):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasMaxRamp"),
                    Literal(max_ramp, datatype=XSD.float)))
            if isinstance(th, (int, float)) and str(th)!='tbd':
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasTailHeight"),
                    Literal(th, datatype=XSD.float)))
            if gc != "" and gc != "tbd" and isinstance(gc, str) and gc is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasGearConfig"),
                           URIRef(Config.cv_ai4dm + gc)))
            if icao !="" and icao !="tbd" and isinstance(icao,str) and icao is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasIcaoCode"),
                    Literal(icao, datatype=XSD.string)))
            if wc !="" and wc !="tbd" and isinstance(wc,str) and wc is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasWakeCategory"),
                    URIRef(Config.cv_ai4dm + wc)))

            if isinstance(pa, (int, float)):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasParkingArea"),
                    Literal(pa, datatype=XSD.float)))
            if iata !="" and icao !="tbd" and isinstance(iata,str) and iata is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasIataCode"),
                    Literal(iata, datatype=XSD.string)))

            if isinstance(airline,str):
                if airline != "":
                    al = airline.split(".")

                    for a in al:
                        an = f"airline-{a}"
                        g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "isAircraftOf"),
                               URIRef(f"{Config.ai4dm_data}{an}")))

        return g












