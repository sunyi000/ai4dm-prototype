import logging
import pickle
import pprint

import flask
from flask import Flask, request
from flask_cors import CORS, cross_origin
import os
from SPARQLWrapper import SPARQLWrapper,JSON
import helper
from helper import *
import subprocess
from subprocess import PIPE
from etl.aircraft import Aircraft
from etl.flight import Flight
from etl.region import Region
from etl.runway import Runway
from etl.country import Country
from etl.organisation import Organisation
from etl.event import Event
from etl.person import Person
from etl.institution import Institution
from etl.airport import Airport
from etl.airline import Airline

from config import Config
from rdflib import Graph, RDF
from rdflib.namespace import OWL
from rdflib.term import URIRef

import queries.queries as queries
import requests

app = Flask(__name__)

CORS(app)


def get_rule_pred():
    r = []
    df = helper.load_rules()
    for i, val in df['rule'].items():
        p = val.split("<=")[0]
        p=p.split("(")[0]
        r.append(p)

    return list(set(r))

rule_pred = get_rule_pred()

@app.route("/ai4dm/api/airports")
@app.route("/ai4dm/api/airports/<page>")
def get_airports(page=-1):
    results = queries.get_all_airports(page)
    return results_in_json(results["results"]["bindings"])


@app.route("/ai4dm/api/questions/airport/<type>")
def get_airport_predicate_by_airport(type):
    # rule_pred = get_rule_pred()

    if (type=="obj"):
        results = queries.get_airport_predicate_by_airport_asobject()
    else:
        results = queries.get_airport_predicate_by_airport()

    results = [s for s in results["results"]["bindings"] if s["pred"]["value"] in rule_pred ]
    return results_in_json(results)




@app.route("/ai4dm/api/facts/<subj>/<pred>/<t>")
def get_facts(subj,pred,t):
    if t =="subj":
        results = queries.get_facts(subj,pred)
    else:
        results = queries.get_facts_obj(subj,pred)
    return results_in_json(results["results"]["bindings"])


@app.route("/ai4dm/api/prediction/<subj>/<pred>/<t>")
def get_prediction(subj,pred,t):
    df = helper.load_rules()
    df_col = df[df['rule'].str.startswith(pred)]

    fpath="C://Users/ysun/Documents/griffith/ai4dm/anyburl/data/last_score.pkl"
    if(os.path.exists(fpath)):
        f = open(fpath,"rb")
        df_last_score = pd.read_pickle(f)
        f.close()
    else:
        f = open(fpath,"wb")
        df_last_score=df
        pickle.dump(df,f)
        f.close()

    results =[]
    for index,row in df_col.iterrows():
        rule = row['rule'].split("<=")[1]
        p = row['rule'].split("<=")[0]
        if t=="subj":
            tr=queries.get_prediction(subj,rule,p)
        else:
            tr = queries.get_prediction_obj(subj,rule)
        r=tr["results"]["bindings"]
        for item in r:
            item["score"] ={"value":row["score"]}
            item["rule"] = {"value":row["rule"]}
            item["last_score"]={'value':df_last_score.iloc[list(df_last_score['rule'].values).index(row['rule'])]['score']}

        if len(r)>0:
            results.append(r)
    results = [item for sublist in results for item in sublist]

    results = helper.sorted_uniq(results)

    return results_in_json(results)

@app.route("/ai4dm/api/runway/<id>")
def get_runway_by_id(id):
    results = queries.get_runway_by_id(id)
    return results_in_json(results["results"]["bindings"])


@app.route("/ai4dm/api/region/<id>")
def get_region_by_id(id):
    results = queries.get_region_by_id(id)
    return results_in_json(results["results"]["bindings"])

@app.route("/ai4dm/api/country/<id>")
def get_country_by_id(id):
    results = queries.get_country_by_id(id)
    return results_in_json(results["results"]["bindings"])


@app.route("/ai4dm/api/institution/<id>")
def get_institution_by_id(id):
    results = queries.get_institution_by_id(id)
    return results_in_json(results["results"]["bindings"])


@app.route("/ai4dm/api/events/<id>")
def get_event_by_id(id):
    results = queries.get_event_by_id(id)
    return results_in_json(results["results"]["bindings"])


@app.route("/ai4dm/api/orgs/<id>")
@app.route("/ai4dm/api/orgs/")
def get_org(id=-1):
    if id==-1:
        results = queries.get_all_organisations()
    else:
        results = queries.get_org_by_id(id)

    return results_in_json(results["results"]["bindings"])


@app.route("/ai4dm/api/persons/<id>")
@app.route("/ai4dm/api/persons/")
def get_persons(id=-1):
    if id==-1:
        results = queries.get_all_persons()
    else:
        results = queries.get_person_by_id(id)

    return results_in_json(results["results"]["bindings"])

@app.route("/ai4dm/api/questions/persons/<type>")
def get_persons_predicate(type):
    if (type=="obj"):
        results = queries.get_persons_predicate_asobject()
    else:
        results = queries.get_persons_predicate_assubject()

    results = [s for s in results["results"]["bindings"] if s["pred"]["value"] in rule_pred ]
    return results_in_json(results)


@app.route("/ai4dm/api/aircraft/<id>")
@app.route("/ai4dm/api/aircraft/")
def get_aircraft(id=-1):
    if id==-1:
        results = queries.get_all_aircrafts()
    else:
        results = queries.get_aircraft_by_id(id)
    return results_in_json(results["results"]["bindings"])

