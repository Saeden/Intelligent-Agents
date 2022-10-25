#import requests
from owlready2 import *



owlready2.JAVA_EXE = "C:\\Program Files (x86)\\Java\\jre1.8.0_351\\bin\\java.exe"
owlready2.reasoning.JAVA_MEMORY = 1000

#onto_path.append("Ontology_Intelligent_Agents_Group8.owl")

onto = get_ontology("file://ontology_test.owl").load()

sync_reasoner()

