#################################################################################################
#################################################################################################

# ALL FUNCTIONS STARTING WITH PRECHECK ARE FOR DEBUGGING AND TESTING PURPOSES
# DO NOT USE FOR FINAL IMPLEMENTATION

# NOTES #
# more than likely, if we are to use one entire list for all entities, better to use a set for lack of duplicates and efficiency
# for more advanced usage, can train a custom pipeline to check for our custom entities
# for now, using the pretrained model for ease of use
# also need to check how connectivity works for account linking and inbox access

# IMPLEMENTATION #
# will write debugging functions first for checking access to inbox and message retrieval
# bc dont want to use api calls if not needed
# using matchers for custom entities for std nlp pipeline
# will train custom pipeline later

#################################################################################################
#################################################################################################

import inboxAccess.py
import processContent.py

# IMPLEMENT A FUNCTION HERE FOR CHECKING ENTITIES AND CUSTOM ENTITIES AGAINST DATABASE OF REQUESTED ENTITIES AND DESIRED ACTIONS
# ex) Entity: "Internship"-->Action: "Star Mail" - - - - - Entity: "Food Subscription Email"-->Action: "Archive Mail"



#################################################################################################
# Main function to run the script #
#################################################################################################
if __name__ == '__main__':
     # one long string to check for entities
     stringToProcess = fetch_mail()
     # went with two separate functions for ease of debugging and testing, can combine later if needed
     allNormalLabels = process_content(stringToProcess)
     allCustomLabels = process_rule_entities(stringToProcess, userRulesInput) # where userRulesInput is a list of inputted custom rules 


