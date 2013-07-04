import py2neo.neo4j
from py2neo import node,rel
from neo4j import GraphDatabase

class Neo4jHandler:

	def __init__(self, graph_path):
		config = {"node_keys_indexable":'key,name',"node_auto_indexing":'true' }
		self.graph_db = GraphDatabase(graph_path ,**config)
		self.node_auto_index = self.graph_db.node.indexes.get('node_auto_index')
		#self.graph_db = py2neo.neo4j.GraphDatabaseService( graph_path)

	def findNode(self, node_dict):
		
		result = self.node_auto_index['key'][node_dict['key']]
		if result:
			# .single goes mad when there is a result set with more than one value
			return result.single
		#py2neo_node = self.graph_db.get_indexed_node('node_auto_index', 'key', node_dict['key'])
		#return py2neo_node


	def createUniqueNodeByKey(self, node_dict):

		py2neo_node = self.findNode(node_dict)
		if py2neo_node:
			# if it was found return it
			return py2neo_node
		else:
			# if not create it
			with self.graph_db.transaction:
				return self.graph_db.node( **node_dict )
			#return self.graph_db.node( node(**node_dict) )[0]

	def findNodeByKey(self, key, value):
		return self.node_auto_index[key][value].single
		#py2neo_node = self.graph_db.get_indexed_node('node_auto_index', key, value)
		#return py2neo_node


	def addEvent(self, parsed_data):
		# create event node
		key_of_relato = "relato:"+str(parsed_data['id_relato'])
		with self.graph_db.transaction:
			relato_neo4j_node = self.graph_db.node(key=key_of_relato, type="relato") 
		#relato_neo4j_node = self.graph_db.create( node(key=key_of_relato) )[0]
		
		# connect victims to events via actos
		actos_processed = list()
		for acto in parsed_data['actos']:
			actos_processed.append(self.getCrimes(acto))

		victim_groups = set()
		for acto in actos_processed:
			key_of_victim_node = acto[0]
			if key_of_victim_node.startswith('grupo:'):
				victim_groups.add(key_of_victim_node)


		# get the node dictioanry of the armed entities
		list_of_node_dict_armed_entities = list()
		list_of_node_dict_victim_groups=list()
		for armed_entity in parsed_data['grupo']:
			node_dict_entity = self.getArmedEntity(armed_entity)
			if not node_dict_entity['key'] in victim_groups:
				list_of_node_dict_armed_entities.append( node_dict_entity )
			else:
				list_of_node_dict_victim_groups.append(node_dict_entity)


		# add them to neo4j
		list_of_neo4j_armed_nodes =list()
		for armed_node_dict in list_of_node_dict_armed_entities:
			# create armed group node
			armed_node =self.createUniqueNodeByKey(armed_node_dict)
			list_of_neo4j_armed_nodes.append(armed_node)
			# relate armed group with eevent
			#self.graph_db.create( (armed_node,'responsible_for',relato_neo4j_node) )
			with self.graph_db.transaction:
				armed_node.relationships.create('responsible_for', relato_neo4j_node )

		for victim_group in list_of_node_dict_victim_groups:
			# create armed group node
			victim_group_node =self.createUniqueNodeByKey(victim_group)




		# get the node dictionaries for the victims
		list_of_node_dict_victims = list()
		list_of_adjacent_victim_relation = list()
		for victima in parsed_data['victimas']:
			victim_node, adjacent_relations = self.getVictim(victima)
			list_of_node_dict_victims.append(victim_node)
			list_of_adjacent_victim_relation.append(adjacent_relations)

		# add them to neo4j
		list_of_neo4j_victim_nodes =list()
		for index in range(0,len(list_of_node_dict_victims)):
			victim_node_dict =  list_of_node_dict_victims[index]
			other_relations = list_of_adjacent_victim_relation[index]
			# create victim node
			victim_node =self.createUniqueNodeByKey(victim_node_dict)
			list_of_neo4j_victim_nodes.append(victim_node)
			# connect to things like rando de edad, sexo, organizacion
			for other_rel in other_relations:
				relation_name = other_rel[0]
				other_node_dict = other_rel[1]
				other_neo4j_node =self.createUniqueNodeByKey(other_node_dict)
				# connecting victim to other info
				#self.graph_db.create( (victim_node,relation_name,other_neo4j_node) )
				with self.graph_db.transaction:
					victim_node.relationships.create(relation_name, other_neo4j_node )


		for acto in actos_processed:
			key_of_victim_node = acto[0] 
			key_of_armed_group = acto[1]
			arc_dictionary =  acto[2]

			victim_neo4j_node = self.findNodeByKey('key',key_of_victim_node)
			armed_group_neo4j_node = self.findNodeByKey('key',key_of_armed_group)

			#self.graph_db.create( (relato_neo4j_node,arc_dictionary['agresion_particular'],victim_neo4j_node, arc_dictionary)  )
			with self.graph_db.transaction:
				relato_neo4j_node.relationships.create(arc_dictionary['agresion_particular'],victim_neo4j_node, **arc_dictionary)

		# transform each observacion in a node connected to the event
		for observacion in parsed_data['observaciones']:
			if not 'bienes' in observacion:
				for key, value in  observacion.items():
					observacion_node_dict = dict()
					if isinstance(value, list):
						for element in value:
							observacion_node_dict['key'] ="observacion:"+element
							observacion_node_dict['type'] ="observacion"
							observacion_neo4j_node = self.createUniqueNodeByKey(observacion_node_dict)
							#self.graph_db.create( (relato_neo4j_node,key, observacion_neo4j_node) )
							with self.graph_db.transaction:
								relato_neo4j_node.relationships.create(key, observacion_neo4j_node)
					else:
						observacion_node_dict['key'] ="observacion:"+value
						observacion_node_dict['type'] ="observacion"
						observacion_neo4j_node = self.createUniqueNodeByKey(observacion_node_dict)
						#self.graph_db.create( (relato_neo4j_node,key, observacion_neo4j_node) )
						with self.graph_db.transaction:
							relato_neo4j_node.relationships.create(key, observacion_neo4j_node)


		# create arcs between event and groups ( using the)

		# create arcs between event and victims

	def getVictim(self, dictionary_of_victim_node):
		victim_node_dict = dict()
		victim_node_dict['key']= 'persona:'+dictionary_of_victim_node['id_persona']
		victim_node_dict['fecha_nacimiento'] = dictionary_of_victim_node.get('fecha_nacimiento')
		victim_node_dict['name'] = dictionary_of_victim_node.get('nombre')
		victim_node_dict['type'] = 'victim'
		victim_node_dict['sexo'] = dictionary_of_victim_node.get('sexo')

		del dictionary_of_victim_node['id_persona']
		if 'fecha_nacimiento' in dictionary_of_victim_node:
			del dictionary_of_victim_node['fecha_nacimiento']
		if 'nombre' in  dictionary_of_victim_node:
			del dictionary_of_victim_node['nombre']
		# making gender a node property
		if 'sexo' in  dictionary_of_victim_node:
			del dictionary_of_victim_node['sexo']

		# instead of using properties use node and relations to define the other fields
		adjacent_relations = list()
		for relation_name,value in dictionary_of_victim_node.items():
			other_node_dict = { 'key':relation_name+":"+value, 'type':relation_name }
			relation_tuple = (relation_name, other_node_dict)
			adjacent_relations.append(relation_tuple)

		return victim_node_dict, adjacent_relations

	def getArmedEntity(self, dictionary_of_armed_entity):
		armed_node_dict = dict()
		armed_node_dict['key'] = "grupo:"+dictionary_of_armed_entity['id_grupo']
		armed_node_dict['type'] = "victimario"
		if 'nombre_grupo' in dictionary_of_armed_entity:
			armed_node_dict['name'] = dictionary_of_armed_entity['nombre_grupo']

		return armed_node_dict

	def getCrimes(self, dictionary_of_crime):
		key_of_victim_node = None
		if 'id_grupo_victima' in dictionary_of_crime:
			key_of_victim_node = "grupo:"+dictionary_of_crime['id_grupo_victima']
		else:
			key_of_victim_node = "persona:"+dictionary_of_crime['id_victima_individual']
		key_of_armed_group = "grupo:" +dictionary_of_crime['id_presunto_grupo_responsable']
		arc_dictionary = dict()
		arc_dictionary['agresion_particular'] = dictionary_of_crime.get('agresion_particular')
		arc_dictionary['agresion'] = dictionary_of_crime.get('agresion')

		return (key_of_victim_node, key_of_armed_group, arc_dictionary)

