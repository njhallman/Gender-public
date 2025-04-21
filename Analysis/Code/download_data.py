#---------------------------------#
# Import packages and set optoins #
#---------------------------------#
print("Import packages and set options")

# Install misc packages
import pandas as pd; pd.set_option('display.max_columns', None); pd.set_option('display.float_format', lambda x: '%.2f' % x)
import shutil
import numpy as np
from datetime import datetime
import wrds
from tqdm import tqdm 
import warnings
import gc
import os

#--------------------------------#  
# Initialize connection to WRDS #
#--------------------------------#
print("You will be asked for WRDS credentials.")
conn = wrds.Connection()

#----------------------------------------------------------------------------#
# Define a set of roles for which we need to download user and position data #
#----------------------------------------------------------------------------#

# Define a set of roles for which we need to download user and position data
fsm = [
    "actuarial",
    "actuarial analyst",
    "actuary",
    "aml analyst",
    "audit",
    "auditor",
    "banking consultant",
    "broker",
    "brokerage",
    "business controller",
    "capital markets",
    "cfo",
    "commercial finance",
    "commercial underwriter",
    "controller",
    "credit analyst",
    "equity analyst",
    "equity research",
    "equity research analyst",
    "finance controller",
    "financial adviser",
    "financial analyst fp a",
    "financial consultant",
    "financial controller",
    "financial officer",
    "financial planner",
    "financial planning",
    "financial planning analysis",
    "financial planning analyst",
    "financial reporting",
    "financial reporting analyst",
    "fraud analyst",
    "fraud investigator",
    "investment analyst",
    "investment banking",
    "investment banking analyst",
    "investment consultant",
    "investments",
    "mergers acquisitions",
    "portfolio analyst",
    "pricing analyst",
    "project controller",
    "quantitative analyst",
    "sap fico consultant",
    "stock controller",
    "tax",
    "tax accountant",
    "tax analyst",
    "tax consultant",
    "trade finance",
    "trader",
    "trading",
    "underwriter",
    "underwriting"
]


#---------------------------------#
# Download user and position data #
#---------------------------------#
print("Downloading user and position data in batches (one batch per role). The process will take a several minutes per role.")

# Loop through each batch
for role in tqdm(fsm):

    # Generate the default file name (original path)
    # Create directory if it doesn't exist
    os.makedirs('/workspaces/Gender-public/Analysis/Data/Revelio/CurrentData', exist_ok=True)
    file_name = f'/workspaces/Gender-public/Analysis/Data/Revelio/CurrentData/revelioPosUsr_role_{role}.feather'
    
    # Check if the file already exists at the chosen path
    if os.path.exists(file_name):
        continue
    elif 'conn' in globals() and conn is not None:
        pass
    else:
        conn = wrds.Connection()

    # Write query to get the user and position data
    query = f"""
        SELECT pos.*, pos_raw.*, user_raw.*, usr.*
        FROM revelio.individual_positions AS pos
        JOIN revelio.individual_positions_raw AS pos_raw
            ON pos.position_id = pos_raw.position_id
        JOIN revelio.individual_user_raw AS user_raw
            ON pos.user_id = user_raw.user_id
        JOIN revelio.individual_user as usr
            ON pos.user_id = usr.user_id
        WHERE pos.role_k1500 = '{role}'
        AND usr.user_country IN ('United States')
        AND pos.country IN ('United States')"""

    # Submit query to get the user and position data
    pos_user_result = conn.raw_sql(query)

    # Drop duplicate columns
    pos_user_result = pos_user_result.loc[:, ~pos_user_result.columns.duplicated()]

    # Save the file
    pos_user_result.to_feather(file_name, compression='zstd')

    # Release memory by deleting the dataframe and forcing garbage collection
    del pos_user_result
    gc.collect()


#--------------------------------------------------------------------------#
# Create a list of user_ids for which we need to download educational data #
#--------------------------------------------------------------------------#

# Get a list of files in the ../Data/Revelio directory that don't contain 'Edu' or 'FsPosUsr' in their name and which don't start with .
files = [os.path.join("/workspaces/Gender-public/Analysis/Data/Revelio/CurrentData", f) for f in os.listdir('/workspaces/Gender-public/Analysis/Data/Revelio/CurrentData') if f.startswith("revelioPosUsr_role_")]


# Read and concatenate
pos_user_combined = pd.concat([pd.read_feather(f) for f in files], ignore_index=True)

# Create a list of unique user IDs for whom we need to download educational data
user_list = pos_user_combined['user_id'].unique()


#----------------------------------------#
# Download educational data in one batch #
#----------------------------------------#
print("Downloading educational data in one batch")

# Define the target file path
target_file_path = '/workspaces/Gender-public/Analysis/Data/Revelio/CurrentData/revelioEdu_role_combined.feather'

# Check if the file already exists
if os.path.exists(target_file_path):
    print(f"File {target_file_path} already exists, skipping download.")
else:
    # Write query to get the education data
    query = f"""
        SELECT usr_edu.*
        FROM revelio.individual_user_education as usr_edu
        WHERE usr_edu.user_id IN ({', '.join(str(user_id) for user_id in user_list)})"""
    
    # Submit query to get the education data
    print("Executing SQL query to fetch education data...")
    edu_result = conn.raw_sql(query)
    
    # Save the results
    print(f"Saving data to {target_file_path}")
    edu_result.to_feather(target_file_path, compression='zstd')

print("Downloads complete")