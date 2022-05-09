import cherrypy
import os
import json
import requests
import tabular

import sys
import hashlib
import cacheEventExtract
from datetime import datetime
from time import time


################################ Sys parameters ###############################
serviceURL = sys.argv[1]
servicePort = int(sys.argv[2])

################################ Cache Loading ################################
# Instantiate Cache Class
cache = cacheEventExtract.CacheEventExtraction()
        
cache_EE = cache.load("EE")

################################ Server Path ###############################
BASE_HTML_PATH = "./EVENTS_html"
BASE_KAIROS_NER_HTTP = "http://dickens.seas.upenn.edu:4022/ner"
BASE_KAIROS_SRL_HTTP = "http://dickens.seas.upenn.edu:4039/annotate"
# BASE_KAIROS_EVENTS_HTTP = "http://leguin.seas.upenn.edu:4023/annotate"
BASE_KAIROS_EVENTS_HTTP = "http://dickens.seas.upenn.edu:4048/annotate"
BASE_KAIROS_TEMPORAL_HTTP = "http://leguin.seas.upenn.edu:4024/annotate"
BASE_KAIROS_STORYLINE_HTTP = "http://leguin.seas.upenn.edu:4025/annotate"


'''
def getBasicAnnotations(text):
    # input = {"task":"mention_detection","text":text}
    input = {"task":"kairos_ner","text":text}
    # res_out = requests.get(BASE_KAIROS_NER_HTTP, params = input)
    res_out_NER = requests.post(BASE_KAIROS_NER_HTTP,json=input)
    print('(1)BASE_KAIROS_NER_HTTP was used!!!!!!!!!!!!!!!!!!!!!')
    # print(res_out)
    res_json_NER = res_out_NER.json()
    #print("----------")
    #print(res_json_NER)
    #print("----------")
    # SRL
    input = {"sentence":text}
    res_out_SRL = requests.post(BASE_KAIROS_SRL_HTTP, json = input)
    print('(2)BASE_KAIROS_SRL_HTTP was used!!!!!!!!!!!!!!!!!!!!!')
    res_json_SRL = res_out_SRL.json()
    tokens = []
    endPositions = []
    if "tokens" in res_json_SRL:
        tokens = res_json_SRL["tokens"]
    # print(tokens)
    if "sentences" in res_json_SRL:
        sentences = res_json_SRL["sentences"]
        if "sentenceEndPositions" in sentences:
            endPositions = sentences["sentenceEndPositions"]
    return tokens, endPositions, res_json_NER, res_json_SRL

def getSRL(text):
    input = {"sentence":text}
    res_out = requests.post(BASE_KAIROS_SRL_HTTP, json = input)
    print('(2，2)BASE_KAIROS_SRL_HTTP was used!!!!!!!!!!!!!!!!!!!!!')
    # print(res_out.text)
    # res_json = json.loads(res_out.text)
    return res_out.json()
'''
'''
def getNER_ONTONOTES(text):
    input = {"views":"NER_ONTONOTES","text":text}
    res_out = requests.get(BASE_COGCOMP_HTTP, params = input)
    # print(res_out.text)
    res_json = json.loads(res_out.text)
    return res_json

def getSRL_VERB(text):
    input = {"views":"SRL_VERB","text":text}
    res_out = requests.get(BASE_COGCOMP_HTTP, params = input)
    # print(res_out.text)
    res_json = json.loads(res_out.text)
    return res_json

def getSRL_NOM(text):
    input = {"views":"SRL_NOM","text":text}
    res_out = requests.get(BASE_COGCOMP_HTTP, params = input)
    # print(res_out.text)
    res_json = json.loads(res_out.text)
    return res_json

def getSRL_PREP(text):
    input = {"views":"SRL_PREP","text":text}
    res_out = requests.get(BASE_COGCOMP_HTTP, params = input)
    # print(res_out.text)
    res_json = json.loads(res_out.text)
    return res_json

def getRELATION(text):
    input = {"views":"RELATION","text":text}
    res_out = requests.get(BASE_COGCOMP_HTTP, params = input)
    # print(res_out.text)
    res_json = json.loads(res_out.text)
    return res_json

def getTIMEX3(text):
    input = {"views":"TIMEX3","text":text}
    res_out = requests.get(BASE_COGCOMP_HTTP, params = input)
    # print(res_out.text)
    res_json = json.loads(res_out.text)
    return res_json
'''

