import pandas as pd

# Create a new dataframe named target_df
target_df = pd.DataFrame()

# Copy the 'case_date' column from source_df to the 'CaseDate' column in target_df without any transformation
target_df['CaseDate'] = source_df['case_date']

# Concatenate the 'firstname' and 'lastname' columns from source_df (with a space in between) and store the result in the 'FullName' column in target_df
target_df['FullName'] = source_df['firstname'] + " " + source_df['lastname']

# Copy the 'case_type' column from source_df to the 'CaseType' column in target_df without any transformation
target_df['CaseType'] = source_df['case_type']

# Return the target_df as the output of the script
target_df