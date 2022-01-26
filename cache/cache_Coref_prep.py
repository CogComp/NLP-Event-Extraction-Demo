'''
This cache_Coref_prep.py is used to get Coreference annotations from function:

getSTORYLINE(events_json)
 
in EVENTS_demo_backend.py, and add the Coreference annotations into the cache_EE.
'''

import json
import hashlib
import requests
import sys

BASE_KAIROS_STORYLINE_HTTP = "http://leguin.seas.upenn.edu:4025/annotate"

#-------------------- Coreference function and load function--------------------

def getSTORYLINE(events_json):
    input = events_json
    print("==== GENERATING STORYLINE =====")
    # print(eventsOutput)
    # res_out = requests.post(BASE_KAIROS_TEMPORAL_HTTP, data = input)
    res_out = requests.post(BASE_KAIROS_STORYLINE_HTTP, json = input)
    print("(5)BASE_KAIROS_STORYLINE_HTTP was used!!!!!!!!!!!!!!!")
    # print("res_out.text",res_out.text)
    # exit(0)
    text = res_out.text
    if text.strip() == "" or text.strip() is None:
        return events_json
    # exit(0)
    res_out_json = json.loads(res_out.text)
    # REMOVE EVENTS 
    newRelations = []
    for v in res_out_json["views"]:
        if v["viewName"] == "Event_extraction":
            vDataRels = v["viewData"][0]["relations"]
            for r in vDataRels:
                # print(r["relationName"])
                if r["relationName"] == "coref": # and r["srcConstituent"] < r["targetConstituent"]:
                    newRelations.append(r)
            v["viewData"][0]["relations"] = newRelations
    return res_out_json # res_out.json()

def load(name):
    try:
        with open('cache_' + name + '.json') as file_obj:
            cache = json.load(file_obj)
        print("Successfully loaded cache from cache_" + name + ".json")
    except:
        ValueError("Cannot find cache_" + name + ".json")

    return cache 

#-------------------- Run the script ----------------- 

if __name__ == "__main__":
    cache_EE = load('EE')  #cache_EE is a dictionary
    count = 0
    for key in cache_EE['eng'].keys():  
        annjsonEvents = cache_EE['eng'][key]['res_json']
        try:
            res_out_json = getSTORYLINE(annjsonEvents)
            cache_EE['eng'][key]['coref'] = res_out_json            
            print('Sample ' + str(count + 1) + ' has been added to cache_EE!!')
            print(cache_EE['eng'][key]['text'])
            count += 1
        except:
            print('Failed to add sample ' + str(count + 1) +'into cache_EE!!')
            count +=1

    cache_Coref_json = json.dumps(cache_EE, indent=4)
    with open('cache_EE.json', 'w') as json_file:
        json_file.write(cache_Coref_json) 