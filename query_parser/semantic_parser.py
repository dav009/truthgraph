class QuerySemanticParser:

    def __init__(self):
        pass

    def parse(self, sintactic_tree):
        return self.processCurrentHead(sintactic_tree)
    
    def processCurrentHead(self, node):
        expression_head = node[0]

        if expression_head == ""