from tokenizer import Tokenizer
from parser import QueryParser

scanner = Tokenizer()
data = "people whose name is \"david alejandro\" and lives in place whose name is \"the united states\""
#data = "node"
list_of_tokens= scanner.tokenize(data)
print "TOKEN LIST:"
print list_of_tokens
parser = QueryParser()

print "PARSING RESULT"
print parser.parse(list_of_tokens)
