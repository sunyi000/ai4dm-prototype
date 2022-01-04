from aircraft import Aircraft
from flight import Flight
from region import Region
from runway import Runway
from country import Country
from organisation import Organisation
from event import Event
from person import Person
from institution import Institution
from airport import Airport
from airline import Airline

from helper import extract_part,append_triple
from config import Config
from rdflib import Graph, RDF
from rdflib.namespace import OWL
from rdflib.term import URIRef
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph

# def append_triple(g):
#     with open("ai4dm-triples.txt", "a",encoding="utf-8") as f:
#         for s,p,o in g:
#             if (extract_part(p) in Config.preds) and (extract_part(s).isascii() and extract_part(o).isascii()):
#                 f.write(extract_part(s) + "\t" + extract_part(p) + "\t" + extract_part(o) + "\n")

def bind_ns(g,t):
    g.bind("cv-ai4dm", Config.cv_ai4dm)
    g.bind("skos", Config.skos)
    g.bind("xsd", Config.xsd)
    g.bind("owl", Config.owl)
    g.bind("rdf", Config.rdf)
    g.bind("rdfs", Config.rdfs)
    g.bind("ai4dm", Config.ai4dm)
    g.bind("cv", Config.cv)
    g.bind("ai4dm-data", Config.ai4dm_data)

    g.add((URIRef(Config.ai4dm_data + t), RDF.type, OWL.Ontology))
    g.add((URIRef(Config.ai4dm_data + t), OWL.imports, URIRef(Config.cv_ai4dm)))

    return g

def create_aircraft_data():
    g = Graph()
    g= bind_ns(g,"aircraft-data")
    acv = Aircraft(Config.AIRCRAFT, g)
    g = acv.create_triples(g)

    # g.serialize("aircraft-data.ttl",format='turtle')
    append_triple(g)

def create_flight_data():
    g = Graph()
    g= bind_ns(g,"flights-data")

    acv = Flight(g,Config.FLIGHT)
    g = acv.create_triples(g)

    # g.serialize("flights-data.ttl",format='turtle')
    append_triple(g)

def create_event_data():
    g = Graph()
    g= bind_ns(g,"events-data")

    acv = Event(g,Config.EVENT)
    g = acv.create_triples(g)
    # g.serialize("events-data.ttl",format='turtle')

    append_triple(g)



def create_region_data():
    g = Graph()
    g= bind_ns(g,"regions-data")

    acv = Region(g,Config.REGION)
    g = acv.create_triples(g)

    # g.serialize("region-data.ttl",format='turtle')
    append_triple(g)

def create_country_data():
    # countries
    g = Graph()
    g = bind_ns(g,"countries-data")
    re = Country(g,Config.COUNTRY)
    g = re.create_triples(g)
    # g.serialize("countries-data.ttl",format='turtle')
    append_triple(g)

def create_organisation_data():
    # # organisation
    g = Graph()
    g=bind_ns(g,"organisation-data")

    org = Organisation(g,Config.ORGANISATION)
    g = org.create_triples(g)
    # g.serialize("organisation-data.ttl",format='turtle')
    append_triple(g)

def create_person_data():
    #person
    g = Graph()
    g = bind_ns(g,"person-data")


    p = Person(g,Config.PERSON)
    g = p.create_triples(g)
    # g.serialize("person-data.ttl",format='turtle')
    append_triple(g)

def create_institution_data():
    # Institution
    g = Graph()
    g = bind_ns(g,"institution-data")

    ins = Institution(g,Config.INSTITUTION)
    g = ins.create_triples(g)
    # g.serialize("institution-data.ttl",format='turtle')
    append_triple(g)

def create_runway_data():
    # runway
    g = Graph()
    g = bind_ns(g,"runway-data")
    runway = Runway(g,Config.RUNWAY)
    g = runway.create_triples(g)
    # g.serialize("runway-data.ttl",format='turtle')
    append_triple(g)

def create_airport_data():
    # airport
    g = Graph()
    g = bind_ns(g,"airport-data")

    airport = Airport(g,Config.AIRPORT)
    g = airport.create_triples(g)
    g.serialize("airport-data.ttl",format='turtle')
    # append_triple(g)

def create_airline_data():
    # airline
    g = Graph()
    g = bind_ns(g,"airline-data")

    airline = Airline(g,Config.AIRLINE)
    g = airline.create_triples(g)
    # g.serialize("airline-data.ttl",format='turtle')
    append_triple(g)

if __name__ == '__main__':
    # g = Graph()
    # acv = Aircraft(Config.AIRCRAFT,g)
    #
    # acv.generate_cv('wingtip')
    # acv.generate_cv('model')
    # acv.generate_cv('manufacturer')
    # acv.generate_cv('physical_class')
    # acv.generate_cv('gear_config')
    # acv.generate_cv('wake_category')


    # create_aircraft_data()
    # create_flight_data()
    # create_event_data()
    # create_region_data()
    # create_country_data()
    create_organisation_data()
    # create_person_data()
    # create_institution_data()
    # create_airport_data()
    # create_runway_data()
    # create_airline_data()