def getBasicAnnotationsFromEVENTS(text,lang="eng"):
    # start_time = time()
    global cache_EE
    verb_srl = {}
    hash_value = hashlib.sha1(text.encode()).hexdigest()
    
    if cache.count(cache_EE) > 200:
        cache.write('EE', cache_EE)
        cache_EE = cache.load('EE')
    
    if hash_value in cache_EE[lang].keys():
        tokens, endPositions, res_json, cache_EE = cache.read('Event', cache_EE, lang, hash_value)
        return tokens, endPositions, res_json, verb_srl

    else:
        input = {"text":text}
        headers = {'Content-type': 'application/json'}
        start_time = time()
        # res_out = requests.post(BASE_KAIROS_EVENTS_HTTP, json = input)
        # res_out = requests.post(BASE_KAIROS_EVENTS_HTTP, 
        #     json={"text": text, "task": "event_verb"}, headers=headers)
        res_out = requests.post(BASE_KAIROS_EVENTS_HTTP, 
            json={"text": text, "task": "include_verb_srl"}, headers=headers)
        print("\nProcessing Time for Event Extraction: ", time() - start_time)
        print("(3)BASE_KAIROS_EVENTS_HTTP was used!!!!!!!!!!!!!!!")

        #print("=======================")
        #print(res_out.text)
        #print("=======================")
        # res_json = json.loads(res_out.text)
        res_jsons = res_out.json()
        res_json = res_jsons["result"]
        verb_srl = res_jsons["verb_srl_temporal"]
        # print(verb_srl)
        
        tokens = []
        endPositions = []

        if "tokens" in res_json:
            tokens = res_json["tokens"]
        # print(tokens)
        if "sentences" in res_json:
            sentences = res_json["sentences"]
            if "sentenceEndPositions" in sentences:
                endPositions = sentences["sentenceEndPositions"]
        
        cache_EE = cache.add('Event', cache_EE, lang, text, hash_value, res_json, tokens, endPositions)
        # print("\nProcessing Time for Event Extraction: ", time() - start_time)
        return tokens, endPositions, res_json, verb_srl

'''
def getEVENTS(text):
    input = {"text":text}
    res_out = requests.post(BASE_KAIROS_EVENTS_HTTP, json = input)
    #print("=======================")
    #print(res_out.text)
    #print("=======================")
    # res_json = json.loads(res_out.text)
    return res_out.json()
'''
def getSTORYLINE(events_json, text=None):
    # start_time = time()
    global cache_EE
    lang="eng"
    hash_value = hashlib.sha1(text.encode()).hexdigest()

    if hash_value in cache_EE[lang].keys():
        try:
            res_out_json, cache_EE = cache.read('Coref', cache_EE, lang, hash_value)
                       
        except:
            input = events_json
            print("==== STORYLINE =====")
            start_time = time()
            res_out = requests.post(BASE_KAIROS_STORYLINE_HTTP, json = input)
            print("\nProcessing Time for Coref: ", time() - start_time)
            print("(5)BASE_KAIROS_STORYLINE_HTTP was used!!!!!!!!!!!!!!!")
            text = res_out.text
            if text.strip() == "" or text.strip() is None:
                return events_json
            res_out_json = json.loads(res_out.text)
            newRelations = []
            for v in res_out_json["views"]:
                if v["viewName"] == "Event_extraction":
                    vDataRels = v["viewData"][0]["relations"]
                    for r in vDataRels:
                        if r["relationName"] == "coref": # and r["srcConstituent"] < r["targetConstituent"]:
                            newRelations.append(r)
                    v["viewData"][0]["relations"] = newRelations
            cache_EE = cache.add('Coref', cache_EE, lang, text, hash_value, res_out_json)

    else:
        input = events_json
        print("==== STORYLINE =====")
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
        cache_EE = cache.add('Coref', cache_EE, lang, text, hash_value, res_out_json)
    # print("\nProcessing Time for Coref: ", time() - start_time)
    return res_out_json # res_out.json()

