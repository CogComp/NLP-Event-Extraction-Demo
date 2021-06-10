import json 

def getAnnView(textAnnViews = {},annViewName = ''):
    if "views" in textAnnViews:
        for v in textAnnViews["views"]:
            if v["viewName"] == annViewName:
                return v
    return None

def getAnnConstituents(annView = {}):
    if "viewData" in annView:
        if "constituents" in annView["viewData"][0]:
            return annView["viewData"][0]["constituents"]
    return None
    
def getAnnRelations(annView = {}):
    if "viewData" in annView:
        if "relations" in annView["viewData"][0]:
            return annView["viewData"][0]["relations"]
    return None
    

class TabularRow():
    cells = []
    lastTokenUsed = 0
    def __init__(self,noTokens=0):
        # print (">>>>>>>>>>>>>>>>>>", noTokens)
        self.cells = []
        self.lastToken = 0
        for c in range(noTokens):
            self.cells.append(TabularCell())

class TabularCell():
    text = ""
    css = None
    colSpan = -1
    hidden = False
    border_left = False
    border_right = False
    def __init__(self):
        self.text = ""
        self.css = None
        self.colSpan = -1
        self.hidden = False
        self.border_left = False
        self.border_right = False

def markBorders(sent,annLabel,start,end):
    for aLabel in sent["anns"]:
        ann = sent["anns"][aLabel]
        for rownum in range(len(ann["rows"])):
            if aLabel != annLabel or rownum+1 < len(ann["rows"]):
                # print("aLabel",aLabel,rownum,start,end)
                row = ann["rows"][rownum]
                if not row.cells[start].text and (start == 0 or not row.cells[start-1].text): row.cells[start].border_left = True
                if end < len(row.cells):
                    if False or not row.cells[end-1].text: row.cells[end].border_left = True
                else:
                    if False or not row.cells[end-1].text: row.cells[end-1].border_right = True
        if aLabel == annLabel: return

