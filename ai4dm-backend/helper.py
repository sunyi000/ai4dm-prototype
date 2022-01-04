from flask import jsonify
import pandas as pd
from config import Config
import csv
from rdflib.namespace import OWL
from rdflib.term import URIRef

from rdflib import Graph, RDF

def results_in_json(results):

    json_result = jsonify(results)
    return json_result

def append_triple(g):
    with open("C://Users/ysun/Documents/griffith/ai4dm/anyburl/data/ai4dm-triples-train.txt", "a",encoding="utf-8") as f:
        for s,p,o in g:
            if (extract_part(p) in Config.preds) and (extract_part(s).isascii() and extract_part(o).isascii()):
                f.write(extract_part(s) + "\t" + extract_part(p) + "\t" + extract_part(o) + "\n")

def sorted_uniq(r):
    r_sorted = sorted(r, key=lambda x: (x["obj"]["value"], -float(x["score"]["value"])))
    sorted_ids = [x["obj"]["value"] for x in r_sorted]
    return [r_sorted[sorted_ids.index(_id)] for _id in set(sorted_ids)]

def load_rules():
    rule_file = "C://Users/ysun/Documents/griffith/ai4dm/anyburl/rules/alpha-100"

    df = pd.read_csv(rule_file, delimiter="\t", names=['n1', 'n2', 'score', 'rule'])

    return df

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
    g.add((URIRef(Config.ai4dm_data + t), OWL.imports, URIRef('http://www.w3.org/2004/02/skos/core')))

    return g

def roundLatLong(results):
    for r in results:
        if (checkKey(r,"latitude")):
            r["latitude"]["value"] = round(float(r["latitude"]["value"]),2)
        if (checkKey(r,"longitude")):
            r["longitude"]["value"] = round(float(r["longitude"]["value"]), 2)

    return results


def checkKey(dict, key):
    if key in dict.keys():
        return True
    else:
        return False


def extract_part(uri):
    p = uri.split("/")[-1]

    if p.find("#") !=-1:
        return p.split("#")[-1]
    else:
        return uri.split("/")[-1]