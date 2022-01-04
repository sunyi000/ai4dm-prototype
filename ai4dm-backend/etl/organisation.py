import pandas as pd
from rdflib import Literal, RDF
from rdflib.namespace import XSD,SKOS
from rdflib.term import URIRef
from config import Config
import urllib.parse

class Organisation:

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


    def create_triples(self,g):
        for i, row in self.df.iterrows():
            org_name = row['name']
            region_code = row['region']
            country = row['iso_country']
            wikilink = row['weblink']
            found_date = row["founded"]
            founded_by = row["founded_by"]

            instance_name = urllib.parse.quote(f"organisation-{org_name}")

            g.add((URIRef(Config.ai4dm_data + instance_name), RDF.type,URIRef(Config.ai4dm + "Organisation")))
            g.add((URIRef(Config.ai4dm_data + instance_name), SKOS.prefLabel, Literal(org_name,datatype=XSD.string)))
            g.add((URIRef(Config.ai4dm_data + instance_name), SKOS.hiddenLabel,Literal(org_name, datatype=XSD.string)))

            if region_code is not None and isinstance(region_code,str):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasRegion"),
                       URIRef(Config.ai4dm_data +"region-"+region_code)))

            if country is not None and isinstance(country,str):
                if isinstance(country,float):
                    country = "NA"
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasCountry"),
                         URIRef(Config.ai4dm_data + "country-"+country)))

            if found_date is not None and isinstance(found_date,(str)):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "foundedDate"),
                       Literal(found_date,datatype=XSD.date)))

            if founded_by is not None and isinstance(founded_by,str):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "foundedBy"),
                       URIRef(Config.ai4dm_data +"" +urllib.parse.quote("person-" + founded_by))))


            if wikilink is not None and isinstance(wikilink,str):
                g.add((URIRef(Config.ai4dm_data + instance_name), URIRef(Config.ai4dm + "hasWikiLink"),
                       Literal(wikilink,datatype=XSD.anyURI)))



        return g




