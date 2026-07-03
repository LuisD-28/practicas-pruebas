from pg_manager import PgManager
import os
import csv
from datetime import datetime

# Db connection parameters
db = PgManager(
    dbname='postgres',
    user='postgres',
    password='280596',
    host='localhost',
)

# Backup directory
current_date = datetime.now().strftime("%Y-%m-%d")
backup_dir = f"backup_{current_date}"

os.makedirs(backup_dir, exist_ok=True)

# Export tables Function
def export_table_to_csv(table_name, file_name):
    try:
        query = f"SELECT * FROM lyfter_car_rental.{table_name}"

        db.cursor.execute(query)
        rows = db.cursor.fetchall()

        column_names = [desc[0] for desc in db.cursor.description]
        
        # Create CSV file
        file_path = os.path.join(backup_dir, file_name)

        with open(file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)

            # Headers
            writer.writerow(column_names)

            # Data rows
            for row in rows:
                writer.writerow(row)

        print(f'Backup created: {file_path}')

    except Exception as e:
        print(f"Error exporting table {table_name} to CSV: {e}")

# Export each table
export_table_to_csv('users', f'users_backup_{current_date}.csv')
export_table_to_csv('cars', f'cars_backup_{current_date}.csv')
export_table_to_csv('rentals', f'rentals_backup_{current_date}.csv')

print("Backup completed successfully.")