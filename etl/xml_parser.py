import xml.etree.ElementTree as xml
import unicodedata
class parseFile:

	LIST_OF_UNKNOWN_VALUES = [u"SIN INFORMACIÓN","SIN INFORMACION" ]

	def __init__(self, path_to_file):
		# parse xml
		self.xmldoc =  xml.parse(path_to_file)

		# relevant information
		self.victims = list()
		self.armedGroups =list()
		self.observations = dict()
		self.action = dict()

	def processTagText(self, text):
		if text:
			splitted_text = text.split(",")

			if len(splitted_text) >3 :
				return splitted_text
			else:
				if not isinstance(text,str):
					return unicodedata.normalize('NFKD', text).encode('ascii','ignore')
				else:
					return text

	def getDictionaryFromXMLNode(self, xmlNode ):
		dictionary = dict()
		if len(xmlNode.getchildren()) > 0:
			for child in xmlNode.getchildren():
				if not child.text in self.LIST_OF_UNKNOWN_VALUES and not child.tag =="agresion_sin_vicd":
					if not child.tag == "observaciones":
						dictionary[child.tag] = self.processTagText(child.text)
					else:
						for key, value in child.attrib.items():
							dictionary[value] =  self.processTagText(child.text)
		elif  len(xmlNode.attrib) == 0:
			dictionary[xmlNode.tag] =  self.processTagText(xmlNode.text)
		else:
			for key, value in xmlNode.attrib.items():
				if xmlNode.text and  not xmlNode.text in self.LIST_OF_UNKNOWN_VALUES:
					dictionary[ value] =  self.processTagText(xmlNode.text)
		return dictionary

	def unifyPersonasVictimas(self, list_of_dictionary_of_persona, list_of_dictionary_of_victima):

		unified_list_of_victims = list()

		hash_of_personas = dict()
		for persona in list_of_dictionary_of_persona:
			hash_of_personas[persona['id_persona']] = persona

		for victim in list_of_dictionary_of_victima:
			persona = hash_of_personas.get(victim['id_persona'])
			if persona:
				unifed_dict = dict( victim.items() + persona.items() )
				unified_list_of_victims.append(unifed_dict)

		return unified_list_of_victims


	def parseFile(self,file_path):

		rootElement = self.xmldoc.getroot().getchildren()[0]

		# list of personas
		personas = rootElement.findall("persona")
		list_of_personas_dictionary = [ self.getDictionaryFromXMLNode(persona) for persona in personas ]
		#print list_of_personas_dictionary

		victimas = rootElement.findall("victima")
		list_of_victimas_dictionary = [ self.getDictionaryFromXMLNode(victima) for victima in victimas ]
		#print list_of_victimas_dictionary

		grupos = rootElement.findall("grupo")
		list_of_grupos_dictionary = [ self.getDictionaryFromXMLNode(grupo) for grupo in grupos ]
		#print "GRUPOS"
		#print list_of_grupos_dictionary

		actos = rootElement.findall("acto")
		list_of_actos_dictionary = [ self.getDictionaryFromXMLNode(acto) for acto in actos ]
		#print list_of_actos_dictionary

		observaciones = rootElement.findall("observaciones")
		list_of_observaciones_dictionary = [ self.getDictionaryFromXMLNode(observacion) for observacion in observaciones ]
		#print list_of_observaciones_dictionary

		fecha = rootElement.findall("fecha")[0]
		fecha =self.getDictionaryFromXMLNode(fecha)
		#print fecha

		departamento = rootElement.findall("departamento")
		if len(departamento) > 0:
			departamento = departamento[0]
			departamento =self.getDictionaryFromXMLNode(departamento)
		else:
			departamento = 'unknown'
		#print departamento

		# unify personas and victimas
		list_of_victimas = self.unifyPersonasVictimas(list_of_personas_dictionary, list_of_victimas_dictionary)


		parsed_data = dict()

		parsed_data['victimas'] = list_of_victimas
		parsed_data['grupo'] = list_of_grupos_dictionary
		parsed_data['actos'] = list_of_actos_dictionary
		parsed_data['observaciones'] = list_of_observaciones_dictionary
		parsed_data['fecha'] =fecha
		parsed_data['departamento'] =departamento
		parsed_data['id_relato'] = rootElement.findall("id_relato")[0].text

		return parsed_data