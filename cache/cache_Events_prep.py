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
		"There were at least 40 tornadoes reported across nine states between Friday night and early Saturday morning in the United States. Kentucky was the worst-hit state, with at least 64 confirmed fatalities.",
		"There were at least 40 tornadoes reported across nine states between Friday night and early Saturday morning in the United States.",
		"The tornadoes destroyed many houses.",
        "The devastated family of a Brooklyn fifth-grader who died suddenly last week in the wake of several incidents of what relatives described as school bullying demanded answers Friday from education and health officials on how the tragedy unfolded.",
		"A short drive away, Ismokoweni, who leads 'Aisyiyah's local environmental chapter and goes by one name, picks her way past painted gravestones towards an area of damaged forest where the group has also planted seedlings.",
		"Media reports on suicides should also be cautious, because a large number of foreign studies have suggested that inappropriate media coverage can encourage imitation.",
		"Two states - Karnataka, which includes tech hub Bengaluru, and Maharashtra, which includes Mumbai - have announced they will temporarily suspend vaccination for people aged 18-44 years as they prioritize those over 45 who need their second dose.",
		"Pope Urban II encouraged military support for Byzantine Emperor Alexios I against the Seljuk Turks and an armed pilgrimage to Jerusalem. Volunteers took a public vow to join the crusade. Historians now debate the combination of their motivations, which included the prospect of mass ascension into Heaven at Jerusalem, satisfying feudal obligations, opportunities for renown, and economic and political advantage.",
		"A firefighter and his crew battled to keep the raging Glass Fire from devastating an upmarket Napa Valley vineyard. The firefiighter denies lighting backfires which consume fuel in a wildfire's path but admits his team failed to advise Cal Fire, the state's fire agency that it was in the evacuated area, as required by law.",
		"The incident highlights how a booming business in private firefighting is creating friction with government firefighters as wildfires grow more frequent and dangerous across the western US. It also underscores the inequity of who receives protection. Businesses and wealthy property owners have growing options to protect themselves, for a price. Meanwhile, homeowners across California are being denied homeowner's insurance renewals because of wildfire risk.",
		"The bombers blew themselves up among a crowd of shoppers at a second-hand clothes market in Tayaran Square. The last deadly suicide attack in the city was in January 2018, when 35 people were killed in the same square. No group has said it carried out the latest attack, but suspicion will fall on the jihadist group Islamic State. The Iraqi government declared victory in its war against IS at the end of 2017. However, sleeper cells continue to wage a low-level insurgency in the country, operating mainly in rural areas and targeting security forces.",
		"According to the US justice department, at about noon that day several of the contractors opened fire in and around Nisoor Square, a busy roundabout that was immediately adjacent to the heavily-fortified Green Zone.",
		"US prosecutors said Slatten was the first to fire, without provocation, killing Ahmed Haithem Ahmed Al Rubiay, an aspiring doctor who was driving his mother to an appointment. The contractors said they mistakenly believed that they were under attack. The incident caused international outrage, strained relations between the US and Iraq, and sparked a debate over the role of contractors in warzones.",
		"Several witnesses insisted that the contractors had panicked and opened fire indiscriminately.",
		"In 2014, a US federal court found Slatten guilty of murder, while Slough, Liberty and Heard were convicted of voluntary manslaughter, attempted manslaughter and other charges. Slatten was sentenced to life in prison, and the other three were handed 30-year terms.",
		"Boris Johnson has condemned the \"shameful racism\" aimed at British Jews, after a video appeared to show people shouting anti-Semitic abuse. It comes amid rising tension between Israel and Palestinians in the Middle East, culminating in the worst violence since 2014.",
		"Within weeks, China had managed to test 9 million people for SARS-CoV-2 in Wuhan. It set up an effective national system of contact tracing.Across the country, 14000 health checkpoints were established at public transport hubs. By contrast, the UK's capacity for contact tracing was overwhelmed soon after the pandemic struck the country.",
		"My research suggests that the control of the virus in China is not the result of authoritarian policy, but of a national prioritization of health. China learned a tough lesson with SARS, the first coronavirus pandemic of the 21st century.",
		"The latest conflict continues to rapidly escalate between Israel and Hamas. Both sides are sticking to their own argument over how the conflict started.",
		"A suspected suicide bomb attack outside a Catholic church has left at least 14 people wounded. A destroyed motorbike and body parts were found at the scene and police said the two attackers had died. Militant Islamists have attacked churches in the past but no group has yet said it was behind the bombing.",
		"There were two people riding on a motorbike when the explosion happened at the main gate of the church. Footage from security cameras showed fire, smoke and debris being blown into the middle of the road.",
		"The goverment has banned public schools from making religious attire compulsory, after the story of a Christian student being pressured to wear a headscarf in class went viral. The 16-year-old girl was attending a school that had a rule that all students had to wear the Muslim headscarf. The government has given schools 30 days to revoke any existing rules. But there are growing concerns about rising religious intolerance. The ban was signed into decree on Wednesday, and schools which do not comply may face sanctions.",
		"We all know what a Mad Hatter's tea party looks like, can liken hapless pairs to Tweedledum and Tweedledee, or a big grin to a Cheshire cat. The image of a little blonde girl in a blue dress and an Alice band is always and inevitably, well, Alice. (Yes, the headband is named after her).",
		"A tuk-tuk driver wants to do his bit to help his fellow citizens weather the pandemic. So, he has turned his humble vehicle into an ambulance, ferrying people to and from hospitals for free. This is a huge help given the shortage of ambulances as the city struggles against a deadly second wave of Covid-19. Cases have risen rapidly in the past month, leading to an acute shortage of hospital beds, medicines and oxygen. The crisis has also contributed to a sharp increase in Covid deaths."]
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
        
