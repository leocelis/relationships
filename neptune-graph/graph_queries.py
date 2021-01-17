"""
Neptune DB cluster setup: https://docs.aws.amazon.com/neptune/latest/userguide/get-started-create-cluster.html

Graph Viz: https://github.com/bricaud/graphexp
"""

from __future__ import print_function  # Python 2/3 compatibility

from gremlin_python import statics
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph
from tornado import httpclient

statics.load_statics(globals())
graph = Graph()

# connect to Neptune
my_req = httpclient.HTTPRequest('wss://localhost:8182/gremlin',
                                # headers={"Authorization": "Token AZX ..."},
                                validate_cert=False)

remoteConn = DriverRemoteConnection(my_req, 'g')
g = graph.traversal().withRemote(remoteConn)

# get who Lauren (003A000001fOaGAIA0) knows
r = g.V().has('~id', "003A000001fOaGAIA0").out('knows').last_name.toList()
print("Lauren's contacts")
for i in r:
    print(i)

# get who Lauren's contacts knows
r = g.V().has('~id', "003A000001fOaGAIA0").out('knows').out('knows').last_name.toList()
print("\n\nLauren contacts' contacts")
for i in r:
    print(i)

# get Lauren's contact with score > 2
r = g.V().has('~id', "003A000001fOaGAIA0").outE('knows').has('score', gt(1)).inV().last_name.toList()
print("\n\nLauren's score > 1 contacts")
for i in r:
    print(i)

# get Lauren contacts' contacts with score > 2
r = g.V().has('~id', "003A000001fOaGAIA0"
              ).outE('knows').has('score', gt(1)).inV().outE().has('score', gt(2)).inV().last_name.toList()
print("\n\nLauren's score > 1 contacts' contacts with score > 2")
for i in r:
    print(i)

# Lauren's path to 003A000001TvO1KIAV
r = g.V().has('~id', "003A000001fOaGAIA0"
              ).repeat(out().simplePath()).until(hasId('003A000001TvO1KIAV')
                                                 ).path().limit(1).unfold().last_name.toList()
print("\n\nLauren's shortest path to Ochoa")
print(r)

# delete all data
# g.V().drop().iterate()

# close connection
remoteConn.close()
