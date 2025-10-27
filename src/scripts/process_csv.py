import os
import sys
import pandas as pd
import numpy as np

# Get the input directory from the command line arguments
input_dir = sys.argv[1]

# Read the SD_length_grid_index.csv file
sd_length_df = pd.read_csv(os.path.join(input_dir, 'SD_length_grid_index.csv'), sep='\t')
sd_length_df = sd_length_df[['file', 'SD length']]
sd_length_df.rename(columns={'SD length': 'SD_length'}, inplace=True)

# Get the list of CSV files in the directory, excluding all_params.csv and SD_length_grid_index.csv
files = [f for f in os.listdir(input_dir) if f.endswith('.csv') and f not in ['all_params.csv', 'SD_length_grid_index.csv']]

# Create a list to store data for each file
data_list = []

# Loop through each CSV file
for i, f in enumerate(files):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(os.path.join(input_dir, f), sep='\t')

    # Rename columns
    df.rename(columns={'Perim.': 'Perimeter', 'Circ.': 'Circularity'}, inplace=True)

    # Convert columns to numeric, coercing errors to NaN
    df['Perimeter'] = pd.to_numeric(df['Perimeter'], errors='coerce')
    df['Circularity'] = pd.to_numeric(df['Circularity'], errors='coerce')

    # Calculate the average of the columns
    avg_perimeter = df['Perimeter'].mean()
    avg_circularity = df['Circularity'].mean()

    # Extract the group and animal ID from the file name
    group = f.split('_')[0]
    animal_id = f.split('_')[1]
    file_base = f.replace('_fp_params.csv', '')

    # Get the SD_length from the sd_length_df
    sd_length_row = sd_length_df[sd_length_df['file'] == file_base]
    sd_length = sd_length_row.iloc[0]['SD_length'] if not sd_length_row.empty else None

    # Append the data to the list
    data_list.append({
        'ID': i + 1,
        'File': file_base,
        'Group': group,
        'Animal ID': animal_id,
        'Perimeter': avg_perimeter,
        'Circularity': avg_circularity,
        'SD_length': sd_length
    })

# Create the all_data DataFrame from the list of dictionaries
all_data = pd.DataFrame(data_list)

# Calculate the average for each animal
animal_avg = all_data.groupby(['Group', 'Animal ID'])[['Perimeter', 'Circularity', 'SD_length']].mean().reset_index()

# Calculate the average for each group
group_avg = all_data.groupby(['Group'])[['Perimeter', 'Circularity', 'SD_length']].mean().reset_index()

# Create an Excel writer object
output_path = os.path.join(input_dir, 'delivery.xlsx')
writer = pd.ExcelWriter(output_path, engine='xlsxwriter')

# Write the three DataFrames to a new sheet in the Excel file
all_data.to_excel(writer, sheet_name='Results', index=False)
animal_avg.to_excel(writer, sheet_name='Results', startcol=all_data.shape[1] + 2, index=False)
group_avg.to_excel(writer, sheet_name='Results', startcol=all_data.shape[1] + 2 + animal_avg.shape[1] + 2, index=False)

# Save the Excel file
writer.close()

print(f"Successfully created {output_path}")
