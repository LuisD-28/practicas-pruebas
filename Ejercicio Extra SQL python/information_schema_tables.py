from pg_manager import PgManager

def validate_system():
    try:
        # check db connection
        db = PgManager(
            dbname="postgres",
            user="postgres",
            password="280596",
            host="localhost"
        )
        
        # Check required tables
        required_tables = ['users', 'cars', 'rentals']
        for table in required_tables:
            db.cursor.execute(
                """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'lyfter_car_rental'
                    AND table_name = %s
                );
                """,
                (table,)
            )
            exists = db.cursor.fetchone()[0]
            if not exists:
                return f"Table '{table}' does not exist in the 'lyfter_car_rental' schema."
            
        # Check if the 'cars' table has at least one record
        db.cursor.execute(
            """
            SELECT COUNT(*) 
            FROM lyfter_car_rental.cars
            WHERE car_status = 'available';
            """
        )
        available_cars_count = db.cursor.fetchone()[0]

        if available_cars_count < 1:
            return "DB ERROR. No available cars found"
        
        return "System validation successful."
    
    except Exception as e:
        return f"DB connection error: {e}"
    
if __name__ == "__main__":
    result = validate_system()
    print(result)
