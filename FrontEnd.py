import Pyro4
serverList = []
print("POPULATING SERVER LIST")
with Pyro4.locateNS() as ns:#initialises list of servers using name server
    servers = ns.list(prefix = "SERVER")
    for server in servers.keys():
        serverList.append(Pyro4.Proxy(servers.get(server)))
        

print("SERVERS FOUND AND CONNECTED")

@Pyro4.expose
class FrontEnd:
    #initialising timestamp and update ID
    ts = [0,0,0]
    uID = 0
    #this function takes a user query action and attempts to execute it on one of the servers
    def userQuery(self,action,movie,userID):
        
        for server in serverList:#attempts each server in the list to see if one is online
            if server.getStatus() == "online":
                return server.query(FrontEnd.ts,action,movie,userID)
        #if all servers are offline or overloaded it tells the client
        return "All servers are currently busy, please try again later"
        
        
    #this function takes a user update and attempts to send it to a server           
    def userUpdate(self,action,movie,userID,rating):
        
        for server in serverList:
            if server.getStatus() == "online":
                #sends update to online server and gets a timestamp back
                newTS = server.update([action,movie,userID,rating],FrontEnd.ts,FrontEnd.uID)
                if newTS != 1:#if the server already did the update then don't worry
                    FrontEnd.uID += 1
                    FrontEnd.ts = FrontEnd.merge(FrontEnd.ts,newTS)
                    return "Your update has been sent"
        
        return "All servers are currently busy, please try again later"

    def merge(ts1,ts2):#merges two timestamps
        outputTS = [] 
        for i in range(len(ts1)):
            outputTS.append(max(ts1[i],ts2[i]))
        return outputTS
    
    def changeStatus(self,serverNum):#changes server status
        return serverList[serverNum].changeStatus()
   
#creating frontend server and adding it to the name server
print("REGISTERING FRONT END SERVER") 
daemon = Pyro4.Daemon()
uri = daemon.register(FrontEnd)


#making sure all servers know eachother before being ready for client connection
for server in serverList:
    server.getOtherServers()

with Pyro4.locateNS() as ns:
    ns.register("FRONTEND",uri)

print("CLIENT CAN NOW CONNECT")
daemon.requestLoop()
