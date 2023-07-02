from rich.console import Console
from rich.table import Table

import getpass
import os
import sys
import json

console=Console()
table=Table(title="Configuration Details",title_justify="center")

print("Enter Configuration details",end="\n\n")
print("Configure TOKENS")
open_ai_token=input("OpenAI Token: ")
print("\n\n")

print("Configure HTTP")
http_host=input("HTTP Host: ")
print("\n\n")

print("Configure DB")
db_host=input("DB Host: ")
db_name=input("DB Name: ")
db_user=input("DB User: ")
db_pass=getpass.getpass("DB Password: ")
print("\n\n")
print("Application Secret Key")
secret_key=input("Key: ")

table.add_column("Keys",justify="left")
table.add_column("Values",justify="left")

table.add_row("Token Configuration","",style="bold")
table.add_row("OpenAI Token",open_ai_token)
table.add_section()
table.add_row("Database Configuration","",style="bold")
table.add_row("DB Host",db_host)
table.add_row("DB User",db_user)
table.add_row("DB Name",db_name)
table.add_row("DB Password",db_pass)
table.add_section()
table.add_row("HTTP Configuration","",style="bold")
table.add_row("HTTP Host",http_host)
table.add_section()
table.add_row("App Configuration","",style="bold")
table.add_row("Secret Key",secret_key)


console.print(table)
data={"db":{"user":db_user,"password":db_pass,"host":db_host,"database":db_name},"http":{"host": http_host},"tokens":{"openai":open_ai_token}}
commit_option=input("Commit? (y/n): ")
if commit_option.lower() == 'y':
    if os.path.isfile("config.json") == False:
        with open("config.json","a") as f:
            json.dump(data,f)
            f.close()
    else:
        print("Overwriting File")
        with open("config.json","w") as f:
            json.dump(data,f)
            f.close()
        
elif commit_option.lower() == 'n':
    sys.exit("Did not Commit. No operation Performed")

else:
    sys.exit("Wrong Option")