'''
def getTEMPORAL_OLD(eventsOutput):
    input = eventsOutput
    print("==== TEMPORAL =====")
    # print(eventsOutput)
    # res_out = requests.post(BASE_KAIROS_TEMPORAL_HTTP, data = input)
    res_out = requests.post(BASE_KAIROS_TEMPORAL_HTTP, json = input)
    # print("==== res_out.text =====")
    # print(res_out.text)
    print("res_out.text",res_out.text)
    res_out_json = json.loads(res_out.text)
    # print("==== res_out.json =====")
    # print(res_out.json())
    # print("=======================")
    
    # REMOVE EVENTS - keep BEFORE/AFTER (source < target)
    newRelations = []
    for v in res_out_json["views"]:
        if v["viewName"] == "Event_extraction":
            vDataRels = v["viewData"][0]["relations"]
            for r in vDataRels:
                if r["relationName"] in ["before","after"] and r["srcConstituent"] < r["targetConstituent"]:
                    newRelations.append(r)
            v["viewData"][0]["relations"] = newRelations
    
    # res_json = json.loads(res_out.text)
    return res_out_json # {} # res_out.json()
'''
def getTEMPORAL(eventsOutput, verb_srl, text=None):  #add 'text' argument for checking if the Temporal annotations of the text has already existed.
    # start_time = time()
    global cache_EE
    lang="eng"
    hash_value = hashlib.sha1(text.encode()).hexdigest()
    print("verb_srl: ", verb_srl)
    if hash_value in cache_EE[lang].keys():
        try:
            res_out_json, cache_EE = cache.read('Temporal', cache_EE, lang, hash_value)
                       
        except:
            headers = {'Content-type': 'application/json'}
            input = eventsOutput
            print("==== TEMPORAL =====")
            start_time = time()
            # res_out = requests.post(BASE_KAIROS_TEMPORAL_HTTP, json = input)
            res_out = requests.post(BASE_KAIROS_TEMPORAL_HTTP, json={"eventsOutput": eventsOutput, "verb_srl": verb_srl}, headers=headers)
            print("\nProcessing Time for Temporal: ", time() - start_time)
            print('(4) BASE_KAIROS_TEMPORAL_HTTP!!!!!!!!!!!!!!!!!!!!!!!!')
            print("res_out.text",res_out.text)
            res_out_json = json.loads(res_out.text)
            cache_EE = cache.add('Temporal', cache_EE, lang, text, hash_value, res_out_json)
        
    else:
        input = eventsOutput
        print("==== TEMPORAL =====")
        print("\n\n", "*"*100)
        # print(eventsOutput)
        headers = {'Content-type': 'application/json'}
        # res_out = requests.post(BASE_KAIROS_TEMPORAL_HTTP, data = input)
        start_time = time()
        # res_out = requests.post(BASE_KAIROS_TEMPORAL_HTTP, json = input)
        res_out = requests.post(BASE_KAIROS_TEMPORAL_HTTP, 
            json={"eventsOutput": eventsOutput, "verb_srl": verb_srl}, headers=headers)
        print("\nProcessing Time for Temporal: ", time() - start_time)
        print('(4) BASE_KAIROS_TEMPORAL_HTTP!!!!!!!!!!!!!!!!!!!!!!!!')
        # print("==== res_out.text =====")
        # print(res_out.text)
        print("res_out.text",res_out.text)
        res_out_json = json.loads(res_out.text)
        # print("==== res_out.json =====")
        # print(res_out.json())
        # print("=======================")
        
        '''
        # REMOVE EVENTS - keep BEFORE/AFTER (source < target)
        newRelations = []
        for v in res_out_json["views"]:
            if v["viewName"] == "Event_extraction":
                vDataRels = v["viewData"][0]["relations"]
                for r in vDataRels:
                    if r["relationName"] in ["before","after"] and r["srcConstituent"] < r["targetConstituent"]:
                        newRelations.append(r)
                v["viewData"][0]["relations"] = newRelations
        ''' 
        # res_json = json.loads(res_out.text)
        cache_EE = cache.add('Temporal', cache_EE, lang, text, hash_value, res_out_json)
    # print("\nProcessing Time for Temporal: ", time() - start_time)
    return res_out_json # {} # res_out.json()

