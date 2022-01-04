import pickle

from queries.prefix import *
import requests
from urllib.parse import unquote,quote
from helper import *
import os

from SPARQLWrapper import SPARQLWrapper,JSON,CSV

QUERY_URL = "http://localhost:7200/repositories/ai4dm"


def sparql_result(query):
    sparql = SPARQLWrapper(QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    return result

# Get all airports
#
#
# return: json object contains all airport
#
def get_all_airports(page):
    offset = int(page) * 10
    query = f"""{get_prefixes()} 
        select distinct (strafter(str(?a),str(ai4dm-data:)) as ?Airport)  (ROUND(?lat*1000)/1000 AS ?Latitude)  
        (ROUND(?long*1000)/1000 AS ?Longitude) (strafter(str(?t),str(cv-ai4dm:))as ?Type) 
        (strafter(str(?c),str(ai4dm-data:))as ?Country) ?Elevation ?GPS_Code ?Description 
        (strafter(str(?rs),str(ai4dm-data:))as ?Region_Served) ?Identifier ?Municipality ?IATA 
        (strafter(str(?rw),str(ai4dm-data:))as ?Runway)
        where {{ 
            ?a rdf:type ai4dm:Airport .
            ?a geo:lat ?lat .
            ?a geo:long ?long .
            ?a ai4dm:airportType ?t .
            ?a ai4dm:hasAirportIdent ?Identifier .
            ?a ai4dm:hasCountry ?c .
            ?c rdf:type ai4dm:Country .
            ?a ai4dm:hasElevation ?Elevation .
            ?a ai4dm:hasGPSCode ?GPS_Code .
            ?a dct:description ?Description .
            ?a ai4dm:regionServed ?rs .
            ?rs rdf:type ai4dm:Region .
            ?a ai4dm:hasMunicipality ?Municipality .
            ?a ai4dm:hasFAAIdentifier ?IATA .
            ?rw ai4dm:isRunwayOf ?a .
            filter(?IATA != "") .
            filter(?t !=cv-ai4dm:closed) .
        }}
        # limit 200 
            
            """

    result = sparql_result(query)
    return result





# get airport related predicates, including runway. airport as subject
def get_airport_predicate_by_airport():
    query = f"""{get_prefixes()}
        select distinct (strafter(str(?p),str(ai4dm:)) as ?pred ) 
        where {{
            {{
                ?a rdf:type ai4dm:Airport .
                ?a ?p ?d .
            }}
                union
            {{
                ?rw rdf:type ai4dm:Runway .
                ?rw ai4dm:isRunwayOf ?a .
                ?rw ?p ?s .
            }}
            filter(?pred !="")
        }}

    """
    result = sparql_result(query)
    return result

def get_airport_predicate_by_airport_asobject():
    query = f"""{get_prefixes()}
        select distinct (strafter(str(?p),str(ai4dm:)) as ?pred ) 
        where {{
                ?a rdf:type ai4dm:Airport .
                ?s ?p ?a .
        }}

    """
    result = sparql_result(query)
    return result

def get_facts(subj,pred):
    if pred =="capableOfLanding":
        query = f""" {get_prefixes()}
                select distinct (strafter(str(?o),str(ai4dm-data:))as ?obj) 
                where {{
                        ?x rdf:type ai4dm:Runway .
                        ?x ai4dm:isRunwayOf ai4dm-data:{subj} .
                        ?x ai4dm:{pred} ?o .
                      }}    
                """
    else:
        query = f""" {get_prefixes()}
                select distinct (strafter(str(?o),str(ai4dm-data:))as ?obj)
                where {{
                    ai4dm-data:{subj} ai4dm:{pred} ?o .
                }}    
        """

    result = sparql_result(query)
    return result

def get_prediction(sub,rule,p):

    if p.startswith("capableOfLanding"):
        query = f"""{get_prefixes()}
                 select distinct (strafter(str(?Y),str(ai4dm-data:))as ?obj) 
                 where {{ ?X ai4dm:isRunwayOf ai4dm-data:{sub} ."""
    else:
        query = f"""{get_prefixes()}
                 select distinct (strafter(str(?Y),str(ai4dm-data:))as ?obj) 
                 where {{        """

    rules = rule.split(", ")
    for r in rules:
        pred = r.split("(")[0].strip()
        subj = r.split("(")[1].split(",")[0].strip()
        obj = r.split("(")[1].split(",")[1][:-1].strip()

        if subj =="X":
            if p.startswith("capableOfLanding"):
                q = f"""?{subj} ai4dm:{pred} ?{obj} . """
            else:
                q= f"""ai4dm-data:{sub} ai4dm:{pred} ?{obj} . """

        elif obj =="X":
            if p.startswith("capableOfLanding"):
                q = f"""?{subj} ai4dm:{pred} ?{obj} . """
            else:
                q = f"""?{subj} ai4dm:{pred} ai4dm-data:{sub} . """
        else:
            q = f"""?{subj} ai4dm:{pred} ?{obj} . """

        query += q

    query+="}"

    result = sparql_result(query)
    return result

def get_facts_obj(obj,pred):
    query = f""" {get_prefixes()}
                select distinct (strafter(str(?ob),str(ai4dm-data:)) as ?obj) 
                where {{
                    ?ob ai4dm:{pred} ai4dm-data:{obj} .
                }}   
    """

    result = sparql_result(query)
    return result

def get_prediction_obj(ob,rule):

    query = f"""{get_prefixes()}
                 select distinct (strafter(str(?X),str(ai4dm-data:))as ?obj) 
                 where {{        """

    rules = rule.split(", ")
    for r in rules:
        pred = r.split("(")[0].strip()
        subj = r.split("(")[1].split(",")[0].strip()
        obj = r.split("(")[1].split(",")[1][:-1].strip()
        if subj == "Y":
            q = f"""ai4dm-data:{ob} ai4dm:{pred} ?{obj} . """
        elif obj == "Y":
            q = f"""?{subj} ai4dm:{pred} ai4dm-data:{ob} . """
        else:
            q = f"""?{subj} ai4dm:{pred} ?{obj} . """
        query += q

    query+="}"

    result = sparql_result(query)
    return result

def get_runway_by_id(id):
    query = f"""{get_prefixes()}
        select distinct ?lighted (strafter(str(?sf),str(cv-ai4dm:))as ?surface)  ?width 
        (group_concat(strafter(str(?ac),str(ai4dm-data:));separator=",") as ?aircraft) 
        (strafter(str(?ap),str(ai4dm-data:))as ?airport) 
        where {{
                ?a rdf:type ai4dm:Runway .
                optional {{?a ai4dm:hasLighted ?lighted .}}
                optional {{?a ai4dm:hasRunwayLength ?length .}}
                optional {{?a ai4dm:hasSurface ?sf .}}
                optional {{?a ai4dm:hasWidth ?width .}}
                optional {{?a ai4dm:capableOfLanding ?ac .}}
                optional {{?a ai4dm:isRunwayOf ?ap .}}
                filter(?a=ai4dm-data:{id})
        }}
        group by ?lighted ?sf ?width ?ap
    """
    result = sparql_result(query)
    return result


def get_region_by_id(id):
    query = f"""{get_prefixes()}
        select   distinct  (strafter(str(?a),str(ai4dm-data:)) as ?region) (strafter(str(?c),str(ai4dm-data:)) as ?country) (strafter(str(?rc),str(cv-ai4dm:)) as ?region_code) ?wk (strafter(str(?con),str(cv-ai4dm:)) as ?continent)
        where {{
        ?a a ai4dm:Region .
        ?a ai4dm:isRegionOf ?c .
        ?c a ai4dm:Country .
        ?a ai4dm:hasRegionCode ?rc .
        ?a ai4dm:hasWikiLink ?wk .
        ?a ai4dm:hasContinent ?con .
        filter(?a=ai4dm-data:{id})
    }}
    """
    result = sparql_result(query)
    return result

def get_country_by_id(id):
    query = f"""{get_prefixes()}
        select  distinct  (strafter(str(?a),str(ai4dm-data:)) as ?country) (strafter(str(?rc),str(cv-ai4dm:)) as ?country_code) ?wk (strafter(str(?con),str(cv-ai4dm:)) as ?continent)
        where {{
        ?a a ai4dm:Country .
        ?a ai4dm:hasCountryCode ?rc .
        ?a ai4dm:hasWikiLink ?wk .
        ?a ai4dm:hasContinent ?con .     
        filter(?a=ai4dm-data:{id})
    }}
    """
    result = sparql_result(query)
    return result


def get_institution_by_id(id):
    query = f"""{get_prefixes()}
        select	distinct  (strafter(str(?a),str(ai4dm-data:)) as ?institution) ?label (strafter(str(?r),str(ai4dm-data:)) as ?region) (strafter(str(?t),str(ai4dm-data:)) as ?type) ?a
        where {{
            ?a a ai4dm:Institution .    
            ?a skos:prefLabel ?label .
            ?a ai4dm:hasRegion ?r .
            ?a ai4dm:hasInstitutionType ?t
           filter(?a=ai4dm-data:{quote(id)})
        }}
    """
    result = sparql_result(query)
    return result

def get_aircraft_by_id(id):
    query = f"""{get_prefixes()}
        select distinct ?model (strafter(str(?manu),str(cv-ai4dm:)) as ?manufacturer) (strafter(str(?wt),str(cv-ai4dm:)) as ?wingtip) 
        ?engine_count ?approach_speed ?wing_span ?length ?tail_height ?mtow ?max_ramp 
        ?icao_code (strafter(str(?gc),str(cv-ai4dm:)) as ?gear_config) (strafter(str(?wc),str(cv-ai4dm:)) as ?wake_category) 
        ?parking_area (strafter(str(?pc),str(cv-ai4dm:)) as ?physical_class)
        where {{
            ?a rdf:type ai4dm:Aircraft .
            optional {{ ?a ai4dm:aircraftModel ?model .}}
            optional {{ ?a ai4dm:hasManufacturer ?manu .}}
            optional {{ ?a ai4dm:hasWingtip ?wt .}}
            optional {{ ?a ai4dm:hasEngineCount ?engine_count .}}
            optional {{ ?a ai4dm:hasApproachSpeed ?approach_speed .}}
            optional {{ ?a ai4dm:hasWingSpan ?wing_span .}}
            optional {{ ?a ai4dm:hasAircraftLength ?length .}}
            optional {{ ?a ai4dm:hasTailHeight ?tail_height .}}
            optional {{ ?a ai4dm:hasMTOW ?mtow .}}
            optional {{ ?a ai4dm:hasMaxRamp ?max_ramp .}}
            optional {{ ?a ai4dm:hasGearConfig ?gc .}}
            optional {{ ?a ai4dm:hasIcaoCode ?icao_code .}}
            optional {{ ?a ai4dm:hasWakeCategory ?wc .}}
            optional {{ ?a ai4dm:hasParkingArea ?parking_area .}}
            optional {{ ?a ai4dm:hasPhysicalClass ?pc .}}
            filter(?a=ai4dm-data:{id})
        }}

    """
    result = sparql_result(query)
    return result

def get_all_aircrafts():
    query = f"""{get_prefixes()}
        select distinct (strafter(str(?a),str(ai4dm-data:)) as ?aircrafts) 
        where {{
            ?a rdf:type ai4dm:Aircraft .
        }}

    """
    result = sparql_result(query)
    return result

def get_aircraft_predicate_assubject():
    query = f"""{get_prefixes()}
        select distinct (strafter(str(?p),str(ai4dm:)) as ?pred )
            where {{
                ?a rdf:type ai4dm:Aircraft .
                ?a ?p ?d .
			    ?d rdf:type ai4dm:Airline .
	            filter(?pred !="")
                }}
        """
    result = sparql_result(query)
    return result

def get_aircraft_predicate_asobject():
    query = f"""{get_prefixes()}
        select distinct (strafter(str(?p),str(ai4dm:)) as ?pred )
            where {{
                ?d rdf:type ai4dm:Aircraft .
                ?a ?p ?d .
                filter(?pred !="")
                }}

    """
    result = sparql_result(query)
    return result


def get_all_airlines():
    query = f"""{get_prefixes()}
        select distinct (strafter(str(?a),str(ai4dm-data:)) as ?airlines) 
        where {{
            ?a rdf:type ai4dm:Airline .
        }}

    """
    result = sparql_result(query)
    return result


def get_airline_predicate_assubject():
    query = f"""{get_prefixes()}
        select distinct (strafter(str(?p),str(ai4dm:)) as ?pred ) 
        where {{
            ?a rdf:type ai4dm:Airline .
            ?a ?p ?d .
            {{
                ?d rdf:type ai4dm:Airport .
            }}union
            {{
                ?d rdf:type ai4dm:Airline .
            }}union
            {{
                ?d rdf:type ai4dm:Region .
            }}union
            {{
                ?d rdf:type ai4dm:Organisation .
            }}union
            {{
                ?d rdf:type ai4dm:Person .
            }}
        }}
        """
    result = sparql_result(query)
    return result

def get_airline_predicate_asobject():
    query = f"""{get_prefixes()}
        select distinct (strafter(str(?p),str(ai4dm:)) as ?pred )
            where {{
                ?d rdf:type ai4dm:Airline .
                ?a ?p ?d .
                filter(?pred !="")
                }}

    """
    result = sparql_result(query)
    return result

def get_airline_by_id(id):
    query = f"""{get_prefixes()}
            select distinct (strafter(str(?al),str(ai4dm-data:)) as ?airline ) ?al ?callsign ?foundedDate ?netIncome 
            ?fleetSize ?icaoCode ?description (strafter(str(?c),str(ai4dm-data:)) as ?country )
            where {{
                ?al rdf:type ai4dm:Airline .
                ?al ai4dm:hasCallsign ?callsign .
                ?al ai4dm:foundedDate ?foundedDate .
                ?al ai4dm:netIncome ?netIncome .
                ?al ai4dm:hasFleetSize ?fleetSize .
                ?al ai4dm:hasIcaoCode ?icaoCode .
                ?al dct:description ?description .
                ?al ai4dm:hasCountry ?c .
                filter(?al=ai4dm-data:{id})
            }}
            """
    result = sparql_result(query)
    return result

def get_all_flights():
    query = f"""{get_prefixes()}
        select distinct (strafter(str(?al),str(ai4dm-data:)) as ?flight )
        where{{
            ?al rdf:type ai4dm:Flight .
        }}
    
        """
    result = sparql_result(query)

    return result

def get_flight_by_id(id):
    query = f"""{get_prefixes()}
            select distinct (strafter(str(?al),str(ai4dm-data:)) as ?flight )  ?flight_no (strafter(str(?ft),str(cv-ai4dm:)) as ?flight_type ) ?stops
            where {{
                ?al rdf:type ai4dm:Flight .
                ?al ai4dm:hasFlightNo ?flight_no .
                ?al ai4dm:hasFlightType ?ft .
                ?al ai4dm:hasStops ?stops .
                filter(?al=ai4dm-data:{id})
            }}
            """
    result = sparql_result(query)
    return result


def get_flight_predicate_assubject():
    query = f"""{get_prefixes()}
        select distinct (strafter(str(?p),str(ai4dm:)) as ?pred )
        where {{
            ?a rdf:type ai4dm:Flight .
            ?a ?p ?d .
            {{
                ?d rdf:type ai4dm:Airport .
            }}union
            {{
                ?d rdf:type ai4dm:Airline .
            }}union
            {{
                ?d a ai4dm:Aircraft .
            }}  
        }}
        """
    result = sparql_result(query)
    return result

def get_flight_predicate_asobject():
    query = f"""{get_prefixes()}
        select distinct (strafter(str(?p),str(ai4dm:)) as ?pred )
            where {{
                ?d rdf:type ai4dm:Flight .
                ?a ?p ?d .
                filter(?pred !="")
                }}

    """
    result = sparql_result(query)
    return result


def get_all_events():
    query = f"""{get_prefixes()}
        select distinct (strafter(str(?s),str(ai4dm-data:)) as ?event )
        where{{
            ?s a ai4dm:Event .
        }}
    """
    result = sparql_result(query)
    return result


def get_event_predicate_assubject():
    query = f"""{get_prefixes()}
        select distinct ?pred
        where{{
            ?s a ai4dm:Event .
            ?s ?pred ?o .
            filter(STRSTARTS(STR(?p), "http://dbpedia.org/ontology/ai4dm/"))
        }}
    """
    result = sparql_result(query)
    return result


def get_event_by_id(id):
    query = f"""{get_prefixes()}
        select distinct (strafter(str(?al),str(ai4dm-data:)) as ?event ) ?name 
        (strafter(str(?r),str(ai4dm-data:)) as ?region ) ?label ?description ?date (strafter(str(?t),str(cv-ai4dm:)) as ?type )
        where{{
            ?al rdf:type ai4dm:Event .
            ?al ai4dm:hasEventID ?id .
            ?al ai4dm:eventName ?name  .
            optional{{?al ai4dm:hasEventType ?t .}}
            optional{{?al ai4dm:hasRegion ?r .}}
            optional{{?t skos:prefLabel ?label .}}
            optional{{?t skos:definition ?description .}}
            optional{{?al ai4dm:eventDate ?date .}}
            filter(?al = ai4dm-data:{id})
        }}
        """
    result = sparql_result(query)
    return result


def get_all_organisations():
    query = f"""{get_prefixes()}
        select distinct (strafter(str(?al),str(ai4dm-data:)) as ?organisation )
        where{{
            ?al rdf:type ai4dm:Organisation .
        }}

        """
    result = sparql_result(query)

    return result


def get_org_by_id(id):
    query = f"""{get_prefixes()}
        select distinct (strafter(str(?al),str(ai4dm-data:)) as ?org )  ?wk ?date
        where {{
            ?al rdf:type ai4dm:Organisation .
            optional {{?al ai4dm:hasWikiLink ?wk .}}
            optional {{?al ai4dm:foundedDate ?date .}}
            filter(?al=ai4dm-data:{quote(id)})
        }}
        """
    result = sparql_result(query)
    return result


def get_org_predicate_assubject():
    query = f"""{get_prefixes()}
        select distinct (strafter(str(?p),str(ai4dm:)) as ?pred )
        where {{
            ?a rdf:type ai4dm:Organisation .
            ?a ?p ?d .
            filter(?pred!="") 
        }}
        """
    result = sparql_result(query)
    return result


def get_org_predicate_asobject():
    query = f"""{get_prefixes()}
        select distinct (strafter(str(?p),str(ai4dm:)) as ?pred )
            where {{
                ?d rdf:type ai4dm:Organisation .
                ?a ?p ?d .
                filter(?pred !="")
                }}

    """
    result = sparql_result(query)
    return result




def get_all_persons():
    query = f"""{get_prefixes()}
        select distinct (strafter(str(?al),str(ai4dm-data:)) as ?person )
        where{{
            ?al rdf:type foaf:Person .
        }}

        """
    result = sparql_result(query)

    return result


def get_person_by_id(id):
    query = f"""{get_prefixes()}
       select distinct (strafter(str(?al),str(ai4dm-data:)) as ?person )  ?name
        where {{
            ?al rdf:type foaf:Person .
            ?al foaf:name ?name 
            filter(?al=ai4dm-data:{quote(id)})
        }}
        """
    result = sparql_result(query)
    return result


def get_persons_predicate_assubject():
    query = f"""{get_prefixes()}
        select distinct (strafter(str(?p),str(ai4dm:)) as ?pred )
        where {{
            ?a rdf:type foaf:Person .
            ?a ?p ?d .
            filter(?pred!="") 
        }}
        """
    result = sparql_result(query)
    return result


def get_persons_predicate_asobject():
    query = f"""{get_prefixes()}
        select distinct (strafter(str(?p),str(ai4dm:)) as ?pred )
        where {{
            ?a rdf:type foaf:Person .
            ?d ?p ?a .
            filter(?pred!="") 
        }}

    """
    result = sparql_result(query)
    return result