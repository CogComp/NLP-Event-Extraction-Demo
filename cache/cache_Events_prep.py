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
        "At least seven historically Black colleges and universities (HBCUs) across the United States received back-to-back bomb threats this week, forcing students to evacuate or shelter in place while authorities investigated. The threats come amid a dramatic rise in bombings in the US and follow bomb threats at other US colleges last November.",
        "Police arrested seven rioters in The Hague on Saturday night after youths set fires in the streets and threw fireworks at officers. The unrest came a day after police opened fire on protesters in violence that broke out at a protest against coronavirus restrictions.",
        "The World Health Organization on Wednesday declared the novel coronavirus outbreak a pandemic. There are 118,000 cases, more than 4,000 deaths, the agency said, and the virus has found a foothold on every continent except for Antarctica.",
        "The number of people already infected by the mystery virus emerging in China is far greater than official figures suggest, scientists have told the BBC. There have been more than 60 confirmed cases of the new coronavirus, but UK experts estimate a figure nearer 1,700. Two people are known to have died from the respiratory illness, which appeared in Wuhan city in December.",
        "A short drive away, Ismokoweni, who leads 'Aisyiyah's local environmental chapter and goes by one name, picks her way past painted gravestones towards an area of damaged forest where the group has also planted seedlings.",
        "Two states - Karnataka, which includes tech hub Bengaluru, and Maharashtra, which includes Mumbai - have announced they will temporarily suspend vaccination for people aged 18-44 years as they prioritize those over 45 who need their second dose.",
        "A firefighter and his crew battled to keep the raging Glass Fire from devastating an upmarket Napa Valley vineyard. The firefiighter denies lighting backfires which consume fuel in a wildfire's path but admits his team failed to advise Cal Fire, the state's fire agency that it was in the evacuated area, as required by law.",
        "The incident highlights how a booming business in private firefighting is creating friction with government firefighters as wildfires grow more frequent and dangerous across the western US. It also underscores the inequity of who receives protection. Businesses and wealthy property owners have growing options to protect themselves, for a price. Meanwhile, homeowners across California are being denied homeowner's insurance renewals because of wildfire risk.",
        "According to the US justice department, at about noon that day several of the contractors opened fire in and around Nisoor Square, a busy roundabout that was immediately adjacent to the heavily-fortified Green Zone.",
        "US prosecutors said Slatten was the first to fire, without provocation, killing Ahmed Haithem Ahmed Al Rubiay, an aspiring doctor who was driving his mother to an appointment. The contractors said they mistakenly believed that they were under attack. The incident caused international outrage, strained relations between the US and Iraq, and sparked a debate over the role of contractors in warzones.",
        "In 2014, a US federal court found Slatten guilty of murder, while Slough, Liberty and Heard were convicted of voluntary manslaughter, attempted manslaughter and other charges. Slatten was sentenced to life in prison, and the other three were handed 30-year terms."
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
        
