"""
Abel Maldonado
Class: CS 521 - Fall 1
Date: 10/19/2024
Final Project (user-defined class)
"""

import json
import hashlib
import os
import time

class userDB:
   """This class registers users and stores their hashed credentials in a JSON file"""
   def __init__(self, filename="user_data.json"):
      self.filename = filename   # public attribute
      self.__user_data = {}      # dictionary for username and pws; private attribute
      self.__usernames = set()   # set of usernames
      self.user_count = 0        # public attribute
      self.login_attempts = 0    # counts login
      self.cooldown = False      # cooldown initialization
      self.cooldown_end = 0      # cooldown end
      self.current_user = None   # confirms logged in user

      file_path = self.find_file(self.filename) # looks for filename
      if file_path:     
         self.filename = file_path  # update file attribute if found
         self.load_user_data()      # load user data from existing file
      else:
         self.create_user_file()    # uses create_user_file method if file does not exist

   def find_file(self, filename, spath="."):    # "input" file
      """Locates database file"""
      files_found = []     # list to store found file paths
      for root, dirs, files in os.walk(spath):  # recursive search
         if filename.lower() in (f.lower() for f in files): # disregard capitalization
            f_path = os.path.join(root, filename)
            files_found.append(f_path)       # adds file path to list if file found
            print(f"User database found: {f_path} \nPlease Wait...")

      return files_found[0] if files_found else None # return first found file path if found, else None
      
   def create_user_file(self):      # output file
      """Creates database file"""
      with open(self.filename, "w") as file:
         json.dump({}, file)
      print(f"Creating user database: {self.filename}")

   def load_user_data(self):
      """Loads database file"""
      try:
         with open(self.filename, "r") as file:
            self.__user_data = json.load(file)
            self.user_count = len(self.__user_data)
            self.__usernames = set(self.__user_data.keys())
      except (FileNotFoundError, json.JSONDecodeError):
         print("Error loading user data. New file created")
      else:    # try-else 
         print(f"Loaded {self.user_count} user(s) from {self.filename}")

   def save_user_data(self):
      """Saves database file"""
      try:
         with open(self.filename, "w") as file:
            json.dump(self.__user_data, file)
      except IOError as e:
         print(f"Error while saving data: {e}")

   def __salt(self):
      """Creates a random salt"""
      return os.urandom(16).hex() # 16 random bytes and convert them to a hexadecimal string
   
   def __user_exists(self, username):
      """Checks if user already exists"""
      return username in self.__usernames # return True if username found
   
   def hash_pw(self, password, salt):
      """Hashes password using a random salt (__salt)"""
      return hashlib.sha256((salt + password).encode('utf-8')).hexdigest() # combine salt and password, encode to bytes, and hash result with SHA-256
   
   def reg_user(self):
      """Registers users"""
      print("\nRegister User")
      user = input("Register username: ")
      password = input("Enter a password: ")

      if self.__user_exists(user):  # check if username exists
         print("Username already exists. Try another username")
         return False   # registration fails if username exists
      
      salt = self.__salt() # generates a random salt for password hashing
      hashed_pass = self.hash_pw(password, salt) # hash the password with salt

      self.__user_data[user] = {'password': hashed_pass, 'salt': salt}
      self.__usernames.add(user) # add username to set of existing username
      self.user_count += 1    # increment user count

      print(f"\"{user}\" registered successfully")
      self.save_user_data()   # save updated user date to file
      return True       # successful registration
   
   def login(self):
      """Authenticates user by checking credentials; sets cooldown for failed login attempts"""
      current_time = time.time()

    # Check if the user is on cooldown
      if self.cooldown:
         if current_time < self.cooldown_end:   # check if still on cooldown
            remaining_time = self.cooldown_end - current_time
            print(f"\nToo many failed attempts. Wait {remaining_time:.0f} seconds to try again")
            return False   # login fails if in cooldown
         else:
            # cooldown period has ended
            self.cooldown = False
            self.login_attempts = 0  # reset attempts after cooldown

      print("\nLogin with Proper Credentials")
    
      user = input("Enter username: ")
      password = input("Enter password: ")

      if user not in self.__user_data:    # check if the username exists 
         print("Username does not exist")
         self.login_attempts += 1   # increment login attempts 
         return False   # deny login 

      stored_pw = self.__user_data[user]['password']  # get stored hashed password
      salt = self.__user_data[user]['salt']  # stored salt
      hashed_pw = self.hash_pw(password, salt) # hash the entered pw with salt

      if hashed_pw == stored_pw: # check if hashed password matches stored
         print("Login successful")
         self.login_attempts = 0  # reset attempts on successful login
         self.current_user = user   # set current user
         return True    # successful login
      else:
         print("Login failed")
         self.login_attempts += 1   # increment login attempts

         if self.login_attempts >= 3:
            self.cooldown = True    # start cooldown
            self.cooldown_end = current_time + 120  # 120 seconds cooldown
            print("\nToo many failed attempts. You are now on cooldown for 120 seconds.")
         return False   # deny login

   def __repr__(self):
      """Returns total login attempts and cooldown time"""
      return (f"Total login attempts = {self.login_attempts}, "
              f"Cooldown = {self.cooldown}")
   
   def __len__(self):
      """Returns user count"""
      return self.user_count