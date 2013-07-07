import spark.spark as spark
from spark.ast import AST

class QueryParser(spark.GenericParser):
	def __init__(self, start='expression'):
		spark.GenericParser.__init__(self, start)
		print self.rules

	def p_expression1(self,p):
		'''
		expression ::= simple_expression
		'''
		return p[0]

	def p_expression2(self,p):
		'''
		expression ::= expression OPERATOR multiword simple_expression
		'''
		return ('composed_expr', p[0], ('operator', p[1]), ('verb', p[2] ), p[3])

	def p_type(self,p):
		'''type ::= NODE_KEYWORD
		'''
		return ('type', p[0])

	def p_type2(self,p):
		'''
		type ::= RELATION_KEYWORD
		'''
		return ('type', p[0])

	def p_type3(self,p):
		'''
		type ::= multiword
		'''
		return ('type',p[0])

	def p_property(self, p):
		'''property ::= NAME_PROPERTY'''
		return ('property', p[0])

	def p_property2(self, p):
		'''property ::=  ENID_PROPERTY'''
		return ('property', p[0])

	def p_property3(self, p):
		'''property ::= MID_PROPERTY '''
		return ('property', p[0])

	def p_multiword0(self, p):
		'''multiword ::= STRING
		'''
		return ('multiword', p[0])

	def p_multiword1(self, p):
		'''multiword ::= IS_KEYWORD
		'''
		return ('multiword', p[0])

	def p_multiword2(self, p):
		'''multiword ::= multiword STRING
		'''
		return ('multiword',p[0][1],p[1])

	def p_constraint1(self, p):
		'''constraint ::= property IS_KEYWORD QUOTE multiword QUOTE
		'''
		return ('constraint', ('property', p[0], p[3]) )

	def p_constraint2(self, p):
		'''constraint ::= constraint OPERATOR constraint
		'''
		return ('constraints',(p[0], ('operator', p[1]), p[2] ))

	def p_type_expression1(self, p):
		'''type_expression ::= type
		'''
		return ('type_expr_no_constraints', {'type':p[0]} )

	def p_type_expression2(self, p):
		'''type_expression ::= type WHOSE_KEYWORD constraint 
		'''
		return ('type_expr_constraints', {'type':p[0], 'constraints':p[2]})

	def p_node_expression(self, p):
		'''node_expression ::= COLON NUMBER
		'''
		return ('NODE_IDENTIFIER',p[1].attr)

	def p_simple_expression(self, p):
		'''simple_expression ::= node_expression
		'''
		return p[0]

	def p_simple_expression1(self, p):
		'''simple_expression ::= type_expression
		'''
		return p[0]