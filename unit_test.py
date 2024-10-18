"""
Abel Maldonado
Class: CS 521 - Fall 1
Date: 10/19/2024
Final Project (unit test)
"""

from user_db_udc import userDB

'''Create a username and password, then login with that username and password'''
if __name__ == "__main__":
   """Two unit tests for public class methods"""
   users = userDB("test_user_data.json") # create instance of UserDB

   register = users.reg_user()      # call register method
   assert register, "User registration failed"  # first unit test
   print("\nreg_user method successful")

   login = users.login()   # call login method
   assert login == True, "User login failed"    # second unit test
   print("\nlogin method successful")

   print("\nUnit tests successful")