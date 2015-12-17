#!/usr/bin/env python


#from py2neo import Graph
from django.http.response import HttpResponse
from django.utils import simplejson

NEO_URL = "http://174.129.230.61:7474/db/data/"
#graph = Graph(NEO_URL)

#@get("/graph")
def get_graph(request):
    #results = graph.cypher.execute(
    #    "MATCH (m:MetaNode)<-[:measured_by]-(a:Person) "
    #    "RETURN m.title as movie, collect(a.name) as cast "
    #    "LIMIT {limit}", {"limit": 100})
    results = []
    nodes = []
    rels = []
    i = 0
    for movie, cast in results:
        nodes.append({"title": movie, "label": "movie"})
        target = i
        i += 1
        for name in cast:
            actor = {"title": name, "label": "actor"}
            try:
                source = nodes.index(actor)
            except ValueError:
                nodes.append(actor)
                source = i
                i += 1
            rels.append({"source": source, "target": target})
    return HttpResponse(simplejson.dumps({"nodes": nodes, "links": rels}), mimetype="application/json")

