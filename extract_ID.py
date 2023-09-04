#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 22:00:40 2023

@author: antonomaz
"""

import json
import re

def extract_sequences(data):
    sequences = []
    
    # Convert the JSON data to a string
    data_str = json.dumps(data)
    
    # Use regular expression to find sequences of "Q" followed by digits
    pattern = r'Q\d+'
    matches = re.findall(pattern, data_str)
    
    # Add the matches to the list
    sequences.extend(matches)
    
    return sequences

# Load JSON data from a file
file_path = "../DATA/ELTeC-Fra_2023/ADAM/ADAM_krakenbase/REF/ADAM_Mon-village_REF.txt_entitylinker-refined.json"

/ReFinED/DATA/ELTeC-Fra_2023/ADAM/ADAM_krakenbase/REF/ADAM_Mon-village_REF.txt_entitylinker-refined.json
with open(file_path, 'r') as file:
    json_data = json.load(file)

# Extract sequences from the JSON data
sequences_list = extract_sequences(json_data)

# Print the extracted sequences
for sequence in sequences_list:
    print(sequence)