def initView(myTabularView,text):
    myTabularView.setText(text)
    # t,s,annjsonNER,annjsonSRL = getBasicAnnotations(text)
    t,s,annjsonEvents,verb_srl = getBasicAnnotationsFromEVENTS(text)
    print("*"*100)
    print("verb_srl: \n", verb_srl)
    myTabularView.setTokens( t )
    myTabularView.setSentenceEnds( s )
    #print("====")
    #print(annjson["tokens"])
    #print("====")
    '''
    if "tokens" in annjson:
        tokens = annjson["tokens"]
        if len(tokens) != len(myTabularView.getTokens()): return
        myTabularView.addSpanLabelView(annjson,"NER_CONLL","NER-CONLL")
    '''
    return annjsonEvents,verb_srl
'''
#def processNER(myTabularView,text):
def processNER(myTabularView,annjson):
    # annjson = getNER_ONTONOTES(text)
    if "tokens" in annjson:
        tokens = annjson["tokens"]
        #print("===")
        #print(tokens)
        #print("===")
        #print(annjson)
        #print("===")
        # if len(tokens) != len(myTabularView.getTokens()): return
        myTabularView.addSpanLabelView(annjson,"NER_CONLL","NER-CONLL")

# def processSRL(myTabularView,text):
def processSRL(myTabularView,annjson):
    # annjson = getSRL(text)
    if "tokens" in annjson:
        tokens = annjson["tokens"]
        # if len(tokens) != len(myTabularView.getTokens()): return
        myTabularView.addPredicateArgumentView(annjson,"SRL_ONTONOTES","SRL-Verb")
        myTabularView.addPredicateArgumentView(annjson,"SRL_NOM","SRL-Nom")
        myTabularView.addPredicateArgumentView(annjson,"SRL_NOM_ALL","SRL-Nom-ALL")
        myTabularView.addPredicateArgumentView(annjson,"PREPOSITION_SRL","SRL-Prep")
'''
'''

def processREL(myTabularView,text):
    annjson = getRELATION(text)
    if "tokens" in annjson:
        tokens = annjson["tokens"]
        if len(tokens) != len(myTabularView.getTokens()): return
        myTabularView.addRelationView(annjson,"RELATION","Relation")

def processTIM(myTabularView,text):
    annjson = getTIMEX3(text)
    if "tokens" in annjson:
        tokens = annjson["tokens"]
        if len(tokens) != len(myTabularView.getTokens()): return
        myTabularView.addSpanLabelView(annjson,"TIMEX3","Timex3")
'''


'''
def processEVENTS(myTabularView,text):
    annjson = getEVENTS(text)
    #try:
    #annjson = getSTORYLINE(annjson)
    #except:
    #    None
    #print("====")
    #print(annjson)
    #print("====")
    if "tokens" in annjson:
        tokens = annjson["tokens"]
        # if len(tokens) != len(myTabularView.getTokens()): return
        myTabularView.addRelationView(annjson,"Event_extraction","Events")
    return annjson
'''
def processEVENTS(myTabularView,annjson):
    # annjson = getEVENTS(text)
    #try:
    #annjson = getSTORYLINE(annjson)
    #except:
    #    None
    #print("====")
    #print(annjson)
    #print("====")
    if "tokens" in annjson:
        tokens = annjson["tokens"]
        # if len(tokens) != len(myTabularView.getTokens()): return
        # myTabularView.addRelationView(annjson,"Event_extraction","OLD")
    hasEvents = False
    event_extraction_view = {}
    if "views" in annjson:
        for v in annjson["views"]:
            if v["viewName"] == "Event_extraction" and "viewData" in v:
                if "relations" in v["viewData"][0]:
                    if len(v["viewData"][0]["relations"]) > 0:
                        hasEvents = True
                        event_extraction_view = v["viewData"][0]
    return annjson, hasEvents, event_extraction_view

