from cypher_query_composer import NodeConstraint, RelationConstraint, CypherQueryComposer

class QuerySemanticParser:

    def __init__(self, sintactic_tree):
        self.queryComposer = CypherQueryComposer()
        self.sintactic_tree = sintactic_tree

        self.parsing_map = {
            'type_expr_constraints':self.parse_type_expression,
            #'NODE_IDENTIFIER':self.parse_node_id,
            'composed_expr': self.parse_composed_expr,
            #'type': self.parse_type,
            #'property':self.parse_property,
            #'multiword':self.parse_multiword,
            'constraint':self.parse_constraint,
            #'constraints':self.parse_constraints,
            'type_expr_no_constraints':self.parse_type_expr_no_constraints,
            'type_expr_constraints':self.parse_type_expr_constraints

        }

        self.first_subject = -1

    def parse(self):
        self.parseTree(self.sintactic_tree)
        self.queryComposer.setReturnNode(self.first_subject)
        print self.queryComposer.getQuery()

    def parse_type(self, node):
        pass

    def parse_composed_expr(self, node):
        first_expression = node[1]
        second_expression = node[4]
        target_node_id2 = self.parseTree(second_expression)
        operator = node[2][1]
        verb = node[3][1][1]
        target_node_id1 = self.parseTree(first_expression)
        self.queryComposer.addRelationConstraint(target_node_id1, verb, target_node_id2, '')
        return target_node_id1

    def parse_type_expr_no_constraints(self, node):
        type_node_id = self.queryComposer.getNodeIdentifier()
        type_name_value = node[1]['type'][1][1]
        print type_name_value
        self.queryComposer.addNodePropertyConstraints(type_node_id, 'name', type_name_value)
        target_node_id = self.queryComposer.getNodeIdentifier()
        self.queryComposer.addRelationConstraint(type_node_id, 'type_rel', target_node_id, '')

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
            property_name = node[1][1][1]
            print "prop"
            print property_name
            property_value = node[1][2][1]
            print "value"
            print property_value
            self.queryComposer.addNodePropertyConstraints(id_query_node, property_name, property_value)
        
        if node[0] == 'constraints':
            pass

    def parse_type_expression(self, node):
        print "parsing type_expt"

    def parse_node_id(self, node):
        print "parsing node id"

    def parseTree(self, tree):
        node_type = tree[0]
        f = self.parsing_map[node_type]
        return f(tree)

