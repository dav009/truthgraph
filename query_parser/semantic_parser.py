from cypher_query_composer import NodeConstraint, RelationConstraint, CypherQueryComposer
from spark.token import Token
class QuerySemanticParser:

    def __init__(self, sintactic_tree):
        self.queryComposer = CypherQueryComposer()
        self.sintactic_tree = sintactic_tree

        self.parsing_map = {
            'NODE_IDENTIFIER':self.parse_node_id,
            'composed_expr': self.parse_composed_expr,
            'type': self.parse_type,
            'property':self.parse_property,
            'multiword':self.parse_multiword,
            'constraint':self.parse_constraint,
            #'constraints':self.parse_constraints,
            'type_expr_no_constraints':self.parse_type_expr_no_constraints,
            'type_expr_constraints':self.parse_type_expr_constraints,

        }

        self.first_subject = -1

    def parse(self):
        self.parseTree(self.sintactic_tree)
        self.queryComposer.setReturnNode(self.first_subject)
        print self.queryComposer.getQuery()

    def parse_property(self, node):
        return node[1].attr

    def parse_multiword(self, node):
        return node[1]

    def parse_type(self, node):
        print node
        type_node_id = self.queryComposer.getNodeIdentifier()
        if isinstance(node[1],Token) and node[1].type== "NODE_KEYWORD":
            self.queryComposer.setNodeAsAny(type_node_id)
        else:
            type_name_value =  self.parseTree(node[1])
            self.queryComposer.addNodePropertyConstraints(type_node_id, 'name', type_name_value)
        return type_node_id

    def parse_composed_expr(self, node):
        composed_expr_data = node[1]
        first_expression = composed_expr_data['expression1']
        second_expression = composed_expr_data['expression2']
        target_node_id1 = self.parseTree(first_expression)
        target_node_id2 = self.parseTree(second_expression)
        operator = composed_expr_data['operator'].attr
        verb = self.parseTree(composed_expr_data['verb'])
        self.queryComposer.addRelationConstraint(target_node_id1, verb, target_node_id2, 'left')
        return target_node_id1

    def parse_type_expr_no_constraints(self, node):
        type_node_id = self.parseTree(node[1]['type'])
        target_node_id = self.queryComposer.getNodeIdentifier()
        self.queryComposer.addRelationConstraint(type_node_id, 'type_rel', target_node_id, 'right')

        if self.first_subject == -1:
            self.first_subject = target_node_id
        
        return type_node_id, target_node_id

    def parse_type_expr_constraints(self, node):
        type_node_id, target_node_id = self.parse_type_expr_no_constraints(node)
        constraints = node[1]['constraints']
        self.parse_constraint(constraints, target_node_id)
        return target_node_id

    def parse_constraint(self, node, id_query_node):
        if node[0] == 'constraint':
            property_name = self.parseTree(node[1]['property'])
            property_value =  self.parseTree(node[1]['value'])
            self.queryComposer.addNodePropertyConstraints(id_query_node, property_name, property_value)
        
        if node[0] == 'constraints':
            pass

    def parse_node_id(self, node):
        node_id = self.queryComposer.getNodeIdentifier()
        neo4j_id_number = node[1]
        self.queryComposer.setNodeID(node_id, neo4j_id_number)
        return node_id

    def parseTree(self, tree):
        node_type = tree[0]
        f = self.parsing_map[node_type]
        return f(tree)

