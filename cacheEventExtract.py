import json 
import hashlib
from datetime import datetime

class CacheEventExtraction:

    def __init__(self):
        self.lang = ["eng"]

    def load(self, name):
        '''
        name: "EE"
        '''
        try:
            with open('cache/cache_' + name + '.json') as file_obj:
                cache = json.load(file_obj)
            print("Successfully load cache from cache_" + name + ".json.")
        except:
            cache = {}
            for lang in self.lang: 
                cache[lang] = {}
            print("Cannot find cache_" + name + ".json and an empty new nested dictionary for cache is created.")
        
        return cache 

    
    def read(self, types, cache_dic, lang, hash_value):
        
        if types == 'Event':
            tokens = cache_dic[lang][hash_value]['token']
            endPositions = cache_dic[lang][hash_value]['end_pos']
            res_json = cache_dic[lang][hash_value]['res_json']

            if 'count' not in cache_dic[lang][hash_value].keys():
                cache_dic[lang][hash_value]['count'] = 1
            else:
                cache_dic[lang][hash_value]['count'] += 1

            print("--------------The " + types + " annotations is loaded from cache_EE --------------")

            
            return tokens, endPositions, res_json, cache_dic

        elif types == "Temporal":
            res_json = cache_dic[lang][hash_value]['temporal']
            print("--------------The " + types + " annotations is loaded from cache_EE --------------")

            return res_json, cache_dic

        else:
            res_json = cache_dic[lang][hash_value]['coref']
            print("--------------The " + types + " annotations is loaded from cache_EE --------------")

            return res_json, cache_dic


    def add(self, types, cache_dic, lang, text, hash_value, res_json, tokens=None, end_pos=None):
        
        if types == "Event":
            cache_dic[lang][hash_value] = {}
            cache_dic[lang][hash_value]['text'] = text
            cache_dic[lang][hash_value]['res_json'] = res_json
            cache_dic[lang][hash_value]['token'] = tokens
            cache_dic[lang][hash_value]['end_pos'] = end_pos
            cache_dic[lang][hash_value]['count'] = 1
            print("--------------The " + types + " annotations is not included from cache_EE --------------")

            return cache_dic

        elif types == "Temporal":
            cache_dic[lang][hash_value]['temporal'] = res_json           
            print("--------------The " + types + " annotations is not included from cache_EE --------------")
            return cache_dic

        else:
            cache_dic[lang][hash_value]['coref'] = res_json           
            print("--------------The " + types + " annotations is not included from cache_EE --------------")
            return cache_dic


    def count(self, cache_dic):
        '''
        This function is used to count the number of sentence in a cache
        '''  
        num = sum([len(cache_dic[key]) for key in cache_dic.keys()])

        return num


    def write(self, name, cache_dic):

        json_dic = json.dumps(cache_dic, indent=4)
        with open('cache/cache_' + name + '_'+ datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.json', 'w') as json_file:
            json_file.write(json_dic) 