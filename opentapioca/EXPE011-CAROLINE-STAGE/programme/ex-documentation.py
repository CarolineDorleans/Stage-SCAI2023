#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 15:12:22 2023

@author: antonomaz
"""
# import spacy
# nlp = spacy.blank("en")
# nlp.add_pipe('opentapioca')
# doc = nlp("Christian Drosten works in Germany.")
# for span in doc.ents:
#     print((span.text, span.kb_id_, span.label_, span._.description, span._.score))
    
    
# import spacy
# nlp = spacy.blank("en")
# nlp.add_pipe('opentapioca')
# doc = nlp("Napoleon envaded Russia")
# for span in doc.ents:
#     print((span.text, span.kb_id_, span.label_, span._.description, span._.score))

import spacy
nlp = spacy.blank("en")
nlp.add_pipe('opentapioca')
doc = nlp("Napoleon Bonaparte a envahi la Russie en 1912")
for span in doc.ents:
    print((span.text, span.kb_id_, span.label_, span._.description, span._.score))