import requests
import json

def ambariREST( restAPI ) :
    url = "http://"+AMBARI_DOMAIN+":"+AMBARI_PORT+restAPI
    r= requests.get(url, auth=(AMBARI_USER_ID, AMBARI_USER_PW))
    return(json.loads(r.text));

def getServices( SERVICE) :
    restAPI = "/api/v1/clusters/"+CLUSTER_NAME+"/services/"+SERVICE
    json_data =  ambariREST(restAPI)
    return(json_data);

AMBARI_DOMAIN='localhost'
AMBARI_PORT='8080'
AMBARI_USER_ID='raj_ops'
AMBARI_USER_PW='raj_ops'

restAPI='/api/v1/clusters'
url="http://"+AMBARI_DOMAIN+":"+AMBARI_PORT+restAPI
r=requests.get(url, auth=(AMBARI_USER_ID, AMBARI_USER_PW))
json_data=json.loads(r.text)
CLUSTER_NAME=json_data["items"][0]["Clusters"]["cluster_name"]
print(CLUSTER_NAME)
data = getServices('SPARK2')
Services = ['ZOOKEEPER','HDFS','SPARK2','KAFKA','HIVE']
for Service in Services:
    data = getServices(Service)
    #print(data)
    print(data["ServiceInfo"]["service_name"]+' '+data["ServiceInfo"]["state"])
    #print(data["ServiceInfo"]["state"])
