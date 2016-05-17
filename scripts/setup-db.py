from pymongo import MongoClient

client = MongoClient()
connection = client.test

connection.create_collection("projects")
connection.create_collection("users")
connection.create_collection("roles")
connection.create_collection("paygrades")

projects = connection.projects
users = connection.users
roles = connection.roles
paygrades = connection.paygrades

roles.insert_one({"title": "Admin"})
roles.insert_one({"title": "All Staff"})
roles.insert_one({"title": "Delivery Manager"})

users.insert_one({ "_id" : "ADMIN", "password" : "pbkdf2:sha1:1000$l6RzU94o$dd8d80a18509fa2f3d1f6f5b6ed9d42bf3b41bab", "paygrade" : "RE1", "workdays" : { "Thursday" : "7.5", "Wednesday" : "7.5", "Friday" : "7.5", "Monday" : "7.5", "Tuesday" : "7.5" }, "lastname" : "User", "role" : "Admin", "firstname" : "Admin" })

paygrades.insert_one({ "_id" : "RE2L", "hourly_rate" : 12 })
paygrades.insert_one({ "_id" : "RO", "hourly_rate" : 10 })
paygrades.insert_one({ "_id" : "RE2U", "hourly_rate" : 14 })
paygrades.insert_one({ "_id" : "RE1", "hourly_rate" : 16 })

projects.insert_one({ "_id" : "P1", "name" : "Project 1" })
projects.insert_one({ "_id" : "P2", "name" : "Project 2" })
projects.insert_one({ "_id" : "P3", "name" : "Project 3" })
projects.insert_one({ "_id" : "P4", "name" : "Project 4" })
projects.insert_one({ "_id" : "P5", "name" : "Project 5" })
projects.insert_one({ "_id" : "LEAVE", "name" : "Leave" })
projects.insert_one({ "_id" : "OLEAVE", "name" : "Other Leave" })

