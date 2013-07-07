from cypher_query_composer import NodeConstraint, RelationConstraint, CypherQueryComposer

class QuerySemanticParser:

    def __init__(self, sintactic_tree):
        self.queryComposer = CypherQueryComposer()
        self.sintactic_tree = sintactic_tree

        self.parsing_map = {
            'type_expr_constraints':self.parse_type_expression,
            'NODE_IDENTIFIER':self.parse_node_id

        }

    def parse(self):
        self.parseTree(self.sintactic_tree)

    def parse_type_expression(self, node):
        print "parsing type_expt"

    def parse_node_id(self, node):
        print "parsing node id"

    def parseTree(self, tree):
        node_type = tree[0]
        f = self.parsing_map[node_type]
        f(tree)