'''
def processTEMPORAL_OLD(myTabularView,eventsOutput):
    annjson = getTEMPORAL(eventsOutput)
    #print("====")
    #print(annjson)
    #print("====")
    if "tokens" in annjson:
        tokens = annjson["tokens"]
        # if len(tokens) != len(myTabularView.getTokens()): return
        myTabularView.addRelationView(annjson,"Event_extraction","Temporal")
'''
def processTEMPORAL(myTabularView,eventsOutput, verb_srl, text=None):
    annjson = getTEMPORAL(eventsOutput, verb_srl, text)
    # print("*"*100)
    #print("====")
    #print(annjson)
    #print("====")
    if "tokens" in annjson:
        tokens = annjson["tokens"]
        # if len(tokens) != len(myTabularView.getTokens()): return
        # myTabularView.addTemporalView(annjson,"Event_extraction","Temporal")
    tmp_view = {}
    temporal_view = []
    if "views" in annjson:
        for v in annjson["views"]:
            if v["viewName"] == "Event_extraction" and "viewData" in v:
                if "relations" in v["viewData"][0]:
                    if len(v["viewData"][0]["relations"]) > 0:
                        tmp_view = v["viewData"][0]
    for r in v["viewData"][0]["relations"]:
        if r["relationName"] in ["after","before"]:
            temporal_view.append ( r )
    return annjson, temporal_view

'''
def processSTORYLINE(myTabularView,eventsOutput):
    annjson = getSTORYLINE(eventsOutput)
    #print("====")
    #print(annjson)
    #print("====")
    if "tokens" in annjson:
        tokens = annjson["tokens"]
        # if len(tokens) != len(myTabularView.getTokens()): return
        myTabularView.addRelationView(annjson,"Event_extraction","Coref")
'''

def processCOREF(myTabularView,eventsOutput,text=None):
    annjson = getSTORYLINE(eventsOutput, text)
    #print("====")
    #print(annjson)
    #print("====")
    if "tokens" in annjson:
        tokens = annjson["tokens"]
        # if len(tokens) != len(myTabularView.getTokens()): return
        # myTabularView.addTemporalView(annjson,"Event_extraction","Temporal")
    tmp_view = {}
    coref_view = []
    if "views" in annjson:
        for v in annjson["views"]:
            if v["viewName"] == "Event_extraction" and "viewData" in v:
                if "relations" in v["viewData"][0]:
                    if len(v["viewData"][0]["relations"]) > 0:
                        tmp_view = v["viewData"][0]
    for r in v["viewData"][0]["relations"]:
        if r["relationName"] == "coref":
            coref_view.append ( r )
    return annjson, coref_view

