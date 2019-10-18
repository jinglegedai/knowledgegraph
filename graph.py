import pandas as pd
import spacy
from tqdm import tqdm


nlp = spacy.load('en_core_web_sm')

sent = "later, a woman’s scream is heard in the distance."

for tok in nlp(sent):
    print(tok.text, '----', tok.dep_)

#  It extracts subject and object from the given sentence. As of now it works only for the sentences with single subject and object. 
#  It extracts all the subject and objects based on dependency parse tree along with it's modifiers. It also considers compound nouns. 
def extract_entities(sent):
    subj = ''
    obj = ''
    prv_tok_txt = ''
    prv_tok_dep = ''
    pfx = ''
    mod = ''

    for tok in nlp(sent):
        
        if tok.dep_.endswith('mod'):
            mod = tok.text
        
        if tok.dep_ == 'punct' and prv_tok_dep.endswith('mod'):
            mod = mod + tok.text
        
        if tok.dep_ == 'compound':
            pfx = tok.text + ' '
            if prv_tok_dep == 'compound':
                pfx = prv_tok_txt + ' ' + pfx

        if tok.dep_.find("subj") == True:
            
            if prv_tok_dep != 'compound':
                pfx = ''
            
            if prv_tok_dep != 'punct' and prv_tok_dep.endswith('mod') == False:
                mod = ''
            
            if prv_tok_dep == 'punct':
                subj = mod + pfx + tok.text
            else:
                subj = mod + ' ' + pfx + tok.text
            pfx = ''
            mod = ''

        if tok.dep_.find("obj") == True:
            
            if prv_tok_dep != 'compound':
               pfx = ''
            
            if prv_tok_dep != 'punct' and prv_tok_dep.endswith('mod') == False:
                mod = ''
            
            if prv_tok_dep == 'punct':
                obj = mod + pfx + tok.text
            else:
                obj = mod + ' ' + pfx + tok.text
            pfx = ''
            mod = ''

        prv_tok_dep = tok.dep_
        prv_tok_txt = tok.text

    return [subj.strip(), obj.strip()]

def get_entities(sent):
  ## chunk 1
  ent1 = ""
  ent2 = ""

  prv_tok_dep = ""    # dependency tag of previous token in the sentence
  prv_tok_text = ""   # previous token in the sentence

  prefix = ""
  modifier = ""

  #############################################################
  
  for tok in nlp(sent):
    ## chunk 2
    # if token is a punctuation mark then move on to the next token
    if tok.dep_ != "punct":
      # check: token is a compound word or not
      if tok.dep_ == "compound":
        prefix = tok.text
        # if the previous word was also a 'compound' then add the current word to it
        if prv_tok_dep == "compound":
          prefix = prv_tok_text + " "+ tok.text
      
      # check: token is a modifier or not
      if tok.dep_.endswith("mod") == True:
        modifier = tok.text
        # if the previous word was also a 'compound' then add the current word to it
        if prv_tok_dep == "compound":
          modifier = prv_tok_text + " "+ tok.text
      
      ## chunk 3
      if tok.dep_.find("subj") == True:
        ent1 = modifier +" "+ prefix + " "+ tok.text
        prefix = ""
        modifier = ""
        prv_tok_dep = ""
        prv_tok_text = ""      

      ## chunk 4
      if tok.dep_.find("obj") == True:
        ent2 = modifier +" "+ prefix +" "+ tok.text
        
      ## chunk 5  
      # update variables
      prv_tok_dep = tok.dep_
      prv_tok_text = tok.text
  #############################################################

  return [ent1.strip(), ent2.strip()]

# Load sentences from the CSV file
sentences = pd.read_csv('wiki_sentences_v2.csv')

entities = []
# Extract subject and object for each sentence and append it to entites list.
for s in tqdm(sentences['sentence']):
    entities.append(extract_entities(s))

print(entities[0:20])