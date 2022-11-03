from audioop import reverse
import requests
import os
from owlready2 import *
import json


#owlready2.JAVA_EXE = "C:\\Program Files (x86)\\Java\\jre1.8.0_351\\bin\\java.exe"
owlready2.reasoning.JAVA_MEMORY = 1000



onto_path.append("Ontology_IA_Group8Final.owl")
print(f"Loading ontology from: {onto_path}")
onto = get_ontology("file://Ontology_IA_Group8Final.owl").load()

print("Syncing reasoner and closing world...")
with onto:
    sync_reasoner(infer_property_values=True)
    close_world(onto)
    
with open('BEARER_TOKEN.txt') as f:    
    bearer_token = f.readline()


def main():
    print("\n\n---Welcome to the IA Ontological Reasoner---\n")
    print("What question would you like to ask?")
    #print("1. Are soccer and kickboxing unsafe sports?")
    #print("2. Is there a sport that is a riskfactor for a health condition?")

    selected = False
    keywords = [["unsafe"], ["risk", "riskfactor"], ["patents", "monopoly", "monopolized"]]
    #query_options = ["1", "2", "3"]
    finished = False
    done_query = False
    query_type = ''
    while (finished == False):
        while (selected == False):
            query = input("Question: ")
            for word in query.split(" "):
                for query_options in range(0, len(keywords)):
                    if word in keywords[query_options]:
                        query_type = str(query_options+1)
                        selected = True
            if query_type == '':
                print("Sorry but I don't recognise that question, please try again.")
        
        if not done_query:
            agent(query_type)
            done_query = True

        yes_no = input("\n\nDo you want to ask another question? (y/n):")

        if yes_no == 'n':
            finished = True
        elif yes_no == 'y':
            selected = False
            done_query = False
        else:
            print("That is not one of the options, please try again.")

    print(twitter_query())
    #print("\n\n")
    #query2()

def agent(query):
    if (query == "1"):
        check = query1()
        if not check:
            #print("No result from onto")
            twitter_query()

    elif (query == "2"):
        check = query2()
        if not check:
            print("No result from onto")
            #twitter()

    elif (query == "3"):
        check = query3()
        if not check:
            twitter_query()


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

def query3():
    print("Not implemented yet...")



#Parts of the code after this point were inspired by or copied from:
#https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Full-Archive-Search/full-archive-search.py
#https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Recent-Search/recent_search.py

def twitter_query(query: str = ""):
    print("The ontology could not provide an answer, querying Twitter for more up to date info...")

    search_url = "https://api.twitter.com/2/tweets/search/recent"
    #search_url = "https://api.twitter.com/2/tweets/search/all"

    # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
    # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
    query_params = {'query': '#sport OR #competition OR #eating','tweet.fields': 'author_id', 'max_results': 10, 'expansions': 'author_id', 'user.fields': 'public_metrics'}


    
    json_response = connect_to_endpoint(search_url, query_params)
    #print(json.dumps(json_response, indent=4, sort_keys=True))

    #start collecting 10 tweets from the people with the most followers
    most_followers = []
    for user in json_response["includes"]["users"]:
        most_followers.append((user["id"], user["name"], user["username"], user["public_metrics"]["followers_count"]))
    
    most_followers_sorted = sorted(most_followers, key=lambda tup: tup[1], reverse=True)
    #print(most_followers_sorted)

    result = []
    for user in most_followers_sorted[:10]:
        for tweet in json_response["data"]:
            if tweet["author_id"] == user[0]: result.append((user[1:], tweet))

    return result
        

#os.environ.get("BEARER_TOKEN")



def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "IA_Ontology_Reasoner"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

if __name__ == '__main__':
    main()