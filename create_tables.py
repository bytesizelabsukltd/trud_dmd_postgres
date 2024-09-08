import os
import re
from dotenv import load_dotenv
from supabase import create_client, Client
from colorama import init, Fore, Style

def create_supabase_tables(sql_file_path):
    # Initialize colorama for cross-platform colored output
    init(autoreset=True)

    # Load environment variables
    load_dotenv()

    # Initialize Supabase client
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
    supabase: Client = create_client(supabase_url, supabase_key)

    def read_sql_file(file_path):
        with open(file_path, 'r') as file:
            return file.read()

    def extract_create_table_statements(sql_content):
        pattern = r'CREATE TABLE\s+(\w+)\s*\(([\s\S]*?)\);'
        matches = re.findall(pattern, sql_content, re.IGNORECASE)
        
        create_statements = []
        for table_name, table_content in matches:
            statement = f"CREATE TABLE IF NOT EXISTS {table_name} ({table_content});"
            create_statements.append((table_name, statement))
        
        return create_statements

    def execute_create_statements(statements):
        for table_name, statement in statements:
            try:
                result = supabase.rpc('execute_sql', {'sql': statement}).execute()
                print(f"{Fore.GREEN}✔ Created table: {Fore.YELLOW}{table_name}")
            except Exception as e:
                print(f"{Fore.RED}✘ Error creating table: {Fore.YELLOW}{table_name}")
                print(f"{Fore.RED}  Error: {str(e)}{Style.RESET_ALL}")

    print(f"{Fore.MAGENTA}Reading SQL file: {sql_file_path}{Style.RESET_ALL}")
    sql_content = read_sql_file(sql_file_path)
    
    print(f"{Fore.MAGENTA}Extracting CREATE TABLE statements...{Style.RESET_ALL}")
    create_statements = extract_create_table_statements(sql_content)
    
    print(f"{Fore.MAGENTA}Executing CREATE TABLE statements...{Style.RESET_ALL}")
    execute_create_statements(create_statements)
    
    print(f"\n{Fore.GREEN}Table creation process completed.{Style.RESET_ALL}")

# Example usage:
# if __name__ == "__main__":
#     create_supabase_tables('supabase_tables.sql')