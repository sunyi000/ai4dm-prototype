import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace
from rdflib.namespace import XSD,SKOS,DCTERMS
from rdflib.term import URIRef
import urllib
from config import Config

class Airline:

    def __init__(self,g,file):
        self.df = pd.read_csv(file,sep="\t",quotechar='"',encoding='latin1')
        self.g = g

    def __init_graph(self):
        self.g.bind("geo", Config.geo)
        self.g.bind("cv-ai4dm",Config.cv_ai4dm)
        self.g.bind("skos",Config.skos)
        self.g.bind("xsd",Config.xsd)
        self.g.bind("owl",Config.owl)
        self.g.bind("rdf", Config.rdf)
        self.g.bind("rdfs",Config.rdfs)
        self.g.bind("ai4dm", Config.ai4dm)
        self.g.bind("ai4dm-data",Config.ai4dm_data)
        self.g.bind("cv", Config.cv)


    def add_multiple_obj(self,instance_name,g,pred,li,obj):
        if len(li)>0:
            for l in li:
                if obj=="person":
                    g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + pred),
                           URIRef(Config.ai4dm_data + f"person-data/{obj}-{urllib.parse.quote(l)}")))
                else:
                    g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + pred),
                       URIRef(Config.ai4dm_data+f"{obj}-data/{obj}-{l}")))

        return g



    def create_triples(self,g):
        for i, row in self.df.iterrows():
            name = row['name']
            icao = row["icao"]
            iata = row["iata"]
            callsign=row["callsign"]
            country=row["country"]
            alliance = [] if isinstance(row['alliance'],float) else row['alliance'].split(",")
            fleet_size = row['fleet_size']
            base = [] if isinstance(row['base'],float) else row['base'].split(",")
            target_airport = [] if isinstance(row['target_airport'],float) else row['target_airport'].split(",")
            headquarter = row['headquarter']
            founded_date = row['founded_date']
            focus = [] if isinstance(row['focus_region'],float) else row['focus_region'].split(",")
            netincome=row['netIncome']
            kp=[] if isinstance(row['key_people'],float) else row['key_people'].split(",")
            subsidary=row['subsidary_of']

            if isinstance(iata,str) and iata !="":
                instance_name = f"airline-{iata}"
            else:
                instance_name = urllib.parse.quote(name)

            g.add((URIRef(Config.ai4dm_data + instance_name), RDF.type,URIRef(Config.ai4dm + "Airline")))
            g.add((URIRef(Config.ai4dm_data + instance_name), SKOS.prefLabel, Literal(instance_name,datatype=XSD.string)))
            g.add((URIRef(Config.ai4dm_data + instance_name), DCTERMS.description,Literal(name, datatype=XSD.string)))
            g.add((URIRef(Config.ai4dm_data + instance_name), SKOS.hiddenLabel,Literal(instance_name, datatype=XSD.string)))

            if icao is not None and isinstance(icao,str):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasIcaoCode"),
                       Literal(icao,datatype=XSD.string)))

            if callsign is not None and isinstance(callsign,str):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasCallsign"),
                       Literal(callsign,datatype=XSD.string)))

            if fleet_size is not None and isinstance(fleet_size,(str,int)):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasFleetSize"),
                       Literal(fleet_size,datatype=XSD.integer)))

            if headquarter is not None and isinstance(headquarter,str):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasHeadquarter"),
                       URIRef(Config.ai4dm_data + "region-"+headquarter)))

            if country is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasCountry"),
                       URIRef(Config.ai4dm_data+f"country-{country}")))

            if founded_date is not None and isinstance(founded_date, str):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "foundedDate"),
                       Literal(founded_date,datatype=XSD.date)))

            if netincome is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "netIncome"),
                       Literal(netincome,datatype=XSD.string)))

            if subsidary is not None and isinstance(subsidary,str):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "isSubsidaryOf"),
                       URIRef(Config.ai4dm_data + "organisation-"+urllib.parse.quote(subsidary))))

            g = self.add_multiple_obj(instance_name,g,"hasBase",base,"airport")
            g = self.add_multiple_obj(instance_name, g, "hasAlliance", alliance, "airline")
            g = self.add_multiple_obj(instance_name, g, "targetAirport", target_airport, "airport")
            g = self.add_multiple_obj(instance_name, g, "hasFocusRegion", focus, "region")
            g = self.add_multiple_obj(instance_name, g, "hasKeyPeople", kp, "person")





        return g



