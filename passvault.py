"""
Abel Maldonado
Class: CS 521 - Fall 1
Date: 10/19/2024
Final Project (main program)
"""

import json
from user_db_udc import userDB   # import UserDB class

services = {} # stores services and their credentials

def add_service(service, username, password):
   """Stores service-specific credentials"""
   service = service.lower()
   services[service] = {"Username":username, "Password":password}
   print(f"\n{service} added successfully")

def get_service(service):
   """Returns service-specific credentials, if the specified service exists"""
   service = service.lower()
   if service in services: # check if the service exists in the dict
      username = services[service]["Username"]
      password = services[service]["Password"]
      return (username, password)   # return credentials as tuple
   else:
      print("\nService not found")
      return None  # return None if service is not found

def all_services(user):
   """Prints all the service-credentials inputted by the user"""
   print(f"\nAll services for {users.current_user}: ")
   if not services:  # check if no there are no services stored
      print("No services found")
   
   for service, credentials in services.items(): # loop through services dict
      if credentials["Username"] is not None:   # check if username exists
         print(f"Service: {service}\nUsername: {credentials['Username']}\nPassword: {credentials['Password']}\n")

def save_services():
   """Saves all of the user's credentials to a file"""
   try:
      with open("all_services.json", "w") as file:
         json.dump(services, file)  # save services dictionary as JSON
      print("All saved credentials saved to 'all_services.json'")
   except IOError as e: # Handle file I/O errors
      print(f"Error saving file: {e}")

if __name__ == "__main__":
   """Main program """
   users = userDB()  # instance of UserDB class
   print("Now entering PassVault...")

   while True:
      print("\nMenu:")
      print("1. Register")
      print("2. Login")
      print("3. Exit")

      choice = input("Select an option: ")

      if choice == "1":
         register = users.reg_user()   # register user

      elif choice == "2":
         if users.login():    # login user
            while True:
               print(f"\nWelcome '{users.current_user}'!")
               print("1. Add Service")
               print("2. Retrieve Service Information")
               print("3. View All Saved Services")
               print("4. Save Information to File")
               print("5. Logout")

               login_choice = input("Select an option: ")

               if login_choice == "1":
                  service = input("Enter service: ")
                  username = input(f"Username for {service}: ")
                  password = input(f"Password for {service}: ")
                  add_service(service, username, password)  # store credentials

               elif login_choice == "2":
                  service = input("Enter service: ")
                  serv_info = get_service(service) # retrieve specific credential

                  if serv_info:  # print credentials for saved services
                     username, password = serv_info   # unpack tuple
                     print(f"\nService: {service}\nUsername: {username}\nPassword: {password}")

               elif login_choice == "3":
                  all_services(users.current_user) # view all saved services

               elif login_choice == "4":
                  save_services()   # save service information to file

               elif login_choice == "5":
                  print("\nLogging out...")
                  break    # break login menu

               else:
                  print("Invalid input. Try again")

      elif choice == "3":
         print("\nExiting program...")
         break # break main loop

      else:    # input validation for main menu 
         print("Invalid input. Try again")