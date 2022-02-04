'''
This cache_Temp_prep.py is used to get Temporal annotations from function:

getTEMPORAL(eventsOutput)
 
in EVENTS_demo_backend.py, and add the Temporal annotations into the cache_EE.

'''

import json
import hashlib
import requests
import sys

BASE_KAIROS_TEMPORAL_HTTP = "http://leguin.seas.upenn.edu:4024/annotate"


#-------------------- Temporal function and load function--------------------
def getTEMPORAL(eventsOutput):
    input = eventsOutput
    print("==== GENERATING TEMPORAL =====")
    # print(eventsOutput)
    # res_out = requests.post(BASE_KAIROS_TEMPORAL_HTTP, data = input)
    res_out = requests.post(BASE_KAIROS_TEMPORAL_HTTP, json = input)
    print('(4) BASE_KAIROS_TEMPORAL_HTTP!!!!!!!!!!!!!!!!!!!!!!!!')
    # print("==== res_out.text =====")
    # print(res_out.text)
    print("res_out.text",res_out.text)
    res_out_json = json.loads(res_out.text)
    # print("==== res_out.json =====")
    # print(res_out.json())
    # print("=======================")
    
    # res_json = json.loads(res_out.text)
    return res_out_json # {} # res_out.json()


def load(name):
    try:
        with open('cache_' + name + '.json') as file_obj:
            cache = json.load(file_obj)
        print("Successfully loaded cache from cache_" + name + ".json.")
    except:
        ValueError("Cannot find cache_" + name + ".json")
    
    return cache 

#-------------------- Run the script ----------------- 

if __name__ == "__main__":
    cache_EE = load('EE')  #cache_EE is a dictionary
    count = 0
    for key in cache_EE['eng'].keys():
        annjsonEvents = cache_EE['eng'][key]['res_json']
        res_out_json = getTEMPORAL(annjsonEvents)
        cache_EE['eng'][key]['temporal'] = res_out_json
        print('Sample No. ' + str(count + 1))
        print(cache_EE['eng'][key]['text'])
        count += 1

    cache_Temporal_json = json.dumps(cache_EE, indent=4)
    with open('cache_EE.json', 'w') as json_file:
        json_file.write(cache_Temporal_json) 
