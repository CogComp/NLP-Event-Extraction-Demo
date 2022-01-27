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
       "The eruption of an underwater volcano near Tonga on Saturday was likely the biggest recorded anywhere on the planet in more than 30 years, according to experts. Dramatic images from space captured the eruption in real time, as a huge plume of ash, gas and steam was spewed up to 20 kilometers into the atmosphere and tsunami waves were sent crashing across the Pacific.",
        "Crews fighting a massive fire along the central coast of California near the iconic Highway 1 made progress Sunday in containing the blaze, but dozens of homes remained under evacuation orders. The Colorado fire ignited Friday evening in Palo Colorado Canyon in the Big Sur region of Monterey County and swelled to 1050 acres Saturday, up from 100 acres a day prior.", 
        "At least seven historically Black colleges and universities (HBCUs) across the United States received back-to-back bomb threats this week, forcing students to evacuate or shelter in place while authorities investigated. The threats come amid a dramatic rise in bombings in the US and follow bomb threats at other US colleges last November.",
        "Pfizer and BioNTech have begun a clinical trial for their Omicron-specific Covid-19 vaccine candidate, they announced in a news release on Tuesday. The study will evaluate the vaccine for safety, tolerability and the level of immune response, as both a primary series and a booster dose, in up to 1420 healthy adults ages 18 to 55.",
        "The number of people already infected by the mystery virus emerging in China is far greater than official figures suggest, scientists have told the BBC. There have been more than 60 confirmed cases of the new coronavirus, but UK experts estimate a figure nearer 1700. Two people are known to have died from the respiratory illness, which appeared in Wuhan city in December.",
        "The World Health Organization on Wednesday declared the novel coronavirus outbreak a pandemic. There are 118000 cases, more than 4000 deaths, the agency said, and the virus has found a foothold on every continent except for Antarctica.",
        "With the justices sheltering at home, the Supreme Court had been shut down to live arguments until this past October. The court remains closed to the public, and lawyers arguing in the court have to be masked and provide proof of a negative Covid test. Omicron is still ravaging America, and the military has been dispatched to help overwhelmed hospitals. Yet on Thursday the Supreme Court conservative majority struck down the temporary vaccine mandate for large businesses proposed by the Occupational Safety and Health Administration and sided with Covid19, thereby guaranteeing that the pandemic will continue into a third year of misery for Americans.",
        "A firefighter and his crew battled to keep the raging Glass Fire from devastating an upmarket Napa Valley vineyard. The firefighter denies lighting backfires which consume fuel in a wildfire's path but admits his team failed to advise Cal Fire, the state's fire agency that it was in the evacuated area, as required by law.",
        "The incident highlights how a booming business in private firefighting is creating friction with government firefighters as wildfires grow more frequent and dangerous across the western US. It also underscores the inequity of who receives protection. Businesses and wealthy property owners have growing options to protect themselves, for a price. Meanwhile, homeowners across California are being denied homeowner's insurance renewals because of wildfire risk."

]
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
        print("Successfully loaded cache from cache_" + name + ".json")
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
            print("Starting to generate Event annotations of language : " + lang)
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
                    print('Sample ' + str(count) + ' has been added to cache_Event')

        cache_Event_json = json.dumps(cache_Event, indent=4)
        with open('cache_EE.json', 'w') as json_file:
            json_file.write(cache_Event_json)

        print("Successfully created cache_Event!!!")
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
                print(f"Warning: sample no. {i + 1} is already in cache_Events, skip to next sample!")
                pass
            else:
                try:
                    t,s,annjsonEvents = getBasicAnnotationsFromEVENTS(text)
                except:
                    cache_Event_json = json.dumps(cache_Event, indent=4)
                    with open('cache/cache_Event_new.json', 'w') as json_file:
                        json_file.write(cache_Event_json) 
                    ValueError('Error occured in getBasicAnnotationsFromEVENTS()')

                cache_Event[lang][hash_value] = {}
                cache_Event[lang][hash_value]['text'] = text #the raw text is not included in the return of getMULTILANG_EDL(lang,text)
                cache_Event[lang][hash_value]['res_json'] = annjsonEvents
                cache_Event[lang][hash_value]['token'] = t
                cache_Event[lang][hash_value]['end_pos'] = s
                print('The sample no.' + str(i + 1) +' : ')
                print(text)
        
        cache_Event_json = json.dumps(cache_Event, indent=4)
        with open('cache/cache_EE.json', 'w') as json_file:
            json_file.write(cache_Event_json) 
        
