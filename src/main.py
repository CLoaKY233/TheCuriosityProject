# from surrealdb import RecordID, Surreal

# # Connect to the SurrealDB instance
# db = Surreal(
#     "wss://cloakystores-06a9f7u3jlrsf43q77o8ttu1kk.aws-euw1.surreal.cloud"
# )

# # Authenticate with the database
# db.signin({
#     "username": "cloaky",
#     "password": "timsp",
# })

# # Select the namespace and database
# db.use("curiosity", "curiosity")

# # Create nodes (e.g., people)
# db.create(RecordID("person", "john"), {"name": "John Doe", "age": 30})

# db.create(RecordID("person", "jane"), {"name": "Jane Smith", "age": 28})

# # Create an edge (relationship) between nodes
# db.query("""
#     RELATE person:john->knows->person:jane
#     SET since = time::now()
# """)

# # Query the graph to find relationships
# result = db.query("""
#     SELECT ->knows->person AS friends
#     FROM person:john
#     FETCH friends
# """)

# # Print the result
# print(result)

# # Close the connection
# db.close()
