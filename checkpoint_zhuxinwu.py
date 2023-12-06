import json
import requests
import os


def get_location():

    '''
    example: https://maps.googleapis.com/maps/api/place/textsearch/json
    ?location=42.3675294%2C-71.186966
    &query=123%20main%20street
    &radius=10000
    &key=YOUR_API_KEY
    '''

    url="https://maps.googleapis.com/maps/api/place/textsearch/json?query="
    my_key='AIzaSyA_NPvNiC3cLQX9IsKIOzHG63JGDTecGDw'

    search_kind=input("what kind of place you want to search? ")
    search_location=input("and based on which place? (can be specific to a city/road/address)")
    search_radius=input("do you have any radius restrict? if have, enter the number, if no, enter any: ")
    if search_radius.isdigit():
        radius=search_radius
        url_place=url+search_kind+search_location+"&radius="+radius+"&key="+my_key
    else:
        url_place=url+search_kind+search_location+"&key="+my_key

    place_req=requests.get(url_place)
    if place_req.status_code==200:
        place_json_initial=place_req.json()
        place_json=place_json_initial['results']
        print(place_json)
        #place_json.append([search_kind,search_location,search_radius])
    #return json list

    return place_json

def save_cache(place_json):
    #save original json list into cache
    current_directory = os.path.dirname(os.path.abspath(__file__))
    CACHE_FILENAME = os.path.join(current_directory, 'cache.json')
    dumped_json_cache = json.dumps(place_json)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()

def read_cache():
    #read the json list
    current_directory = os.path.dirname(os.path.abspath(__file__))
    CACHE_FILENAME = os.path.join(current_directory, 'cache.json')
    
    #CACHE_FILENAME = "/cache.json"
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict




class ResNode:
    def __init__(self,json):
        self.address=json['formatted_address']
        self.location=json['geometry']["location"]
        self.name=json['name']
        self.id=json["plus_code"]["global_code"]
        if 'rating' in json:
            self.rating=json["rating"]
        else:
            self.rating=0
        self.left=None
        self.right=None

    def print_node(self):
        print(f"address={self.address}, name={self.name}, rating={self.rating}")

def json_to_nodelist(place_json):
    NodeList=[]
    for i in range(len(place_json)):
        curNode=ResNode(place_json[i])
        NodeList.append(curNode)
    
    return NodeList
    
def sort_by_rating_bubble(NodeList):
    for i in range(len(NodeList)):
        for j in range(0, len(NodeList)-1):
            try:
                current_value = NodeList[j].rating
                next_value = NodeList[j+1].rating
                if current_value <= next_value:
                    NodeList[j], NodeList[j+1] = NodeList[j+1], NodeList[j]
            except TypeError:
                pass
    return NodeList

def place_node_toTree(NodeList):
    treefile=()
    rootnode=(None,None,None)




    
    
    

def main():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path_cache = os.path.join(current_directory, "cache.json")

    cache_ans="no"

    if os.path.exists(file_path_cache) is True:
        #cache_ans='no'
        cache_ans=input("You have a cache file. Do you want to read the cache? yes/no ")
    
    if cache_ans=="yes":
        place_json=read_cache()
        NodeList=json_to_nodelist(place_json)
    else:
        print(f"Please start a new search: ")
        place_json=get_location()
        save_cache(place_json)
        NodeList=json_to_nodelist(place_json)


    NodeList_bubble=sort_by_rating_bubble(NodeList)
    print("after sorting:")
    for item in NodeList_bubble:
        item.print_node()







if __name__ == '__main__':
      
    main()