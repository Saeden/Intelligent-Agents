import requests
import os
from owlready2 import *




owlready2.JAVA_EXE = "C:\\Program Files (x86)\\Java\\jre1.8.0_351\\bin\\java.exe"
owlready2.reasoning.JAVA_MEMORY = 1000

#onto_path.append("Ontology_Intelligent_Agents_Group8.owl")

onto = get_ontology("file://Ontology_Intelligent_Agents_T-1.owl").load()

with onto:
    sync_reasoner()

def main():
    print("---Welcome to the IA Ontological Reasoner---\n")
    #print("Select a query: ")
    agent()

def agent(query=""):
    return

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