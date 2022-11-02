import requests
import os
from owlready2 import *


owlready2.JAVA_EXE = "C:\\Program Files (x86)\\Java\\jre1.8.0_351\\bin\\java.exe"
owlready2.reasoning.JAVA_MEMORY = 1000



onto_path.append("Ontology_IA_Group8Final_TEST.owl")
print(f"Loading ontology from: {onto_path}")
onto = get_ontology("file://Ontology_IA_Group8Final.owl").load()

print("Syncing reasoner and closing world...")
with onto:
    sync_reasoner(infer_property_values=True)
    close_world(onto)
    

def main():
    print("\n\n---Welcome to the IA Ontological Reasoner---\n")
    print("What question would you like to ask?")
    print("1. Are soccer and kickboxing unsafe sports?")
    print("2. Is there a sport that is a riskfactor for a health condition?")

    selected = False
    query_options = ["1", "2", "3"]
    finished = False
    done_query = False
    while (finished == False):
        while (selected == False):
            query = input("Select a query: ")
            if (query in query_options): selected = True
            else: 
                print("That is not one of the options, please try again")
        
        if not done_query:
            agent(query)
            done_query = True

        yes_no = input("\n\nDo you want to ask another question? (y/n):")

        if yes_no == 'n':
            finished = True
        elif yes_no == 'y':
            selected = False
            done_query = False
        else:
            print("That is not one of the options, please try again")



    #print("\n\n")
    #query2()

def agent(query):
    if (query == "1"):
        check = query1()
        if not check:
            print("No result from onto")
            #twitter()

    elif (query == "2"):
        check = query2()
        if not check:
            print("No result from onto")
            #twitter()

    elif (query == "3"):
        check = query3()
        if not check:
            print("No result from onto")
            #twitter()

def search(search_iri, search_term):
    print(f"\nQuerying if {search_term} is in the ontology:")

    search_result = onto.search(iri = search_iri)
    if search_result != [] and len(search_result) == 1: 
        print(f"{search_term} in in the ontology as: {search_result}")
        return search_result
    elif search_result != [] and len(search_result) > 1: 
        print(f"There seems to be more than one class related to {search_term}:\n{search_result}")
        print("\nFinding concept that most closely matches our query...")
        for concept in search_result:
            if concept.name == search_term: search_result = concept
        print(f"The best matching concept is: {search_result}")
        return [search_result]
    else:
        print(f"{search_term} is not in the ontology...\nQuerying Twitter for answers...")
        return search_result
        #query_twitter(["Soccer", "Kickboxing", "Unsafe", "Sport"])

def memberOf(instance, ont_class):
    print(f"\nChecking if {instance[0].name} is a member of {ont_class[0].name}:")

    search = onto.search(type = ont_class)
    print(f"Individual: {instance[0]}")
    print(f"Individuals in the class: {search}")
    if (instance[0] in search):
        return True
    else:
        return False

def allMembers(ont_class):
    print(f"\nFinding all individuals of {ont_class[0].name}...")
    search = onto.search(type = ont_class)
    if search != []:
        print(f"Individuals of {ont_class[0].name}:\n{search}")
        return search
    else:
        print("There are no individuals in this class! Searching twitter instead...")
        return search



    


def query1():
    #"1. Are soccer and kickboxing unsafe sports?"
    unsafe_InO = search("*UnsafeSport", "UnsafeSport")
    if unsafe_InO == []: return False
    
    soccer_InO = search("*soccer", "Soccer")
    if soccer_InO == []: return False

    kickbox_InO = search("*kickboxing", "Kickboxing")
    if kickbox_InO == []: return False

    soc_is_in = memberOf(soccer_InO, unsafe_InO)
    print(f"Individual is in class: {soc_is_in}")

    kic_is_in = memberOf(kickbox_InO, unsafe_InO)
    print(f"Individual is in class: {kic_is_in}")

    print(f"\nFinal answer: \nSoccer is unsafe is {soc_is_in} and kickboxing is unsafe is {kic_is_in}")

    return True




def query2():
    #"2. Is there a sport that is a riskfactor for some health condition?"
    sport_InO = search("*Sport", "Sport")
    if sport_InO == []: return False


    healthCon_InO = search("*HealthCondition", "HealthCondition")
    if healthCon_InO == []: return False

    riskFactor_InO = search("*isRiskfactorFor", "isRiskfactorFor")
    if riskFactor_InO == []: return False

    allSports = allMembers(sport_InO)
    if allSports == []: return False

    allHealthCon = allMembers(healthCon_InO)
    if allHealthCon == []: return False


    found = False
    #for each sport check if they are transitively connected to riskFactor
    print("Check for each sport if there is a risk for a health condition...")
    for sport in allSports:
        relations = getattr(sport, riskFactor_InO[0].name)

        for condition in allHealthCon:
            if condition in relations:
                result_sport = sport
                result_cond = condition
                found = True
                break

        if found: break

    if found:
        print(f"There is a sport ({result_sport.name}) which is a risk factor for {result_cond.name}")
    else:
        print("There is no sport that has a health condition as a risk")

    return True

    
        



    #print(onto.search(isRiskfactorFor = "*"))

def query3():
    print("Not implemented yet...")

def twitter(query=""):
    # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
    # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
    query_params = {'query': '(from:twitterdev -is:retweet) OR #twitterdev','tweet.fields': 'author_id'}
    search_url = "https://api.twitter.com/2/tweets/search/recent"    
    requests.get()

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    bearer_token = os.environ.get("BEARER_TOKEN")
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

if __name__ == '__main__':
    main()