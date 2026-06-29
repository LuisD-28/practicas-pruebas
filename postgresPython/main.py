from db import PgManager
from repositories import UserRepository


db_manager = PgManager(
    dbname="postgres",
    user="postgres",
    password="280596",
    host="localhost"
)

user_repo = UserRepository(db_manager)

# new_user = user_repo.create("John Doe", "john.doe@example.com", "password123")
# print("User created:", new_user)

# user = user_repo.get_by_id(7)
# print("User with ID 7:", user)

# updated_user = user_repo.update(7, "Jane Doe", "jane.doe@example.com", "newpassword456")
# print("User updated:", updated_user)

# deleted_user = user_repo.delete(7)
# print("User deleted:", deleted_user)

print("Query executed")
formatted_results = user_repo.get_all()
print(formatted_results)





# def format_user(user_record):
#     return {
#         "id": user_record[0],
#         "full_name": user_record[1],
#         "email": user_record[2],
#         "password": user_record[3],
#     }

# db_manager = PgManager(
#     dbname="postgres",
#     user="postgres",
#     password="280596",
#     host="localhost"
# )

# results = db_manager.execute_query("SELECT * FROM lyfter_duad.users")

# formatted_results = [format_user(record) for record in results]
# print("Query executed")
# print(formatted_results)

# db_manager.close_connection()
