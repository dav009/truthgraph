# -*- coding: utf-8 -*- 
import os
import traceback
import xml.etree.ElementTree as xml
from xml_parser import parseFile
from neo4j_handler import Neo4jHandler

def main():
	neo4j_hand= Neo4jHandler("/home/attickid/Desktop/neo4j-community-1.9/data/graph.db")
	try:
		path = "/home/attickid/Desktop/niebla/n/"
		#neo4j_hand= Neo4jHandler("http://localhost:7474/db/data/")
		
		listing = os.listdir(path)
		counter = 1
		#listing=["nyn3822.xrlat"]

		for infile in listing:
			if infile.endswith('.xrlat'):
				try:
					print str(counter)+" of "+str(len(listing))+".."+infile
					current_file = parseFile(path+infile)
					parsed_data =current_file.parseFile("")
					neo4j_hand.addEvent(parsed_data)
					counter = counter +1
				except xml.ParseError:
					continue
		neo4j_hand.graph_db.shutdown()
	except Exception as e:
		print "error probably unicode"
		traceback.print_exc()
		neo4j_hand.graph_db.shutdown()
main()

