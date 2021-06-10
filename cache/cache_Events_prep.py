'''
This cache_Events_prep script is used to create a cache of Events from function: 

getBasicAnnotationsFromEVENTS(text) 

in EVENTS_demo_backend.py
'''

import json
import hashlib
import requests
import sys

BASE_KAIROS_EVENTS_HTTP = "http://leguin.seas.upenn.edu:4023/annotate"

#--------------------- Sample Sentences ---------------------
sample_dic = {
    "eng": [
		"In the January attack, two Palestinian suicide bombers blew themselves up in central Tel Aviv. The bombing destroyed the whole building, killing 23 other people. Police fatally shot a suspect of the bombing who ended up killing himself this morning.",
		"In the January attack, two Palestinian suicide bombers blew themselves up in central Tel Aviv. The bombing destroyed the whole building, killing 23 other people.",
		"In the January attack, two Palestinian suicide bombers blew themselves up in central Tel Aviv, killing 23 other people.",
		"The bombing destroys the whole building."]
}

#-------------------- Event function --------------------
def getBasicAnnotationsFromEVENTS(text):
    input = {"text":text}
    res_out = requests.post(BASE_KAIROS_EVENTS_HTTP, json = input)
    #print("(3)BASE_KAIROS_EVENTS_HTTP was used!!!!!!!!!!!!!!!")
    #print("=======================")
    #print(res_out.text)
    #print("=======================")
    # res_json = json.loads(res_out.text)
    res_json = res_out.json()
    
    tokens = []
    endPositions = []

    if "tokens" in res_json:
        tokens = res_json["tokens"]
    # print(tokens)
    if "sentences" in res_json:
        sentences = res_json["sentences"]
        if "sentenceEndPositions" in sentences:
            endPositions = sentences["sentenceEndPositions"]
    return tokens, endPositions, res_json

def load(name):
    '''
    name: "Event"
    '''
    try:
        with open('cache/cache_' + name + '.json') as file_obj:
            cache = json.load(file_obj)
        print("Successfully load cache from cache_" + name + ".json.")
    except:
        ValueError("Cannot find cache_" + name + ".json")
    
    return cache 
#-------------------- Run the script -----------------    
if __name__ == "__main__":
    mode = sys.argv[1]

    if mode == "create":
    #-------------------- Create Cache for Event-----------------
        cache_Event = {}
        for lang in sample_dic.keys():
            cache_Event[lang] = {}
            print("Start to get Event annotations from language " + lang)
            count = 0
            for text in sample_dic[lang]:
                hash_value = hashlib.sha1(text.encode()).hexdigest()
                if hash_value in cache_Event[lang].keys():
                    raise ValueError('COLLISION ERROR: Different text has same hash value!')
                else:
                    cache_Event[lang][hash_value] = {}
                    cache_Event[lang][hash_value]['text'] = text #the raw text is not included in the return of getMULTILANG_EDL(lang,text)
                    t,s,annjsonEvents = getBasicAnnotationsFromEVENTS(text)
                    cache_Event[lang][hash_value]['res_json'] = annjsonEvents
                    cache_Event[lang][hash_value]['token'] = t
                    cache_Event[lang][hash_value]['end_pos'] = s
                    count += 1
                    print('The ' + str(count) + 'th sample has been add in cache_Event')

        cache_Event_json = json.dumps(cache_Event, indent=4)
        with open('cache/cache_EE.json', 'w') as json_file:
            json_file.write(cache_Event_json)

        print("Success in creating cache_Event!")
    #-------------------- Add additional Event Annotation into the cache_EE-----------------
    if mode == "add":
        cache_Event = load('EE')
        
        ff = open("sample_manually.txt","r") 
        sample_list = ff.readlines()      # return sentence as list
        ff.close()

        lang='eng'
        count = 0
        for i in range(len(sample_list)):   
            text = sample_list[i][1:-2]        
            hash_value = hashlib.sha1(text.encode()).hexdigest()
            if hash_value in cache_Event[lang].keys():
                print(f"Warning: {i}th sample has already in cache_Events, skip to next sample!")
                pass
            else:
                try:
                    t,s,annjsonEvents = getBasicAnnotationsFromEVENTS(text)
                except:
                    cache_Event_json = json.dumps(cache_Event, indent=4)
                    with open('cache/cache_Event_new.json', 'w') as json_file:
                        json_file.write(cache_Event_json) 
                    ValueError('Error occur in getBasicAnnotationsFromEVENTS()')

                cache_Event[lang][hash_value] = {}
                cache_Event[lang][hash_value]['text'] = text #the raw text is not included in the return of getMULTILANG_EDL(lang,text)
                cache_Event[lang][hash_value]['res_json'] = annjsonEvents
                cache_Event[lang][hash_value]['token'] = t
                cache_Event[lang][hash_value]['end_pos'] = s
                print('The ' + str(i) +'th sample')
                print(text)
        
        cache_Event_json = json.dumps(cache_Event, indent=4)
        with open('cache/cache_EE.json', 'w') as json_file:
            json_file.write(cache_Event_json) 
        