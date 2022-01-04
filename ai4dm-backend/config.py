import os
from rdflib import Namespace

class Config:

    TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'view')

    STATIC_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')


    img_ext = ['.jpg','.png','.svg','.jpeg']

    unwanted_preds_path = "/data/predicates-unwanted.txt"


    cv = Namespace('http://dbpedia.org/ontology/cv/')
    cv_ai4dm = Namespace('http://dbpedia.org/ontology/cv/ai4dm/')
    dct = Namespace('http://purl.org/dc/terms/')
    owl = Namespace('http://www.w3.org/2002/07/owl#')
    rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    rdfs = Namespace('http://www.w3.org/2000/01/rdf-schema#')
    skos = Namespace('http://www.w3.org/2004/02/skos/core#')
    xsd = Namespace('http://www.w3.org/2001/XMLSchema#')
    ai4dm = Namespace('http://dbpedia.org/ontology/ai4dm/')
    ai4dm_data = Namespace('http://dbpedia.org/ontology/data/ai4dm/')
    foaf = Namespace('http://xmlns.com/foaf/0.1/')
    geo = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')

    preds = ["isAircraftOf","hasAircraftEvent","hasOrigin","hasDestination","hasAircraft","isFlightOf",
             "hasRegion","isAircraftEventOf","isSubsidaryOf","hasBase","targetAirport","hasAlliance","hasHeadquarter",
             "hasFocusRegion","foundedBy","hasCountry","regionServed","hasEmployer","hasBirthDate","isAlumniOf",
             "hasNationality","boardFlight","isRunwayOf","isRegionOf","capableOfLanding"]

    pred_map = {
        "http://www.w3.org/2003/01/geo/wgs84_pos#lat": "geo:lat",
        "http://www.w3.org/2003/01/geo/wgs84_pos#long": "geo:long",
        "dbp:airfield": "dbp:airport",
        "dbp:birthplace": "dbp:birthPlace",
        "dbp:elevationF": "dbp:elevation",
        "dbp:elevationFt": "dbp:elevation",
        "dbp:elevationM": "dbp:elevation",
        "dbp:faa": "dbp:faaIdentifier",
        "dbp:foundation":"dbp:founded",
        "dbp:founders":"dbp:founder",
        "dbp:foundingDate":"dbp:founded",
        "dbp:foundingYear":"dbp:founded",
        "dbp:date":"dbp:founded",
        "dbp:built":"dbp:founded",
        "dbp:h1LengthF":"dbp:h1Length",
        "dbp:h1LengthM": "dbp:h1Length",
        "dbp:h2LengthF": "dbp:h2Length",
        "dbp:h2LengthM":"dbp:h2Length",
        "dbp:hubs":"dbp:hub",
        "dbp:hubAirport":"dbp:hub",
        "dbp:lastStopover":"dbp:stopover",
        "dbp:city":"dbp:cityServed",
        "dbp:subsid":"dbp:subsidiary",
        "dbp:subsidiaries":"dbp:subsidiary",
        "dbp:sites":"dbp:site",
        "dbp:region": "dbp:regionServed",
        "dbp:parent":"dbp:parentCompany",
        "dbp:opened":"dbp:open",
        "dbp:openingDate":"dbp:open",
        "dbp:locationCountry":"dbp:location",
        "dbp:locations":"dbp:location",
        "dbp:address":"dbp:location",
        "dbp:keyPerson":"dbp:keyPeople",
        "dbp:profit":"dbp:revenue",
        "dbp:workplaces":"dbp:employer",
        "dbp:r1LengthF":"dbp:r1Length",
        "dbp:r1LengthM": "dbp:r1Length",
        "dbp:r2LengthF": "dbp:r2Length",
        "dbp:r2LengthM": "dbp:r2Length",
        "dbp:r3LengthF": "dbp:r3Length",
        "dbp:r3LengthM": "dbp:r3Length",
        "dbp:r4LengthF": "dbp:r4Length",
        "dbp:r4LengthM": "dbp:r4Length",
        "dbp:product":"dbp:subsidiary",
        "dbp:numberOfEmployees":"dbp:numEmployees",
        "dbp:operatingIncome":"dbp:netIncome",
        "dbp:beganOperation":"dbp:commenced",
        "dbp:closed":"dbp:closingDate",
        "dbp:ceased":"dbp:closingDate",
        "dbp:destinations":"dbp:destination",
        "dbp:faaLocationIdentifier":"dbp:faaIdentifier",
        "dbp:focusCities":"dbp:focusCity",
        "dbp:founder": "dbp:foundedBy",
        "dbp:founderName":"dbp:foundedBy",
        "dbp:currentowner":"dbp:owner",
        "dbp:used":"dbp:founded",
        "dbp:revenue":"dbp:netIncome",
        "dbp:formationDate":"dbp:founded",
        "dbp:institution":"dbp:education"

    }


    ns_mapping = {
        "dbo": 'http://dbpedia.org/ontology/',
        'dbr': 'http://dbpedia.org/resource/',
        'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
        'dbp': 'http://dbpedia.org/property/',
        'foaf': 'http://xmlns.com/foaf/0.1/',
        'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#',
        'xsd': 'http://www.w3.org/2001/XMLSchema#',
        'georss': 'http://www.georss.org/georss/'

    }



