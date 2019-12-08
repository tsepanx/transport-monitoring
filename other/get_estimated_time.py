import json
import time

f = open("data5.json", "r")

s = f.read()
data = json.loads(s)
for i in range(len(data["data"]["properties"]["StopMetaData"]["Transport"])):
    for j in range(len(data["data"]["properties"]["StopMetaData"]["Transport"][i]["threads"])):
        for g in range(len(data["data"]["properties"]["StopMetaData"]["Transport"][i]["threads"][j]["BriefSchedule"]["Events"])):
            cur = list(data["data"]["properties"]["StopMetaData"]["Transport"][i]["threads"][j]["BriefSchedule"]["Events"][g].keys())[0]
            print(data["data"]["properties"]["StopMetaData"]["Transport"][i]["threads"][j]["threadId"], cur, data["data"]["properties"]["StopMetaData"]["Transport"][i]["threads"][j]["BriefSchedule"]["Events"][g][cur]["value"])




            #print(data["data"]["properties"]["StopMetaData"]["Transport"][i]["threads"][j]["BriefSchedule"]["Events"][g]['Estimated']["text"])
#secs = int(data["data"]["properties"]["StopMetaData"]["Transport"][0]["threads"][0]["BriefSchedule"]["Events"][0]['Estimated']["value"])
#print(time.localtime(secs))
