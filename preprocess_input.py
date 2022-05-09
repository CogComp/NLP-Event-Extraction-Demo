import re
from time import time
import regex

from nltk import sent_tokenize, word_tokenize

special_char_list = ["'", ",", ";", ":", "-", "?", "!", "$", "%", "#", "_", "&", "~", "|", "^", "+", "*", "/", "<", "=", ">", "(", ")", "{", "}", "[", "]"]

def replacer(match):
    if match.group(1) is not None:
        return '{} '.format(match.group(1))
    else:
        return ' {}'.format(match.group(2))

def preprocess_text(text):
    rx = re.compile(r'^(\W+)|(\W+)$')
    text = " ".join([rx.sub(replacer, word) for word in raw_text.split()])
    text = re.sub("'", " ' ", text)
    text = re.sub("\t+", " ", text)
    text = re.sub("\s+", " ", text)
    text = re.sub("\n+", " ", text)
    
    return text
    
def preprocess_input_text(input_text="", multi=False, special_char="remove", text_mod=True, char_list=[]):
    # start_time = time()
    input_text = input_text.encode('utf-8').decode("utf-8")
    if not char_list:
        special_char_list = ["!", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "]", "^", "_", "`", "{", "|", "}", "~"]
    else:
        special_char_list = char_list
    if multi:
        if "\n" in input_text:
            input_text = re.sub("\n+", " ", input_text)
        if "\t" in input_text:
            input_text = re.sub("\t+", " ", input_text)

    if special_char=="remove":
        input_text = regex.sub(r'[^\p{Latin}]', u' ', input_text)

    elif special_char=="convert" :
        if "’" in input_text:
            input_text = re.sub("\’", " ' ", input_text)
            # input_text = re.sub("\’", " ", input_text)
        if "‘" in input_text:
            input_text = re.sub("\‘", " ' ", input_text)
            #  input_text = re.sub("\‘", " ", input_text)
        if "“" in input_text:
            input_text = re.sub("“", " \" ", input_text)
            # input_text = re.sub("“", " ", input_text)   
        if "”" in input_text:
            input_text = re.sub("”", " \" ", input_text)
            # input_text = re.sub("”", " ", input_text)
        if "—" in input_text:
            input_text = re.sub("—", " - ", input_text)
        if "–" in input_text:
            input_text = re.sub("–", " - ", input_text)
        if "…" in input_text:
            input_text = re.sub("…", " . ", input_text)
        # if "." in input_text:
        #     input_text = re.sub(".", " . ", input_text)
    
    if special_char_list:
        if "'" in input_text and "'" in special_char_list:
            input_text = re.sub("'", " ' ", input_text)
            # input_text = re.sub("'", " ", input_text)
        if "," in input_text and "," in special_char_list:
            input_text = re.sub(",", " , ", input_text)
            # input_text = re.sub(",", " ", input_text)
        if ";" in input_text and ";" in special_char_list:
            input_text = re.sub(";", " ; ", input_text)
            # input_text = re.sub(";", " ", input_text)
        if ":" in input_text and ":" in special_char_list:
            input_text = re.sub(":", " : ", input_text)
            # input_text = re.sub(":", " ", input_text)
        if "-" in input_text and "-" in special_char_list:
            input_text = re.sub("-+", " - ", input_text)
        if "?" in input_text and "?" in special_char_list:
            input_text = re.sub("\?+", " ? ", input_text)
        if "!" in input_text and "!" in special_char_list:
            input_text = re.sub("!+", " ! ", input_text)

        if "$" in input_text and "$" in special_char_list:
            input_text = re.sub("\$", " $ ", input_text)
        if "%" in input_text and "%" in special_char_list:
            input_text = re.sub("%", " % ", input_text)
        if "#" in input_text and "#" in special_char_list:
            input_text = re.sub("#", " # ", input_text)

        if "_" in input_text and "_" in special_char_list:
            input_text = re.sub("_", " _ ", input_text)
        if "&" in input_text and "&" in special_char_list:
            input_text = re.sub("&", " & ", input_text)
        if "~" in input_text and "~"  in special_char_list:
            input_text = re.sub("~", " ~ ", input_text)
        if "|" in input_text and "|" in special_char_list:
            input_text = re.sub("|", " | ", input_text)
        if "^" in input_text and "^" in special_char_list:
            input_text = re.sub("\^", " ^ ", input_text)

        if "+" in input_text and "+" in special_char_list:
            input_text = re.sub("\+", " + ", input_text)
        if "*" in input_text and "*" in special_char_list:
            input_text = re.sub("\*", " * ", input_text)
        if "/" in input_text and "/" in special_char_list:
            input_text = re.sub("/", " / ", input_text)
        if "<" in input_text and "<" in special_char_list:
            input_text = re.sub("<", " < ", input_text)
        if "=" in input_text and "=" in special_char_list:
            input_text = re.sub("=", " = ", input_text)
        if ">" in input_text and ">" in special_char_list:
            input_text = re.sub(">", " > ", input_text)

        if "(" in input_text and "(" in special_char_list:
            input_text = re.sub("\(", " ( ", input_text)
        if ")" in input_text and ")" in special_char_list:
            input_text = re.sub("\)", " ) ", input_text)
        if "{" in input_text and "{" in special_char_list:
            input_text = re.sub("{", " { ", input_text)
        if "}" in input_text and "}" in special_char_list:
            input_text = re.sub("}", " } ", input_text)
        if "[" in input_text and "[" in special_char_list:
            input_text = re.sub("\[", " [ ", input_text)
        if "]" in input_text and "]" in special_char_list:
            input_text = re.sub("\]", " ] ", input_text)
    
    if text_mod:
        if "p.m" in input_text:
            input_text = re.sub("p.m", "pm", input_text)
        if "p.m." in input_text:
            input_text = re.sub("p.m.", "pm", input_text)
        if "P.M" in input_text:
            input_text = re.sub("P.M", "PM", input_text)
        if "P.M." in input_text:
            input_text = re.sub("P.M.", "PM", input_text)
            
        if "a.m" in input_text:
            input_text = re.sub("a.m", "am", input_text)
        if "a.m." in input_text:
            input_text = re.sub("a.m.", "am", input_text)
        if "A.M" in input_text:
            input_text = re.sub("A.M", "AM", input_text)
        if "A.M." in input_text:
            input_text = re.sub("A.M.", "AM", input_text)
    
    # input_text = regex.sub(r'[^\p{Latin}]', u' ', input_text)
    input_text = re.sub("\s+", " ", input_text).strip()

    # print("input_text[-1] : ", input_text[-1])
    # if not input_text[-1] == '.':
    #     input_text = input_text + "."

    end_time = time()
    # print("***Processing Time (preprocessing): ", time() - start_time)
    # print("**", input_text)
    return input_text
