class UserRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def _format_user(self, user_record):
        return {
            "id": user_record[0],
            "full_name": user_record[1],
            "email": user_record[2],
            "password": user_record[3],
        }
    
    def get_all(self):
        try:
            results = self.db_manager.execute_query(
                "SELECT id, full_name, email, password FROM lyfter_duad.users;"
            )
            formatted_results = [self._format_user(record) for record in results]
            return formatted_results
        except Exception as e:
            print(f"Error executing query: {e}")
            return False
        
    def create(self, full_name, email, password):
        try:
            self.db_manager.execute_query(
                "INSERT INTO lyfter_duad.users (full_name, email, password) VALUES (%s, %s, %s)",
                (full_name, email, password),
            )
            return True
        except Exception as e:
            print(f"Error inserting user into the database: {e}")
            return False
        
    def get_by_id(self, _id):
        try:
            results = self.db_manager.execute_query(
                "SELECT id, full_name, email, password FROM lyfter_duad.users WHERE id = %s;",
                (_id,),
            )
            formatted_results = self._format_user(results[0])
            return formatted_results
        except Exception as e:
            print(f"Error getting user from the database: {e}")
            return False
    
    def update(self, _id, full_name, email, password):
        try:
            self.db_manager.execute_query(
                "UPDATE lyfter_duad.users SET full_name = %s, email = %s, password = %s WHERE id = %s",
                (full_name, email, password, _id),
            )
            return True
        except Exception as e:
            print(f"Error updating user in the database: {e}")
            return False
        
    def delete(self, _id):
        try:
            self.db_manager.execute_query(
                "DELETE FROM lyfter_duad.users WHERE id = %s",
                (_id,),
            )
            print(f"User with ID {_id} deleted successfully.")
            return True
        except Exception as e:
            print(f"Error deleting user from the database: {e}")
            return False