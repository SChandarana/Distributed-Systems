@echo off
start cmd /k pyro4-ns
timeout /t 3
for %%x in (1,1,3) do (start cmd /k python Server.py & timeout /t 2)
timeout /t 7	
start cmd /k python FrontEnd.py
timeout /t 1
start cmd

