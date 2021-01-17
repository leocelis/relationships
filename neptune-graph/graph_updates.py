from __future__ import print_function  # Python 2/3 compatibility

import uuid

from gremlin_python import statics
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph
from tornado import httpclient

statics.load_statics(globals())
graph = Graph()

# connect to Neptune
my_req = httpclient.HTTPRequest('wss://localhost:8182/gremlin', validate_cert=False)

remoteConn = DriverRemoteConnection(my_req, 'g')
g = graph.traversal().withRemote(remoteConn)

# generate unique IDs
contact_1 = str(uuid.uuid1())
contact_2 = str(uuid.uuid1())
contact_3 = str(uuid.uuid1())
company_1 = str(uuid.uuid1())

# add vertices
g.addV('contact').property(id, contact_1).property('name', 'josh').property('age', 27).next()
g.addV('contact').property(id, contact_2).property('name', 'joe').property('age', 32).next()
g.addV('contact').property(id, contact_3).property('name', 'jean').property('age', 32).next()
g.addV('company').property(id, company_1).property('name', 'Jet Blue').property('employees', 550).next()

# add edges
g.V(contact_1).addE('knows').to(g.V(contact_2)).property('score', 5).next()
g.V(contact_3).addE('employee').to(g.V(company_1)).property('join_year', 2000).next()

# shortest path to target company
r = g.V().has('~id', contact_1).repeat(out().simplePath()).until(hasId(company_1)).path().limit(
    1).unfold().name.toList()
print("\n\nJosh shortest path to Jet Blue")
print(r)

# Delete a vertex
g.V().has('name', 'jean').drop().iterate()

# shortest path to target company
r = g.V().has('~id', contact_1).repeat(out().simplePath()).until(hasId(company_1)).path().limit(
    1).unfold().name.toList()
print("\n\nJosh shortest path to Jet Blue")
print(r)

# Delete all vertices
g.V().has('name', 'josh').drop().iterate()
g.V().has('name', 'joe').drop().iterate()
g.V().has('name', 'jean').drop().iterate()
g.V().has('name', 'Jet Blue').drop().iterate()

# WARNING!!! delete all data
# g.V().drop().iterate()

# close connection
remoteConn.close()
