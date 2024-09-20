import spacy

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

#function processes each entity within the document tied to the content, then
# prints the entity and the label associated with it, then adds it to a list
#returns list of all normal pretrained labels
# takes a string (content) as a parameter
def precheck_process_content(content):
     allLabels = []
     doc = nlp(content)
     for ent in doc.ents:
          print(ent.text, ent.label_)
          allLabels.append(ent.label_)
     
     print("All labels of ents in doc...")
     return allLabels



# checking function to see if the entity is a single word, if not, need to use matcher
def singleWordCheck(wordInList):
     word = wordInList.split()
     return (len(word) == 1)



#function to process custom rule entities
#userRules variable represents a List of custom rules from user input through add-on
#takes content and userRules as parameters

#TO DO:
# 1. split rule into matcher pattern for checking
# 2. implement matcher for checking
def precheck_process_rule_entities(content, userRules):
     allCustomLabels = []
     doc = nlp(content)
     for rule in userRules:
          for ent in doc.ents:
               if singleWordCheck(ent.text):
                    if ent.text == rule:
                         print(f"Custom rule entity found: {ent.text}")
                         allCustomLabels.append(ent.text)
               else:
                    # implement matching function here
     
     # need to implement matchers for >1 word entity searching
     print("All custom rule entities found...")
     return allCustomLabels

# IMPLEMENT A FUNCTION TO LABEL BASED ON CUSTOM ENTITY AND EXECUTE DESIRED ACTIONS
# action functions will be separate (label, star, archive, delete)
# ex) Entity: "Internship"-->Action: "Star Mail" - - - - - Entity: "Food Subscription Email"-->Action: "Archive Mail"