@app.route("/ai4dm/api/airlines/<id>")
@app.route("/ai4dm/api/airlines/")
def get_airlines(id=-1):
    if id==-1:
        results = queries.get_all_airlines()
    else:
        results = queries.get_airline_by_id(id)
    return results_in_json(results["results"]["bindings"])

@app.route("/ai4dm/api/events/<id>")
@app.route("/ai4dm/api/events/")
def get_events(id=-1):
    if id==-1:
        results = queries.get_all_events()
    else:
        results = queries.get_event_by_id(id)
    return results_in_json(results["results"]["bindings"])


@app.route("/ai4dm/api/questions/events/")
def get_event_predicate():
    results = queries.get_event_predicate_assubject()

    results = [s for s in results["results"]["bindings"] if s["pred"]["value"] in rule_pred ]
    return results_in_json(results)


@app.route("/ai4dm/api/questions/aircraft/<type>")
def get_aircraft_predicate(type):
    # rule_pred = get_rule_pred()

    if (type=="obj"):
        results = queries.get_aircraft_predicate_asobject()
    else:
        results = queries.get_aircraft_predicate_assubject()

    results = [s for s in results["results"]["bindings"] if s["pred"]["value"] in rule_pred ]
    return results_in_json(results)

@app.route("/ai4dm/api/questions/airlines/<type>")
def get_airline_predicate(type):
    if (type=="obj"):
        results = queries.get_airline_predicate_asobject()
    else:
        results = queries.get_airline_predicate_assubject()

    results = [s for s in results["results"]["bindings"] if s["pred"]["value"] in rule_pred ]
    return results_in_json(results)


@app.route("/ai4dm/api/flights/<id>")
@app.route("/ai4dm/api/flights/")
def get_flights(id=-1):
    if id==-1:
        results = queries.get_all_flights()
    else:
        results = queries.get_flight_by_id(id)
    return results_in_json(results["results"]["bindings"])

@app.route("/ai4dm/api/questions/flights/<type>")
def get_flight_predicate(type):
    if (type=="obj"):
        results = queries.get_flight_predicate_asobject()
    else:
        results = queries.get_flight_predicate_assubject()

    results = [s for s in results["results"]["bindings"] if s["pred"]["value"] in rule_pred ]
    return results_in_json(results)

@app.route("/ai4dm/api/questions/orgs/<type>")
def get_org_predicate(type):
    if (type=="obj"):
        results = queries.get_org_predicate_asobject()
    else:
        results = queries.get_org_predicate_assubject()

    results = [s for s in results["results"]["bindings"] if s["pred"]["value"] in rule_pred ]
    return results_in_json(results)




@app.route("/ai4dm/api/upload/",methods=["POST"])
@cross_origin(origin='*', headers=['accept','Content-Type'])
def upload_file():
    file = request.files['fileKey']
    print(file.filename)
    ds = request.form['datasource']
    cat = request.form['category']
    if ds=="FAA":
        if cat =="Runway":
            g = Graph()
            g = bind_ns(g, "runway-data")
            runway = Runway(g, file)
            g = runway.create_triples(g)
            #post to graphdb
            r=do_post_to_gdb(g,'runway-data')


        elif cat =="Aircraft":
            g = Graph()
            g = bind_ns(g, "aircraft-data")
            ac = Aircraft(g, file)
            g = ac.create_triples(g)
            #post to graphdb
            r=do_post_to_gdb(g,'aircraft-data')
        #
        # elif cat=="Airport":
        # elif cat=="Flight":
        # elif cat =="Incident":
        # elif cat=="Person":
        # elif cat=="Organisation":
        # elif cat=="Institution":
    #
    # elif ds=="OurAirports":
    #     print("ourairports")
    # elif ds == "OurFlights":
    #     print("ourflights")

    if r.response.code == 204:
        print("new data posted to graphdb")
        helper.append_triple(g)
        output = retrain_anyburl()
        # re-run anyburl to train
        if output =="":
            status = flask.Response(status=200)
        else:
            status = flask.Response(status=500)
    else:
        logging.error("new data failed to post to graphdb", r.status_code, r.content)
        status = flask.Response(status=r.status_code)


    # status = flask.Response(status=200)
    return status


def do_post_to_gdb(g,t):
    query = f"""INSERT DATA {{ GRAPH <http://dbpedia.org/ontology/data/ai4dm/{t}>
            {{"""

    for s,p,o in g:
        print(s,p,o)
        if o.startswith("http"):
            o=f"""<{o}>"""
        elif type(o.value) is str:
            o=f"""'{o}'"""

        query+=f"""<{s}> <{p}> {o} ."""
        
    query +=f""" }} }}"""
    sparql = SPARQLWrapper(queries.QUERY_URL+'/statements')
    sparql.method = 'POST'
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    r = sparql.query()

    return r

def retrain_anyburl():
    os.chdir("C://Users/ysun/Documents/griffith/ai4dm/anyburl")
    command = ['java','-Xmx3G','-cp','AnyBURL-JUNO.jar','de.unima.ki.anyburl.LearnReinforced','config-learn.properties']
    result = subprocess.run(command, stdout=PIPE,stderr=PIPE, universal_newlines=True)

    print(result.returncode, result.stdout, result.stderr)
    return result.stderr

if __name__ == '__main__':
    app.run(debug=True)