def doProcess(myTabularView, text=None, anns=None):
    eventsOutput = None
    myTabularView.reset()
    # annjsonNER,annjsonSRL = initView(myTabularView, text)
    annjsonEvents, verb_srl = initView(myTabularView, text)
    # print("\n\nannjsonEvents", "*"*10)
    # print("verb_srl: ", verb_srl)
    
    hasEvents = False
    for ann in anns:
        if ann == "EVENTS": 
            # eventsOutput = processEVENTS(myTabularView, text)
            eventsOutput, hasEvents, event_extraction_view = processEVENTS(myTabularView, annjsonEvents)
            print("hasEvents",hasEvents)
            if hasEvents:
                mainEvents = {}
                for constIndex in range(len(event_extraction_view["constituents"])):
                    constituent = event_extraction_view["constituents"][constIndex]
                    if "properties" in constituent and "predicate" in constituent["properties"]:
                        if constIndex not in mainEvents:
                            mainEvents[constIndex] = event_extraction_view["constituents"][constIndex]
                
                for relation in event_extraction_view["relations"]:
                    if relation["srcConstituent"] not in mainEvents:
                        mainEvents[relation["srcConstituent"]] = event_extraction_view["constituents"][relation["srcConstituent"]]
                print("-- main events --")
                print(json.dumps(mainEvents))
                myTabularView.addEventsView(mainEvents,"Events")
                argsList = []
                for relation in event_extraction_view["relations"]:
                    #if relation["targetConstituent"] not in argsList:
                    #    argsList[relation["targetConstituent"]] = event_extraction_view["constituents"][relation["targetConstituent"]]
                    #    argsList[relation["targetConstituent"]]["srcs"] = []
                    arg = { "constituent":event_extraction_view["constituents"][relation["targetConstituent"]] , "source":relation["srcConstituent"] }
                    argsList.append( arg )
                    #if relation["srcConstituent"] not in argsList[relation["targetConstituent"]]["srcs"]:
                    #    argsList[relation["targetConstituent"]]["srcs"].append( relation["srcConstituent"] )
                print("-- event args --")
                print(json.dumps(argsList))
                myTabularView.addEventsArgsView(mainEvents,argsList,"Arguments")
            
        # if ann == "NER": processNER(myTabularView, annjsonNER)
        # if ann == "SRL": processSRL(myTabularView, annjsonSRL)
        # if ann == "REL": processREL(myTabularView, text)
        if hasEvents:
            if ann == "TEMPORAL" and eventsOutput is not None: 
                #print("--")
                #print("Running TEMPORAL...")
                #processTEMPORAL(myTabularView, eventsOutput)
                temporalOutput, temporalView = processTEMPORAL(myTabularView, annjsonEvents, verb_srl, text)
                print("-- temporalView --")
                print(json.dumps(temporalView))
                myTabularView.addTemporalView(mainEvents,temporalView,"Temporal")
                
            if ann == "STORYLINE" and eventsOutput is not None: 
                #print("--")
                #print("Running TEMPORAL...")
                #processSTORYLINE(myTabularView, eventsOutput)
                corefOutput, corefView = processCOREF(myTabularView, annjsonEvents, text)
                print("-- corefView --")
                print(json.dumps(corefView))
                myTabularView.addCorefView(mainEvents,corefView,"Coref")
                
        # if ann == "TIM": processTIM(myTabularView, text)
    # return json.dumps( myTabularView.getTokens() )
    return myTabularView.HTML()

class MyWebService(object):

    _myTabularView = None
    
    @cherrypy.expose
    def index(self):
        return open(BASE_HTML_PATH+'/index.php')

    def html(self):
        pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def info(self, **params):
        return {"status":"online"}

    @cherrypy.expose
    def halt(self, **params):
        cherrypy.engine.exit()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def view(self, text=None, anns=None):
        print("Current Time: ", datetime.now())
        start_time = time()
        input = { "text" : None , "anns" : [] }
        try:
            data = cherrypy.request.json
        except:
            data = cherrypy.request.params
        if "text" in data: input["text"] = data["text"]
        if "anns" in data: input["anns"] = data["anns"]
        # print(">>>>>>>>>", data["text"])
        self._myTabularView = tabular.TabularView()
        # print("*"*100)
        # data["text"] = preprocess_input_text(data["text"], multi=True, special_char="convert", char_list=special_char_list)

        html = doProcess(self._myTabularView, data["text"] , data["anns"])
        result = {"input": input, "html": html}
        print("\nTotal Processing Time: ", time() - start_time)
        return result

    def showCache(self):
        result = cache_EE
        return result

if __name__ == '__main__':
    print ("")
    print ("Starting 'CogComp' rest service...")
    config = {'server.socket_host': serviceURL}
    cherrypy.config.update(config)
    config = {
      'global' : {
        'server.socket_host' : serviceURL,#'leguin.seas.upenn.edu',
        'server.socket_port' : servicePort, #4021,
        'cors.expose.on': True
      },
      '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())

      },
      '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': BASE_HTML_PATH
      },
      '/html' : {
        'tools.staticdir.on'    : True,
        'tools.staticdir.dir'   : BASE_HTML_PATH,
        'tools.staticdir.index' : 'index.html',
        'tools.gzip.on'         : True
      },
    }
    cherrypy.config.update(config)
    cherrypy.quickstart(MyWebService(), '/', config)

    cache.write('EE', cache_EE)
