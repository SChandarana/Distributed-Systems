import Pyro4
import os
print("CONNECTING TO FRONTEND")
#finding the frontend
with Pyro4.locateNS() as ns:
    uri = ns.lookup("FRONTEND")

frontend = Pyro4.Proxy(uri)


#instructions for using the UI
def information():
    print("\nWelcome to the MovieLens Database, Here are the things you can do:")
    print("To find out information about a movie, type 'find'")
    print("To view your rating for a movie type, 'view'")
    print("To see the average rating for a movie, type 'average'")
    print("To add or update your rating for a movie, type 'rate'")
    print("To delete your rating for a movie, type 'delete'")
    print("[TESTING ONLY] To change a server's status between online and offline, type 'change'")
    print("To quit, type 'quit'\n")

#userID obtained before any actions can be made
userID = ""
while userID == "":
    userID = input("Please enter your userID: ")
    if not userID.isdigit():
        userID = ""
        print("\nINVALID\n")
    
#gets a user instruction, this whole section handles user inputs and makes sure everything they send to the front end is a valid input
userInstruction = ""
while userInstruction == "": #will keep asking for instructions unless the user wants to quit
    information()
    queryActions = ["find","view","average"]#all query actions
    updateActions = ["rate","delete"]#all update actions

    userInstruction = input("\nWhat would you like to do? ")
    action = userInstruction.lower()
    if action in queryActions:#queries
        movie = input("\nWhat is the name of the movie? ")
        while movie == "":
            print("\nDon't leave it blank!")
            movie = input("\nWhat is the name of the movie? ")
        os.system('cls')
        print("\n"+frontend.userQuery(action,movie,userID))
    elif action in updateActions:#updates
        rating = 0
        movie = input("\nWhat is the name of the movie? ")
        while movie == "":
            print("\nDon't leave it blank!")
            movie = input("\nWhat is the name of the movie? ")
        if action == "rate":
            invalid = True
            while invalid == True:
                invalid = False
                rating = input("\nWhat rating would you like to give it(0-5)? ")
                try:
                    float(rating)
                except ValueError:
                    invalid = True
                    print("\nINVALID")
                if not invalid:
                    if not 0 <= float(rating) <= 5:
                        invalid = True
                        print("\nINVALID")
                
        os.system('cls')    
        print(frontend.userUpdate(action,movie,userID,rating))
    elif action == "change":#changing server state

        
        while True:
            server = input("Which server's state would you like to change?(1-3) ")
            if server.isdigit():
                if 1 <= int(server) <= 3:
                    break
                else:
                    print("\nINVALID")
            else:
                print("\nINVALID")
        os.system('cls')
        print(frontend.changeStatus(int(server)-1))
    
    
    
    if action == "quit":#quitting
        os.system('cls')
        print("\nOkay thanks for coming!")
        
    else:
        userInstruction = ""
        
   
        
        