class TabularView():
    _text = ""
    _token = []
    _annLabels = []
    _sentenceEndPositions = []
    _sentence = []

    def __init__(self):
        self._text = ""
        self._token = []
        self._annLabels = []
        self._sentenceEndPositions = []
        self._sentence = []
        self.predicateSeq = 0

    def reset(self):
        self._text = ""
        self._token = []
        self._annLabels = []
        self._sentenceEndPositions = []
        self._sentence = []
        self._relationIndex = 0
        self._eventIndex = 0

    def setText(self,text):
        self._text = text

    def getText(self):
        return self._text
        
    def setTokens(self,tokens):
        self._token = tokens

    def getTokens(self):
        return self._token

    def addAnnLabel(self,label=''):
        if not label or label == "": return False
        if label in self.getAnnLabels(): return False
        self._annLabels.append(label)
        for s in self._sentence:
            s["anns"][label] = {"rowSpan":0,"rows":[],"lastRow":None}
        return True        

    def getAnnLabels(self):
        return self._annLabels
        
    def setSentenceEnds(self,endPositions):
        self._sentenceEndPositions = endPositions
        start_token = 0
        for end_token in endPositions:
            newSentence = {}
            newSentence["start_token"] = start_token
            newSentence["end_token"] = end_token
            newSentence["tokens"] = self.getTokens()[start_token:end_token]
            newSentence["anns"] = {}
            self._sentence.append(newSentence)
            start_token = end_token

    def getSentenceEnds(self):
        return self._sentenceEndPositions

    def getSentences(self):
        return self._sentence
    
    def addLinkedSpan(self, annLabel = '', spanType = '', spanLabel = '', startToken = 0, endToken = 0, annURL = ""):
        # print(">>>>>>>", annLabel, spanLabel, startToken, endToken)
        for sidx in range(len(self._sentence)):
            s = self._sentence[sidx]
            # print(">>>>>>>", "sentence", sidx, "tokens", len(s["tokens"]))
            if annLabel in s["anns"]:
                sannlab = s["anns"][annLabel]
                # --
                start = startToken - s["start_token"]
                end = endToken - s["start_token"]
                # --
                if start >=0 and end >= 0 and start < len(s["tokens"]) and end <= len(s["tokens"]):
                    # print(">>>>>>>", "adding")
                    # print(s["tokens"])
                    row = sannlab["lastRow"]
                    if not row or row.lastTokenUsed > start:
                        row = TabularRow(len(s["tokens"]))
                        sannlab["rows"].append(row)
                        sannlab["rowSpan"] += 1
                        sannlab["lastRow"] = row
                    if annURL and annURL != "":
                        row.cells[start].text = '<a href="'+annURL+'" target="_blank">'+spanLabel+'</a>'
                    else:
                        row.cells[start].text = spanLabel
                    row.cells[start].css = "w3-border w3-round-small "+spanType
                    row.lastTokenUsed = end
                    if end-start>1: row.cells[start].colSpan = end-start
                    for i in range(start+1,end):
                        row.cells[i].hidden = True
                        row.cells[i].text = row.cells[start].text
                    markBorders(s,annLabel,start,end)
                    # print(">>>>>>>", "rows", len(sannlab["rows"]))
                    # print(">>>>>>>", "row", "cells", len(row.cells))
        return

    def addSpan(self, annLabel = '', spanType = '', spanLabel = '', startToken = 0, endToken = 0):
        # print(">>>>>>>", annLabel, spanLabel, startToken, endToken)
        for sidx in range(len(self._sentence)):
            s = self._sentence[sidx]
            # print(">>>>>>>", "sentence", sidx, "tokens", len(s["tokens"]))
            if annLabel in s["anns"]:
                sannlab = s["anns"][annLabel]
                # --
                start = startToken - s["start_token"]
                end = endToken - s["start_token"]
                # --
                if start >=0 and end >= 0 and start < len(s["tokens"]) and end <= len(s["tokens"]):
                    # print(">>>>>>>", "adding")
                    # print(s["tokens"])
                    row = sannlab["lastRow"]
                    if not row or row.lastTokenUsed > start:
                        row = TabularRow(len(s["tokens"]))
                        sannlab["rows"].append(row)
                        sannlab["rowSpan"] += 1
                        sannlab["lastRow"] = row
                    row.cells[start].text = spanLabel
                    row.cells[start].css = "w3-border w3-round-small "+annLabel+"-"+spanType
                    row.lastTokenUsed = end
                    if end-start>1: row.cells[start].colSpan = end-start
                    for i in range(start+1,end):
                        row.cells[i].hidden = True
                        row.cells[i].text = row.cells[start].text
                    markBorders(s,annLabel,start,end)
                    # print(">>>>>>>", "rows", len(sannlab["rows"]))
                    # print(">>>>>>>", "row", "cells", len(row.cells))
        return

    def addPredicates(self, annLabel = '', annPredicates = {}, annConstituents = []):
        for predicateLabel in annPredicates:
            predicate = annPredicates[predicateLabel]
            # print("*** PREDICATE ***",predicate)
            sourceIdx = predicate["sourceConstituent"]
            if type(sourceIdx) is str:
                sourceIdx = int(sourceIdx)
            source = annConstituents[sourceIdx]
            startToken = source["start"]
            endToken = source["end"]
            # print("*** TOKENS ***",startToken,endToken)
            for sidx in range(len(self._sentence)):
                s = self._sentence[sidx]
                if annLabel in s["anns"]:
                    sannlab = s["anns"][annLabel]
                    # print(s["tokens"])
                    start = startToken - s["start_token"]
                    end = endToken - s["start_token"]
                    if start >=0 and end >= 0 and start < len(s["tokens"]) and end <= len(s["tokens"]):
                        # print("*** TOKENS (in) ***",start,end)
                        # always new row for predicates
                        sannlab["rowSpan"] += 1
                        row = TabularRow(len(s["tokens"]))
                        sannlab["rows"].append(row)
                        sannlab["lastRow"] = row
                        #print("-----------------")
                        #print (predicate, start, end, len(row.cells))
                        #print("-----------------")
                        #print (source)
                        #print("-----------------")
                        if "properties" in source: 
                            row.cells[start].text = source["properties"]["predicate"]
                        else:
                            row.cells[start].text = source["label"]
                        row.cells[start].css = "w3-border w3-round-small "+annLabel+"-"+source["label"].replace("/","-")
                        if end-start>1: row.cells[start].colSpan = end-start
                        for i in range(start+1,end):
                            row.cells[i].hidden = True
                            row.cells[i].text = row.cells[start].text
                        markBorders(s,annLabel,start,end)
                        # print("***", s["anns"]["NER-Onto"]["rows"][0].cells[2].border_left)
                        # arguments now
                        for relLabel in predicate:
                            if relLabel != "sourceConstituent":
                                targetIdx = predicate[relLabel]
                                if type(targetIdx) is str:
                                    targetIdx = int(targetIdx)
                                target = annConstituents[targetIdx]
                                start = target["start"] - s["start_token"]
                                end = target["end"] - s["start_token"]
                                if start >=0 and end >= 0 and start < len(s["tokens"]) and end <= len(s["tokens"]):
                                    if row.cells[start].text: row.cells[start].text += ":"
                                    row.cells[start].text += target["label"]
                                    if not row.cells[start].text.endswith(relLabel): row.cells[start].text += ":" + relLabel
                                    if not row.cells[start].css: row.cells[start].css = "w3-border w3-round-small"
                                    row.cells[start].css += " "+annLabel+"-"+target["label"].replace("/","-")
                                    if end-start>1: row.cells[start].colSpan = end-start
                                    for i in range(start+1,end):
                                        row.cells[i].hidden = True
                                        row.cells[i].text = row.cells[start].text
                                    markBorders(s,annLabel,start,end)
        return

    def addRelations(self, annLabel = '', annPredicates = {}, annConstituents = []):
        # predicateSeq = 0
        for predicateLabel in annPredicates:
            self.predicateSeq += 1
            predicate = annPredicates[predicateLabel]
            print("*** PREDICATE ***",predicate)
            sourceIdx = predicate["sourceConstituent"]
            if type(sourceIdx) is str:
                sourceIdx = int(sourceIdx)
            source = annConstituents[sourceIdx]
            startToken = source["start"]
            endToken = source["end"]
            # print("*** TOKENS ***",startToken,endToken)
            for sidx in range(len(self._sentence)):
                s = self._sentence[sidx]
                if annLabel in s["anns"]:
                    sannlab = s["anns"][annLabel]
                    # print(s["tokens"])
                    start = startToken - s["start_token"]
                    end = endToken - s["start_token"]
                    end_source = end
                    if start >=0 and end >= 0 and start < len(s["tokens"]) and end <= len(s["tokens"]):
                        # print("*** TOKENS (in) ***",start,end)
                        # always new row for predicates
                        sannlab["rowSpan"] += 1
                        row = TabularRow(len(s["tokens"]))
                        sannlab["rows"].append(row)
                        sannlab["lastRow"] = row
                        #print("-----------------")
                        #print (predicate, start, end, len(row.cells))
                        #print("-----------------")
                        #print (source)
                        #print("-----------------")
                        '''
                        if "properties" in source: 
                            row.cells[start].text = source["properties"]["predicate"]
                        else:
                        '''
                        row.cells[start].text = "<b>["+str(self.predicateSeq)+":S]</b> " + source["label"] + ': ' + predicate["relationName"]
                        # row.cells[start].css = "w3-leftbar w3-round-large "+annLabel+"-"+source["label"].replace("/","-") # w3-border-left
                        # row.cells[end-1].css = "w3-rightbar w3-border-indigo w3-round-large "+annLabel+"-"+source["label"] # w3-border-right
                        row.cells[start].css = "w3-left-align w3-leftbar w3-round-large Relation-"+str(self._relationIndex) # annLabel+"-"+source["label"].replace("/","-") # w3-border-left 
                        if end-start>1: row.cells[start].colSpan = end-start
                        for i in range(start+1,end):
                            row.cells[i].hidden = True
                            row.cells[i].text = row.cells[start].text
                        #    
                        markBorders(s,annLabel,start,end)
                        # print("***", s["anns"]["NER-Onto"]["rows"][0].cells[2].border_left)
                        # arguments now
                        if True:
                            for relLabel in predicate:
                                if relLabel != "sourceConstituent" and relLabel != "relationName" :
                                    targetIdx = predicate[relLabel]
                                    if type(targetIdx) is str:
                                        targetIdx = int(targetIdx)
                                    target = annConstituents[targetIdx]

                                    for sidx in range(len(self._sentence)):
                                        s2 = self._sentence[sidx]
    
                                        start = target["start"] - s2["start_token"]
                                        end = target["end"] - s2["start_token"]
                                        if start >=0 and end >= 0 and start < len(s2["tokens"]) and end <= len(s2["tokens"]):
                                            '''
                                            NEW ROW NEEDED ??? True = ALWAYS
                                            '''
                                            if True or not start >= end_source:
                                                sannlab2 = s2["anns"][annLabel]
                                                sannlab2["rowSpan"] += 1
                                                row = TabularRow(len(s2["tokens"]))
                                                sannlab2["rows"].append(row)
                                                sannlab2["lastRow"] = row
                                            ### if row.cells[start].text: row.cells[start].text += ":"
                                            row.cells[start].text = target["label"] + " <b>["+str(self.predicateSeq)+":T]</b>"# + " of " + '<div class="w3-light-blue w3-border-indigo">' + source["label"] + "</div>"
                                            ''' CHANGED ABOVE
                                            if not row.cells[start].text.endswith(relLabel): row.cells[start].text += ":" + relLabel
                                            '''
                                            if not row.cells[start].css: row.cells[start].css = "w3-right-align w3-rightbar w3-round-large"
                                            # row.cells[start].css += " "+annLabel+"-"+target["label"].replace("/","-")+"-Part"
                                            row.cells[start].css += " Relation-"+str(self._relationIndex)
                                            if end-start>1: row.cells[start].colSpan = end-start
                                            for i in range(start+1,end):
                                                row.cells[i].hidden = True
                                                row.cells[i].text = row.cells[start].text
                                            markBorders(s,annLabel,start,end)
            self._relationIndex += 1
            if self._relationIndex > 9: self._relationIndex = 0
        return

    def addEvent(self, annLabel = '', eventCSS = '', eventLabel = '', startToken = 0, endToken = 0):
        # print(">>>>>>>", annLabel, eventType, startToken, endToken)
        for sidx in range(len(self._sentence)):
            s = self._sentence[sidx]
            # print(">>>>>>>", "sentence", sidx, "tokens", len(s["tokens"]))
            if annLabel in s["anns"]:
                sannlab = s["anns"][annLabel]
                # --
                start = startToken - s["start_token"]
                end = endToken - s["start_token"]
                # --
                if start >=0 and end >= 0 and start < len(s["tokens"]) and end <= len(s["tokens"]):
                    # print(">>>>>>>", "adding")
                    # print(s["tokens"])
                    row = sannlab["lastRow"]
                    if not row or row.lastTokenUsed > start:
                        row = TabularRow(len(s["tokens"]))
                        sannlab["rows"].append(row)
                        sannlab["rowSpan"] += 1
                        sannlab["lastRow"] = row
                    row.cells[start].text = eventLabel
                    row.cells[start].css = "w3-border w3-round-small "+eventCSS
                    row.lastTokenUsed = end
                    if end-start>1: row.cells[start].colSpan = end-start
                    for i in range(start+1,end):
                        row.cells[i].hidden = True
                        row.cells[i].text = row.cells[start].text
                    markBorders(s,annLabel,start,end)
                    # print(">>>>>>>", "rows", len(sannlab["rows"]))
                    # print(">>>>>>>", "row", "cells", len(row.cells))
        return

    def addEventArg(self, annLabel = '', eventCSS = '', eventLabel = '', startToken = 0, endToken = 0):
        # print(">>>>>>>", annLabel, eventType, startToken, endToken)
        for sidx in range(len(self._sentence)):
            s = self._sentence[sidx]
            # print(">>>>>>>", "sentence", sidx, "tokens", len(s["tokens"]))
            if annLabel in s["anns"]:
                sannlab = s["anns"][annLabel]
                # --
                start = startToken - s["start_token"]
                end = endToken - s["start_token"]
                # --
                if start >=0 and end >= 0 and start < len(s["tokens"]) and end <= len(s["tokens"]):
                    # print(">>>>>>>", "adding")
                    # print(s["tokens"])
                    row = sannlab["lastRow"]
                    if not row or row.lastTokenUsed > start:
                        row = TabularRow(len(s["tokens"]))
                        sannlab["rows"].append(row)
                        sannlab["rowSpan"] += 1
                        sannlab["lastRow"] = row
                    row.cells[start].text = eventLabel
                    row.cells[start].css = "w3-round-large opaque "+eventCSS # w3-border
                    row.lastTokenUsed = end
                    if end-start>1: row.cells[start].colSpan = end-start
                    for i in range(start+1,end):
                        row.cells[i].hidden = True
                        row.cells[i].text = row.cells[start].text
                    markBorders(s,annLabel,start,end)
                    # print(">>>>>>>", "rows", len(sannlab["rows"]))
                    # print(">>>>>>>", "row", "cells", len(row.cells))
        return

    def addTemporalRelation(self, annLabel = '', targetCSS = '', relationLabel = '', startToken = 0, endToken = 0):
        # print(">>>>>>>", annLabel, eventType, startToken, endToken)
        for sidx in range(len(self._sentence)):
            s = self._sentence[sidx]
            # print(">>>>>>>", "sentence", sidx, "tokens", len(s["tokens"]))
            if annLabel in s["anns"]:
                sannlab = s["anns"][annLabel]
                # --
                start = startToken - s["start_token"]
                end = endToken - s["start_token"]
                # --
                if start >=0 and end >= 0 and start < len(s["tokens"]) and end <= len(s["tokens"]):
                    # print(">>>>>>>", "adding")
                    # print(s["tokens"])
                    row = sannlab["lastRow"]
                    if not row or row.lastTokenUsed > start:
                        row = TabularRow(len(s["tokens"]))
                        sannlab["rows"].append(row)
                        sannlab["rowSpan"] += 1
                        sannlab["lastRow"] = row
                    row.cells[start].text = relationLabel
                    row.cells[start].css = "w3-round-large w3-leftbar w3-rightbar w3-border-left w3-border-right "+targetCSS # w3-border
                    row.lastTokenUsed = end
                    if end-start>1: row.cells[start].colSpan = end-start
                    for i in range(start+1,end):
                        row.cells[i].hidden = True
                        row.cells[i].text = row.cells[start].text
                    markBorders(s,annLabel,start,end)
                    # print(">>>>>>>", "rows", len(sannlab["rows"]))
                    # print(">>>>>>>", "row", "cells", len(row.cells))
        return

    def addCorefRelation(self, annLabel = '', targetCSS = '', relationLabel = '', startToken = 0, endToken = 0):
        # print(">>>>>>>", annLabel, eventType, startToken, endToken)
        for sidx in range(len(self._sentence)):
            s = self._sentence[sidx]
            # print(">>>>>>>", "sentence", sidx, "tokens", len(s["tokens"]))
            if annLabel in s["anns"]:
                sannlab = s["anns"][annLabel]
                # --
                start = startToken - s["start_token"]
                end = endToken - s["start_token"]
                # --
                if start >=0 and end >= 0 and start < len(s["tokens"]) and end <= len(s["tokens"]):
                    # print(">>>>>>>", "adding")
                    # print(s["tokens"])
                    row = sannlab["lastRow"]
                    if not row or row.lastTokenUsed > start:
                        row = TabularRow(len(s["tokens"]))
                        sannlab["rows"].append(row)
                        sannlab["rowSpan"] += 1
                        sannlab["lastRow"] = row
                    row.cells[start].text = relationLabel
                    row.cells[start].css = targetCSS # w3-border
                    row.lastTokenUsed = end
                    if end-start>1: row.cells[start].colSpan = end-start
                    for i in range(start+1,end):
                        row.cells[i].hidden = True
                        row.cells[i].text = row.cells[start].text
                    markBorders(s,annLabel,start,end)
                    # print(">>>>>>>", "rows", len(sannlab["rows"]))
                    # print(">>>>>>>", "row", "cells", len(row.cells))
        return


    def addEvents(self, annLabel = '', eventView = {}):
        # predicateSeq = 0
        self._eventIndex += 1
        self._sidx = -1
        self._startToken = -1
        self._endToken = 0
        for eventIndex in eventView:
            # self.predicateSeq += 1
            event = eventView[eventIndex]
            print("*** EVENT ***",event)
            startToken = event["start"]
            endToken = event["end"]
            print("*** TOKENS ***",startToken,endToken)
            event["css"] = 'Event-'+str(self._eventIndex)
            self.addEvent(annLabel = annLabel, eventCSS = event["css"], eventLabel = "<b>["+event["id"]+"]</b> " + event["label"], startToken = startToken, endToken = endToken)
            self._eventIndex += 1
            if self._eventIndex > 9: self._eventIndex = 0
            
            '''
            for sidx in range(len(self._sentence)):
                s = self._sentence[sidx]
                if annLabel in s["anns"]:
                    sannlab = s["anns"][annLabel]
                    # print(s["tokens"])
                    start = startToken - s["start_token"]
                    end = endToken - s["start_token"]
                    end_source = end
                    if start >=0 and end >= 0 and start < len(s["tokens"]) and end <= len(s["tokens"]):
                        # print("*** TOKENS (in) ***",start,end)
                        # always new row for predicates
                        sannlab["rowSpan"] += 1
                        print(startToken, endToken, self._startToken, self._endToken, sidx, self._sidx)
                        if startToken < self._endToken or self._sidx < sidx:
                            print("*** new row ***")
                            row = TabularRow(len(s["tokens"]))
                        self._startToken = startToken
                        self._endToken = endToken
                        self._sidx = sidx
                        sannlab["rows"].append(row)
                        sannlab["lastRow"] = row
                        #print("-----------------")
                        #print (predicate, start, end, len(row.cells))
                        #print("-----------------")
                        #print (source)
                        #print("-----------------")
                        row.cells[start].text = "<b>["+event["id"]+"]</b> " + event["label"] # + ': ' + predicate["relationName"]
                        # row.cells[start].css = "w3-leftbar w3-round-large "+annLabel+"-"+event["label"].replace("/","-") # w3-border-left
                        # row.cells[end-1].css = "w3-rightbar w3-border-indigo w3-round-large "+annLabel+"-"+event["label"] # w3-border-right
                        row.cells[start].css = "w3-left-align w3-leftbar w3-round-large Relation-"+str(self._eventIndex) # annLabel+"-"+event["label"].replace("/","-") # w3-border-left 
                        if end-start>1: row.cells[start].colSpan = end-start
                        for i in range(start+1,end):
                            row.cells[i].hidden = True
                            row.cells[i].text = row.cells[start].text
                        #    
                        markBorders(s,annLabel,start,end)
                        print("*** ADDED ***",event["id"])
                        # print("***", s["anns"]["NER-Onto"]["rows"][0].cells[2].border_left)
            '''
            
            '''
            sourceIdx = predicate["sourceConstituent"]
            if type(sourceIdx) is str:
                sourceIdx = int(sourceIdx)
            # source = annConstituents[sourceIdx]



                        # arguments now
                        if True:
                            for relLabel in predicate:
                                if relLabel != "sourceConstituent" and relLabel != "relationName" :
                                    targetIdx = predicate[relLabel]
                                    if type(targetIdx) is str:
                                        targetIdx = int(targetIdx)
                                    target = annConstituents[targetIdx]

                                    for sidx in range(len(self._sentence)):
                                        s2 = self._sentence[sidx]
    
                                        start = target["start"] - s2["start_token"]
                                        end = target["end"] - s2["start_token"]
                                        if start >=0 and end >= 0 and start < len(s2["tokens"]) and end <= len(s2["tokens"]):
                                            ''
                                            NEW ROW NEEDED ??? True = ALWAYS
                                            ''
                                            if True or not start >= end_source:
                                                sannlab2 = s2["anns"][annLabel]
                                                sannlab2["rowSpan"] += 1
                                                row = TabularRow(len(s2["tokens"]))
                                                sannlab2["rows"].append(row)
                                                sannlab2["lastRow"] = row
                                            ### if row.cells[start].text: row.cells[start].text += ":"
                                            row.cells[start].text = target["label"] + " <b>["+str(self.predicateSeq)+":T]</b>"# + " of " + '<div class="w3-light-blue w3-border-indigo">' + source["label"] + "</div>"
                                            '' CHANGED ABOVE
                                            if not row.cells[start].text.endswith(relLabel): row.cells[start].text += ":" + relLabel
                                            ''
                                            if not row.cells[start].css: row.cells[start].css = "w3-right-align w3-rightbar w3-round-large"
                                            # row.cells[start].css += " "+annLabel+"-"+target["label"].replace("/","-")+"-Part"
                                            row.cells[start].css += " Relation-"+str(self._eventIndex)
                                            if end-start>1: row.cells[start].colSpan = end-start
                                            for i in range(start+1,end):
                                                row.cells[i].hidden = True
                                                row.cells[i].text = row.cells[start].text
                                            markBorders(s,annLabel,start,end)
            '''
        return

    def addSpanLabelView(self, textAnnViews = {}, annViewName = '', annLabel = ''):
        if not self.addAnnLabel(annLabel): return
        annView = None
        annView = getAnnView(textAnnViews,annViewName)
        if annView:
            annConstituents = getAnnConstituents(annView)
            if annConstituents: 
                # print("--------------")
                # print(annConstituents)
                for c in annConstituents:
                    if "properties" in c and "type" in c["properties"] and "value" in c["properties"]:
                        self.addSpan(annLabel,c["properties"]["type"], c["properties"]["type"]+":"+c["properties"]["value"],c["start"],c["end"])
                    else:
                        self.addSpan(annLabel,c["label"],c["label"],c["start"],c["end"])
                # print(">>" , "addSpanLabelView" , annLabel)

    def addSpanList(self, textAnnViews = {}, annViewName = '', annLabel = ''):
        if not self.addAnnLabel(annLabel): return
        for c in textAnnViews:
            if "label" in c and "start" in c and "end" in c:
                spanLink = c["label"].split("|")[0]
                # self.addSpan(annLabel,spanType, c["label"],c["start"],c["end"])
                self.addLinkedSpan(annLabel, spanType = 'EDL', spanLabel = c["label"], startToken = c["start"], endToken = c["end"], annURL = "https://en.wikipedia.org/wiki/"+spanLink)
        # print(">>" , "addSpanLabelView" , annLabel)

    def addPredicateArgumentView(self, textAnnViews = {}, annViewName = '', annLabel = ''):
        if not self.addAnnLabel(annLabel): return
        annView = None
        annView = getAnnView(textAnnViews,annViewName)
        if annView:
            annConstituents = getAnnConstituents(annView)
            annRelations = getAnnRelations(annView)
            if annConstituents and annRelations:
                # print("--------------")
                # print(annConstituents)
                annPredicates = {}
                for r in annRelations:
                    rID = "r"+str(r["srcConstituent"])
                    if rID not in annPredicates: annPredicates[rID] = {"sourceConstituent":r["srcConstituent"]}
                    annPredicates[rID][r["relationName"]] = r["targetConstituent"]
                # print(annPredicates)
                self.addPredicates(annLabel,annPredicates,annConstituents)
                # print(">>" , "addSpanLabelView" , annLabel)

    def addRelationView(self, textAnnViews = {}, annViewName = '', annLabel = ''):
        if not self.addAnnLabel(annLabel): return
        annView = None
        annView = getAnnView(textAnnViews,annViewName)
        if annView:
            annConstituents = getAnnConstituents(annView)
            annRelations = getAnnRelations(annView)
            if annConstituents and annRelations:
                # print("--------------")
                # print(annConstituents)
                annPredicates = {}
                for r in annRelations:
                    rID = "r"+str(r["srcConstituent"])
                    if rID not in annPredicates: annPredicates[rID] = {"sourceConstituent":r["srcConstituent"], "relationName":r["relationName"]}
                    annPredicates[rID][r["relationName"]] = r["targetConstituent"]
                # print(annPredicates)
                self.addRelations(annLabel,annPredicates,annConstituents)
                # print(">>" , "addSpanLabelView" , annLabel)

    def addEventsView(self, eventView = {}, annLabel = ''):
        if not self.addAnnLabel(annLabel): return
        eventID = 0
        for eventLabel in eventView:
            event = eventView[eventLabel]
            eventID += 1
            event["id"] = "EV"+str(eventID)
            #rID = "r"+str(r["srcConstituent"])
            #if rID not in annPredicates: annPredicates[rID] = {"sourceConstituent":r["srcConstituent"], "relationName":r["relationName"]}
            #annPredicates[rID][r["relationName"]] = r["targetConstituent"]
        # print(annPredicates)
        self.addEvents(annLabel,eventView)
        # print(">>" , "addSpanLabelView" , annLabel)

    def addEventsArgsView(self, eventView = {}, argsList = [], annLabel = ''):
        if not self.addAnnLabel(annLabel): return
        eventID = None
        
        for argument in argsList:
            # argument = argsView[argLabel]
            # linkedLabel = 
            argConst = argument["constituent"]
            srcConst = eventView[ argument["source"] ]
            
            self.addEventArg(annLabel = "Arguments", eventCSS = "EVENT-ARG "+srcConst["css"], eventLabel = "["+srcConst["id"]+"] "+argConst["label"], startToken = argConst["start"], endToken = argConst["end"])

            # eventID += 1
            # event["id"] = "EV"+str(eventID)
            # rID = "r"+str(r["srcConstituent"])
            # if rID not in annPredicates: annPredicates[rID] = {"sourceConstituent":r["srcConstituent"], "relationName":r["relationName"]}
            # annPredicates[rID][r["relationName"]] = r["targetConstituent"]
        # print(annPredicates)
        # self.addEvents(annLabel,eventView)
        # print(">>" , "addSpanLabelView" , annLabel)

    def addTemporalView(self, eventView = {}, temporalList = [], annLabel = ''):
        if not self.addAnnLabel(annLabel): return
        for temporal in temporalList:
            relSourceConst = temporal["srcConstituent"]
            relTargetConst = temporal["targetConstituent"]
            if type(relSourceConst) is str:
                relSourceConst = int(relSourceConst)
            if type(relTargetConst) is str:
                relTargetConst = int(relTargetConst)
            
            srcConst = eventView[ relSourceConst ]
            tgtConst = eventView[ relTargetConst ]
            print("-- temporal constituents --")
            print(relSourceConst,relTargetConst,srcConst,tgtConst)
            
            # self.addEventArg(annLabel = "Arguments", eventCSS = "EVENT-ARG "+srcConst["css"], eventLabel = "["+srcConst["id"]+"] "+argConst["label"], startToken = argConst["start"], endToken = argConst["end"])
            icon = '<img src="./html/image/time.png" width="14px" height="12px">'
            if temporal["relationName"] == "before":
                # self.addTemporalRelation(annLabel = annLabel, targetCSS = "TEMP-REL-before "+tgtConst["css"], relationLabel = icon+" "+"["+srcConst["id"]+"] <b>"+temporal["relationName"]+"</b> ["+tgtConst["id"]+"]", startToken = srcConst["start"], endToken = srcConst["end"])
                self.addTemporalRelation(annLabel = annLabel, targetCSS = "TEMP-REL-before temporal-border "+tgtConst["css"], relationLabel = icon+" "+"<b>"+temporal["relationName"]+"</b> ["+tgtConst["id"]+"]", startToken = srcConst["start"], endToken = srcConst["end"])
            if temporal["relationName"] == "after":
                # self.addTemporalRelation(annLabel = annLabel, targetCSS = "TEMP-REL-after "+tgtConst["css"], relationLabel = "["+srcConst["id"]+"] <b>"+temporal["relationName"]+"</b> ["+tgtConst["id"]+"]"+" "+icon, startToken = srcConst["start"], endToken = srcConst["end"])
                self.addTemporalRelation(annLabel = annLabel, targetCSS = "TEMP-REL-after temporal-border "+tgtConst["css"], relationLabel = "["+tgtConst["id"]+"]"+" "+"<b>"+temporal["relationName"]+"</b>"+" "+icon, startToken = srcConst["start"], endToken = srcConst["end"])

    def addCorefView(self, eventView = {}, corefList = [], annLabel = ''):
        if not self.addAnnLabel(annLabel): return
        for coref in corefList:
            relSourceConst = coref["srcConstituent"]
            relTargetConst = coref["targetConstituent"]
            if type(relSourceConst) is str:
                relSourceConst = int(relSourceConst)
            if type(relTargetConst) is str:
                relTargetConst = int(relTargetConst)
            
            srcConst = eventView[ relSourceConst ]
            tgtConst = eventView[ relTargetConst ]
            print("-- coref constituents --")
            print(relSourceConst,relTargetConst,srcConst,tgtConst)
            
            # self.addEventArg(annLabel = "Arguments", eventCSS = "EVENT-ARG "+srcConst["css"], eventLabel = "["+srcConst["id"]+"] "+argConst["label"], startToken = argConst["start"], endToken = argConst["end"])
            icon = '<img src="./html/image/coref.png" width="14px" height="12px">'
            
            #if coref["relationName"] == "coref":
                
            # self.addTemporalRelation(annLabel = annLabel, targetCSS = "COREF "+tgtConst["css"], relationLabel = icon+" "+"["+srcConst["id"]+"] <b>"+coref["relationName"]+"</b> ["+tgtConst["id"]+"]", startToken = srcConst["start"], endToken = srcConst["end"])
            self.addCorefRelation(annLabel = annLabel, targetCSS = "w3-leftbar w3-rightbar COREF coref-border "+tgtConst["css"], relationLabel = icon+" "+"<b>["+tgtConst["id"]+"]</b>", startToken = srcConst["start"], endToken = srcConst["end"])


    def HTML(self):
        html = ""
        # html += str(self._sentenceEndPositions)
        for s in self._sentence:
            loTokens = s["tokens"]
            noTokens = len(loTokens)
            html += '<div class="w3-panel w3-border w3-border-amber" style="overflow-x: auto;white-space: nowrap;">\n'
            html += ' &nbsp; '
            html += ' <table class="w3-center w3-small">\n'
            # html += '  <tr><td>'+" ".join(loTokens)+'</td></tr>'
            html += '  <tr>\n'
            html += '   <td class="w3-border w3-right-align ANN-Label">Sentence&nbsp;&raquo;&nbsp;</td><td>&nbsp;</td>'
            for t in loTokens:
                html += '   <td><b>'+ t +'</b></td>'
            html += '  </tr>\n'
            for annLabel in s["anns"]:
                # print(annLabel)
                ann = s["anns"][annLabel]
                for rownum in range(len(ann["rows"])):
                    # print(rownum)
                    row = ann["rows"][rownum]
                    html += '  <tr>\n'
                    if False or rownum == 0:
                        html += '   <td class="w3-border w3-right-align ANN-Label"'
                        # if ann["rowSpan"] > 1: html += ' rowspan="'+str(ann["rowSpan"])+'"'
                        if ann["rowSpan"] > 1: html += ' rowspan="'+str(len(ann["rows"]))+'"'
                        html += '>'+annLabel+'&nbsp;&raquo;&nbsp;</td>\n'
                    # html += '   <td>'+str(rownum)+'</td>\n'
                    # html += '   <td>'+str(len(row.cells))+'</td>\n'
                    html += '<td>&nbsp;</td>'
                    for cell in row.cells:
                        if not cell.hidden:
                            html += '   <td'
                            if cell.colSpan > 1: html += ' colspan="'+str(cell.colSpan)+'"'
                            # if cell.css: 
                            html += ' class="'+str(cell.css)
                            if not cell.text and cell.border_left: html += " w3-border-left"
                            if not cell.text and cell.border_right: html += " w3-border-right"
                            html += '"' 
                            html += '>'+cell.text+'</td>\n'
                    #html += '   <td class="w3-border">'+str(rownum)+'</td>\n'
                    
                    html += '  </tr>\n'
            html += ' </table>'
            html += ' &nbsp; '
            html += '</div>'
        # print(html)
        return html

