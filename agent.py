import requests
import os
from owlready2 import *




owlready2.JAVA_EXE = "C:\\Program Files (x86)\\Java\\jre1.8.0_351\\bin\\java.exe"
owlready2.reasoning.JAVA_MEMORY = 1000

#onto_path.append("Ontology_IA_Group8Final_TEST.owl")

"""onto_before = get_ontology("file://Ontology_IA_Group8Final_TEST.owl").load()

with onto_before:
    #close_world(onto)
    sync_reasoner()
    
onto_before.save(file = "Ontology_IA_Group8Final_TEST.owl", format = "rdfxml")"""




onto = get_ontology("file://Ontology_IA_Group8Final.owl").load()

with onto:
    sync_reasoner(infer_property_values=True)
    close_world(onto)
    

def main():
    """print("\n\n---Welcome to the IA Ontological Reasoner---\n")
    print("What question would you like to ask?")
    print("1. Are soccer and kickboxing unsafe sports?")

    selected = False
    query_options = ["1", "2", "3"]
    while (selected == False):
        query = input("Select a query: ")
        if (query in query_options): selected = True
        else: 
            print("That is not one of the options, please try again")
    agent(query)"""
    print("\n\n")
    query1()

def agent(query):
    if (query == "1"):
        query1()

    elif (query == "2"):
        query2()

    elif (query == "3"):
        query3()

def searchFound(search_result, search_term):
    if search_result is not []: 
        print(f"{search_term} in in the ontology as: {search_result}")
    else:
        print(f"{search_term} is not in the ontology...\nQuerying Twitter for answers...")
        #query_twitter(["Soccer", "Kickboxing", "Unsafe", "Sport"])

def memberOf(instance, ont_class):
    search = onto.search(is_a = ont_class)
    print(f"Individual: {instance}")
    print(f"Class and its individuals: {search}")
    if (instance[0] in search):
        return True
    else:
        return False


def query1():
    print("\nQuerying if UnsafeSport is in the ontology:")
    unsafe_InO = onto.search(iri = "*UnsafeSport")
    searchFound(unsafe_InO, "UnsafeSport")
    

    print("\nQuerying if soccer is in the ontology:")
    soccer_InO = onto.search(iri = "*soccer")
    searchFound(soccer_InO, "Soccer")

    print("\nQuerying if kickboxing is in the ontology:")
    kickbox_InO = onto.search(iri = "*kickboxing")
    searchFound(kickbox_InO, "Kickboxing")

    print("\nChecking if soccer is a member of UnsafeSport:")
    is_in_soc = memberOf(soccer_InO, unsafe_InO)
    print(f"Indivual is in class: {is_in_soc}")

    print("\nChecking if kickboxing is a member of UnsafeSport:")
    is_in_kic = memberOf(kickbox_InO, unsafe_InO)
    print(f"Indivual is in class: {is_in_kic}")

    print(f"\nFinal answer: \nSoccer is unsafe is {is_in_soc} and kickboxing is unsafe is {is_in_kic}")




def query2():
    print("Not implemented yet...")

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