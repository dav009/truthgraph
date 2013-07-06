
class NodeConstraint:

    def __init__(self, constraint_definition):
        self.constraint_definition = constraint_definition

    def constraint_to_start_header(self):
        return self.constraint_definition['node']+" = node:node_auto_index"+"("+self.constraint_definition['property']+"=\""+self.constraint_definition['value']+"\")"

    def constraint_to_where_header(self):
        return self.constraint_definition['node']+"."+self.constraint_definition['property']+"=\""+self.constraint_definition['value']+"\""

class RelationConstraint:

    def __init__(self, constraint_definition):
        self.constraint_definition = constraint_definition

    def constraint_to_match_header(self):
        pass

class CypherQueryComposer:

    """
START target=node:node_auto_index(name="Barack Obama"), people = node:node_auto_index(mid="/m/04kr")
MATCH target<-[:type_rel]-people
RETURN target
    """
    def __init__(self, list_of_indexed_properties=['mid','enid','name']):
        self.list_of_indexed_properties = indexed_properties
        self.start_query = dict()
        self.match_query = list()
        self.where_query = list()
        self.return_query = dict()

        # automatic generation of ndoes ids
        self.nextNodeId = 0
        self.list_of_node_identifiers = list()
        self.node_id_prefix = "n_"
    
    def addNodePropertyConstraints(self, node_query_identifier, property_name, value):
        constraint_dictionary = NodeConstraint({'node':node_query_identifier,'property':property_name,'value':value})
        if property_name in self.list_of_indexed_properties and not node_query_identifier in self.start_query:
            self.start_query[node_query_identifier] = constraint_dictionary
        else:
            self.where_query.append(constraint_dictionary)

    def addRelationConstraint(self, node_query_id1,relation_type, node_query_id2, direction):
        self.match_query.append({"node1":node_query_id1, "node2":node_query_id2, "relation":relation_type, "direction":direction})

    def getNodeIdentifier(self):
        next_id = self.node_id_prefix +str(self.nextNodeId)
        self.nextNodeId = self.nextNodeId + 1
        self.list_of_node_identifiers.append(next_id)
        return next_id

    def setReturnNode(self, node_identifier):
        self.return_query['return'] = node_identifier

    def getQuery(self):
        self._composeStart()
        self._composeWhere()

    def _composeStart(self):
        query_skeleton = "START"
        body = ""
        connector = ","
        for constraint in self.start_query:
            if body == '':
                body = constraint.constraint_to_start_header()
            else:
                body = connector + constraint.constraint_to_start_header()
        return query_skeleton+" "+body

    def _composeWhere(self):
        query_skeleton_where = "WHERE"
        pass

    def _composeMatch(self):
        query_skeleton_match = "MATCH"
        pass

    def _composeReturn(self):
        query_skeleton_return = "RETURN"
        body = ""
        body = self.return_query['return']
        return query_skeleton_return+" "+body

class QuerySemanticParser:

    def __init__(self):
        pass

    def parse(self, sintactic_tree):
        return self.processCurrentHead(sintactic_tree)
    
    def processCurrentHead(self, node):
        expression_head = node[0]

        if expression_head == ""