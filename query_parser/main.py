from tokenizer import Tokenizer
from parser import QueryParser

data = "people whose name is \"david alejandro\" and lives in place whose name is \"the united states\""
#data = "node"
def analyze(string):
    scanner = Tokenizer()
    list_of_tokens= scanner.tokenize(string)
    print "-------------"
    print "TOKEN LIST:"
    print list_of_tokens
    parser = QueryParser()
    print "----------------"
    print "PARSING RESULT"
    print "----------------"
    print parser.parse(list_of_tokens)
