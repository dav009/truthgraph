class NodeConstraint:

    def __init__(self, constraint_definition):
        self.constraint_definition = constraint_definition

    def constraint_to_start_header(self):
        if self.constraint_definition['property']=="__ANY__" and self.constraint_definition['value']=="__ANY__":
            return self.constraint_definition['node']+" = node(*)"
        elif  self.constraint_definition['property']=="__ID__":
            return self.constraint_definition['node']+" = node"+"("+self.constraint_definition['value']+")"
        else:
            return self.constraint_definition['node']+" = node:node_auto_index"+"("+self.constraint_definition['property']+"=\""+self.constraint_definition['value']+"\")"
            
    def constraint_to_where_header(self):
        print self.constraint_definition
        return self.constraint_definition['node']+"."+self.constraint_definition['property']+"=\""+self.constraint_definition['value']+"\""

class RelationConstraint:

    def __init__(self, constraint_definition):
        self.constraint_definition = constraint_definition

    def constraint_to_match_header(self):
        left_direction= ''
        right_direction =''
        if self.constraint_definition['direction'] == 'left' or self.constraint_definition['direction']=='both':
            left_direction = "<"
        if self.constraint_definition['direction'] == 'right' or self.constraint_definition['direction']=='both':
            right_direction = ">"
        return self.constraint_definition['node1']+left_direction+"-[:"+self.constraint_definition['relation']+"]-"+right_direction+self.constraint_definition['node2']


class CypherQueryComposer:

    """
START target=node:node_auto_index(name="Barack Obama"), people = node:node_auto_index(mid="/m/04kr")
MATCH target<-[:type_rel]-people
RETURN target
    """
    def __init__(self, list_of_indexed_properties=['mid','enid','name']):
        self.list_of_indexed_properties = list_of_indexed_properties
        self.list_of_indexed_properties.append('__ID__')
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

    def setNodeID(self, node_query_identifier, neo4j_id):
        self.addNodePropertyConstraints(node_query_identifier, "__ID__", neo4j_id)

    def setNodeAsAny(self, node_query_identifier):
        self.addNodePropertyConstraints(self, node_query_identifier, "__ANY__", "__ANY__")

    def addRelationConstraint(self, node_query_id1,relation_type, node_query_id2, direction):
        self.match_query.append(RelationConstraint({"node1":node_query_id1, "node2":node_query_id2, "relation":relation_type, "direction":direction}))

    def getNodeIdentifier(self):
        next_id = self.node_id_prefix +str(self.nextNodeId)
        self.nextNodeId = self.nextNodeId + 1
        self.list_of_node_identifiers.append(next_id)
        return next_id

    def setReturnNode(self, node_identifier):
        self.return_query['return'] = node_identifier

    def getQuery(self):
        start = self._composeStart()
        where = self._composeWhere()
        match = self._composeMatch()
        return_ = self._composeReturn()

        return start+" "+where+" "+match+" "+return_

    def _composeStart(self):
        query_skeleton = "START"
        body = ""
        connector = ","
        for constraint in self.start_query.values():
            if body == '':
                body = constraint.constraint_to_start_header()
            else:
                body = body + connector + constraint.constraint_to_start_header()
        return query_skeleton+" "+body

    def _composeWhere(self):
        query_skeleton = "WHERE"
        body = ""
        connector = " AND "
        for constraint in self.where_query:
            if body == '':
                body = constraint.constraint_to_where_header()
            else:
                body = connector + constraint.constraint_to_where_header()

        if body!='':
            return query_skeleton+" "+body
        else:
            return ''

    def _composeMatch(self):
        query_skeleton = "MATCH"
        body = ""
        connector = " AND "
        for relationConstraint in self.match_query:
            if body == '':
                body = relationConstraint.constraint_to_match_header()
            else:
                body = body + connector + relationConstraint.constraint_to_match_header()
        if body != '':
            return query_skeleton + " "+body
        else:
            return ''

    def _composeReturn(self):
        query_skeleton_return = "RETURN"
        body = ""
        body = self.return_query['return']
        return query_skeleton_return+" "+body

if __name__ == '__main__':
    cypher_composer = CypherQueryComposer()
    node1 = cypher_composer.getNodeIdentifier()
    node2= cypher_composer.getNodeIdentifier()
    cypher_composer.addNodePropertyConstraints(node1, 'enid', '/en/george_lucas')
    cypher_composer.addRelationConstraint(node2, 'type_rel', node1, '')
    cypher_composer.addNodePropertyConstraints(node2, 'enid', '/people/person')
    cypher_composer.setReturnNode(node1)
    print cypher_composer.getQuery()