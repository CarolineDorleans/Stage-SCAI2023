#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 10:47:03 2023

@author: antonomaz
"""

from refined.inference.processor import Refined


refined = Refined.from_pretrained(model_name='wikipedia_model_with_numbers',
                                  entity_set="wikipedia")

spans = refined.process_text("Je m'appelle Caroline")

for span in spans:
    #print(span.__dict__)
    description= span.__dict__
    #help(span)
    #dico = dict(clé =span.__dict__)
    dico_sent_tok[ide]={span.__dict__}
    #break
    # span=str(span)
    
    
    # for entite in span: 
    #     print(entite)
    #pan[0] = entite
   #span[1] = ID
   #span[2] = typed
        

#rint(spans)