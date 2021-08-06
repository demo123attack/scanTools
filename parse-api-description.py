import spacy
import os
from spacy import displacy


apiDesFile=open('path_to_api_descriptions')
apiParseFile=open('path_to_save_result','w')
verblist=[]
verblistText=[]
nlp = spacy.load("en_core_web_md")
data=apiDesFile.read()
doc=nlp(data)

for sent in doc.sents:
	Verb=sent[-1]
	Obj=""
	Dobj=sent[-1]
	Pobj=sent[-1]
	Prep=sent[-1]

	
	for token in sent:
		if token.dep_ == "ROOT" and token.pos_ == "VERB":
				Verb=token
				print(Verb.text)

	if "can be used" or "use this" or "Use this" or "can use this API" or "Use this API" in sent.text:
	 	for index in range(len(sent)):
	 		if sent[index].text == "to":
	 			if sent[index+1].pos_ == "VERB":
					 Verb=sent[index+1]
					 print(Verb.text)

	for token in sent:	
		if str(token.dep_) == "dobj":
			if Verb:
				if token.head ==  Verb:
					Dobj=token
					Obj=token.text
	
	for token in sent:	
		if str(token.dep_) == "compound":
			if token.head == Dobj:
				Obj=token.text+" "+Obj
	
	for token in sent:
		if str(token.dep_) == "prep":
				if token.head == Dobj:
						Prep = token

	for token in sent:	
		if str(token.dep_) == "pobj":
			if token.head == Prep:
				Obj=Obj+" "+Prep.text+" "+token.text

	if Dobj == sent[-1]:
		for token in sent:
				if str(token.dep_) == "pobj":
					Obj=token.text
					break;

	for token in sent:
			if token.dep_ == "ROOT":
				if Verb != token:
					print(sent.text,Verb.text,token.text)

	if Verb.text:
		apiParseFile.write(Verb.text+"\t"+Obj+"\n")
		print(Verb.text)
	else:
		apiParseFile.write("\n")

#displacy.serve(doc,style="dep")


