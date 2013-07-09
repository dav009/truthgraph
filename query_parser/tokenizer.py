import spark.spark as spark
from spark.token import Token

class Tokenizer(spark.GenericScanner):

	def __init__(self):
		spark.GenericScanner.__init__(self)

	keywords ={'name':'NAME_PROPERTY',
				'mid':'MID_PROPERTY',
				'enid':'ENID_PROPERTY',
				'whose':'WHOSE_KEYWORD',
				'related':'RELATION_KEYWORD', 
				'is':'IS_KEYWORD',
				'node':'NODE_KEYWORD',
				'and':'OPERATOR'}

	def tokenize(self, input):
		self.rv = []
		spark.GenericScanner.tokenize(self, input)
		return self.rv

	def t_whitespace(self, s):
		r" [ \t\r\n]+ "
		pass

	def t_LPAREN(self, s):
		r" \( "
		self.rv.append(Token(type="LPAREN"))

	def t_RPAREN(self, s):
		r" \) "
		self.rv.append(Token(type="RPAREN"))

	def t_NUMBER(self, s):
		r'[0-9]+'
		print "called"
		self.rv.append(Token(type="NUMBER", attr=s))

	def t_COLON(self, s):
		r' \: '
		self.rv.append( Token(type="COLON") )

	def t_QUOTE(self, s):
		r' \" '
		self.rv.append(Token(type="QUOTE"))

	def t_keyword(self, s):
	    self.rv.append(Token(type=self.keywords[s], attr=s))

	def t_STRING(self, s):
		r' [a-zA-Z0-9_]+ '
		if s in self.keywords:
			self.t_keyword(s)
		else:
			self.rv.append(Token(type="STRING", attr=s))