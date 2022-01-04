import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace
from rdflib.namespace import XSD,SKOS,DCTERMS
from rdflib.term import URIRef
import urllib
from config import Config

class Airport:

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
        self.g.bind("dct", "http://purl.org/dc/terms/")
        self.g.bind("geo",Config.geo)



    def create_triples(self,g):
        for i, row in self.df.iterrows():
            airport_ref = row['id']
            airport_ident = row['ident']
            type = row['type']
            name = row['name']
            lat = row['latitude_deg']

            longitude = row['longitude_deg']
            elev = row['elevation_ft']
            country = row['iso_country']
            region=row['iso_region']
            municipality = row["municipality"]
            gps_code = row["gps_code"]
            iata = row["iata_code"] if isinstance(row["iata_code"],str) else ""
            local_code = row['local_code']

            if iata!="":
                instance_name = f"airport-{iata}"
            else:
                instance_name = f"airport-{airport_ident}"

            g.add((URIRef(Config.ai4dm_data + instance_name), RDF.type,URIRef(Config.ai4dm + "Airport")))
            g.add((URIRef(Config.ai4dm_data + instance_name), SKOS.prefLabel, Literal(instance_name,datatype=XSD.string)))
            g.add((URIRef(Config.ai4dm_data + instance_name), DCTERMS.description,Literal(name, datatype=XSD.string)))
            g.add((URIRef(Config.ai4dm_data + instance_name), SKOS.hiddenLabel,Literal(airport_ref, datatype=XSD.string)))

            if type is not None and isinstance(type,str):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "airportType"),
                       URIRef(Config.cv_ai4dm + type)))

            if lat is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.geo + "lat"),
                       Literal(lat,datatype=XSD.float)))

            if longitude is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.geo + "long"),
                       Literal(longitude,datatype=XSD.float)))

            if elev is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasElevation"),
                       Literal(elev,datatype=XSD.float)))

            if country is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasCountry"),
                       URIRef(Config.ai4dm_data+f"country-{country}")))

            if region is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "regionServed"),
                       URIRef(Config.ai4dm_data+f"region-{region}")))

            if municipality is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasMunicipality"),
                       Literal(municipality,datatype=XSD.string)))

            if gps_code is not None:
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasGPSCode"),
                       Literal(gps_code,datatype=XSD.string)))
            if iata is not None and isinstance(iata,str):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasFAAIdentifier"),
                       Literal(iata,datatype=XSD.string)))
            if local_code is not None and isinstance(local_code,str):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasLocalCode"),
                       Literal(local_code,datatype=XSD.string)))
            if airport_ident is not None and isinstance(airport_ident,str):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasAirportIdent"),
                       Literal(airport_ident,datatype=XSD.string)))




        return g



