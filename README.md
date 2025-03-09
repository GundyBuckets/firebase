# Overview

This is a basic python program to access my zelda games cloud NoSQL database. I wrote this program to help me learn more about accessing cloud databases and how to integrate them with programs.

This program allows you to find data from the zelda games database, insert a new game, delete a game, or modify an already existing game. In order to run the program, you will need to make your own private key since for security reasons, I will not be including one. You can make a key by creating a new realtime database on firebase and import the included JSON file in the repository. You will then need to make a .env file with the following global variables, FIREBASE_CREDENTIALS_PATH which will be the path to your private key, and FIREBASE_DATABASE_URL which is the URL to the database.

[Software Demo Video](https://youtu.be/vhvHvr5cQsg)

# Cloud Database

This program uses a realtime database provided by Firebase. It is in JSON format and test_zelda_games.json is a copy of the JSON file if you would like to see the format

# Development Environment

Visual Studio Code 1.98

Python 3.12.9

## Libraries
firebase_admin
dotenv

# Useful Websites

- [Firebase Realtime Database Documentation](https://firebase.google.com/docs/database)

# Future Work

- Implement User Authentication
- A GUI
- Photos