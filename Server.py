import Pyro4
import sys
import fileParser
import random


@Pyro4.behavior(instance_mode = "single")
@Pyro4.expose
class Server:
    #initialising all needed variables
    ratings = fileParser.ratings
    movieInfo = fileParser.movieInfo
    updateLog = []
    replicaTS = [0,0,0]
    valueTS = [0,0,0]
    updateHistory = []
    allServers = []
    status = "online"
    #this function deals with any query request, only valid actions will be recieved from the frontend
    def query(self,timestamp,action,movie,userID): 
        #before doing the query, server checks timestamp to see if it needs to update
        Server.checkTS(timestamp)
        if action == "find": #defining the find action which returns info about the movie
            if movie in Server.ratings.keys():
        
                return "{0} was made in {1} and has the genres {2}".format(movie,Server.movieInfo[movie][0],Server.movieInfo[movie][1])
            else:
                return "{0} is not in our database yet".format(movie)
        elif action == "view":#defining the view action which shows the user rating
            if movie in Server.ratings.keys():
                if userID in Server.ratings[movie]:
                    return "The rating that user {0} gave to movie {1} was {2}".format(userID,movie,Server.ratings[movie][userID])
                else:
                    return "User has not rated that movie"
            else:
                return "{0} is not in our database yet".format(movie)
            
        elif action == "average":#defining the average action which shows the average movie rating
            if movie in Server.ratings.keys():
                total = 0
                ratings = 0
                for user in Server.ratings[movie].keys():
                    ratings += 1
                    total += Server.ratings[movie][user]
                return "{0} is the average rating for {1}".format(total/ratings,movie)
            else:
                return "{0} is not in our database".format(movie)
    #this function deals with any updates passed directly from the frontend (using the gossip architecture methods)
    def update(self,uOp,uPrev,uID): 
        if uID not in Server.updateHistory: # checks if the update has already been seen
            #does the necessary timestamp things as mentioned in the textbook about gossip architecture
            Server.replicaTS[serverNum] += 1
            ts = uPrev
            ts[serverNum] = Server.replicaTS[serverNum]
            Server.updateLog.append([serverNum,ts,uOp,uPrev,uID]) #adds update to update Log
            return ts #returns updated unique timestamp
        else:
            return 1
    #this function checks the timestamp from the frontend to see if an update is needed
    def checkTS(timestamp):
        requiresUpdate = False
        for i in range(len(Server.valueTS)):
            if Server.valueTS[i] < timestamp[i]: #checks which servers it needs an update from
                requiresUpdate = True
                if Server.allServers[i] != "current server":
                    #this gets the update logs from other servers if the current server needs it 
                    updates = Server.allServers[i].sendUpdates() 
                    Server.addToULog(updates) # adds updates to updateLog
        if requiresUpdate:#does the updates if it is out of date
            Server.doUpdates()
            
    def sendUpdates(self):
        return Server.updateLog #sends update log (for other servers)

    def addToULog(updates):#adds update to updateLog
        for item in updates:
            if item not in Server.updateLog:
                Server.updateLog.append(item)

    def doUpdates():#goes through updates causally 
        first = True
        foundStable = False
        for item in Server.updateLog:
            if item[4] not in Server.updateHistory:#checks update hasn't been done
                foundStable = True
                if first:#searches for the correct update for causal ordering
                    currentMin = item
                    first = False
                else:
                    if item[1] < currentMin[1]:
                        currentMin = item
        if foundStable:#if an update is found it will run doUpdates() again in case this update made other ones stable
            Server.execute(currentMin)
            Server.doUpdates()
        
    #this function takes update = [serverNum,ts,uOP,uPrev,uID] and executes it        
    def execute(newUpdate):
        uOP = newUpdate[2] #uOP = [action,movie,userID,rating]
        action = uOP[0]
        movie = uOP[1]
        userID = uOP[2]
        rating = uOP[3]

        if action == "rate":#defines the rate action which adds/updates a rating
            if movie in Server.ratings.keys():
                Server.ratings[movie][userID] = float(rating)
            
        elif action == "delete":#defines the delete action which deletes your rating
            if movie in Server.ratings.keys():
                try:#attempts to delete rating, if it doesn't exist then prints it
                    del Server.ratings[movie][userID]
                except:
                    print("rating never existed")
        
        Server.valueTS = Server.merge(Server.valueTS,newUpdate[1])#updates timestamp after each update
        Server.updateHistory.append(newUpdate[4])#adds uID to update history
        
        return  
    def merge(ts1,ts2):#merges 2 timestamps
        outputTS = [] 
        for i in range(len(ts1)):
            outputTS.append(max(ts1[i],ts2[i]))
        return outputTS
            
    def getOtherServers(self):#updates the list of other servers, this is called by the frontend when it's initialised
        with Pyro4.locateNS() as ns:
            servers = ns.list(prefix = "SERVER")
            for server in servers.keys():
                if str(server) == "SERVER" + str(serverNum):
                    Server.allServers.append("current server")
                else:
                    otherServer = Pyro4.Proxy(servers.get(server))
                    Server.allServers.append(otherServer)

    def getStatus(self): #returns the server status, has a 20% chance to be overloaded
        if Server.status != "offline":
            if random.random() < 0.8:
                Server.status = "online"
            else:
                Server.status = "over-loaded"
        return Server.status
        
    
    def changeStatus(self):#changes the server status to offline or online
        if Server.status == "online":
            old = Server.status
            Server.status = "offline"
        else:
            old = Server.status
            Server.status = "online"
        return "Server status changed from {0} to {1}".format(old,Server.status)
            
#initialising server with pyro          
print("SETTING UP SERVER")   

daemon = Pyro4.Daemon()
uri = daemon.register(Server)   


with Pyro4.locateNS() as ns:#registering server with name server (changes it's name based on how many servers there are)
    servers = ns.list(prefix="SERVER")
    serverNum = len(servers.keys())
    ns.register("SERVER"+str(serverNum),uri)
print("SERVER READY")
daemon.requestLoop()                  
