# Distributed Systems Gossip architecture system instructions:

## This code has been made to work on windows machines, as such running it on linux can encounter some error messages (i.e. cls has been used instead of clear to clear the terminal)

1. Navigate to the file directory in cmd and run startServer.bat
2. The batch file should open 3 servers, a frontend and another cmd ready to run the client
3. Wait for the frontend to say "CLIENT CAN NOW CONNECT" (may take a while as pyro nameservers are slow)
4. In the cmd that has nothing running type "python Client.py" to start the client
5. Follow the instructions on screen to use the system(an example on testing the system functionality will follow)

## **IF THIS FAILS THEN THE FOLLOWING MANUAL SETUP IS REQUIRED**
1. Open up 5 command prompt windows and navigate to the file directory
2. In the first, run "pyro4-ns"
3. In three others run "python Server.py"
4. Once the servers all say "SERVER READY" run "python FrontEnd.py" 
5. Once the frontend says "CLIENT CAN NOW CONNECT" run "python Client.py" and follow onscreen instructions

The client has several different queries and updates it can make which are all outlined when you run the client. 

## TEST EXAMPLE: (note the client will prompt for another input if the one you entered was invalid)
1. Enter a number for the userID, in my tests I used "1"
2. Use "view" on a movie to see that users' rating for a movie in the system. I used "Toy Story"
3. Use "rate" on that same movie to update it's rating for the user
4. Use "view" again to see if the update went through
5. Use "change" to change server 1's status to offline (the frontend uses servers in order unless they are offline or busy)
6. Use "view" again to see if the other servers have recieved the update
7. Use "change" on servers 2 and 3 to make all servers offline
8. Attempt to use a function, expected output should be "all servers are currently busy"
9. This should show off all the features, it can work across multiple clients too (i.e. another cmd with Client.py running)
10. Make sure to use "change" on the servers to make them online again

# Overview of functionality:
Whilst this is all shown when the client runs, here is an overview of the capabilities of this system. (more details on how it works can be seen in comments throughout the code)

1. Find out information about a movie
2. Find the current user's rating of a movie
3. Find the average rating for a movie
4. Change/Add a rating to a movie
5. Delete your rating for a movie
6. Change a server status between online and offline
7. Quit the system
8. The system has a 20% chance of being "over-loaded" rather than online
9. The system uses causal ordering for updates and recieves gossip messages when needed, handling the timestamping and updates when required
10. The system takes a while to boot up due to nameserver functions being slow in python
