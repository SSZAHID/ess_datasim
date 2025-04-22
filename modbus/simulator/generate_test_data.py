#============================================================================================
#   Name        :   generate_test_data.py
#   Date        :   4/10/2023
#   Version     :   1.0
#   Author      :   Shayan Sharif Zahid
#   Description :   This module does the following:
#                   1.  Reads tag lists defined in the config/csv fodler
#                   2.  Creates a new tag_data file in the same folder which stores the data
#                   3.  The tag_data file has timestamped data for all tags
#                   4.  The data is different according to the data type assigned
#                   5.  Data types are( Short,BOOL,Word,DWord)
#                   6.  This script also scales the values and assigns an offset
#                   7.  The tag_data file is then used by start.py to run the simulator
#============================================================================================

#Set path to current directory
import sys
import os
sys.path.append(os.path.join(os.sep,"ess_datasim","modbus","lib"))

#Import libraries
from core import utils
import pandas as pd
from datetime import datetime, timedelta

#Variable definition
INT_TEST_DATA_DURATION  =   60
LIST_TAG_LIST_FILENAMES =   [
                                'default_tag_list',
                                'bms_tag_list',
                                'cnv_tag_list',
                                'inv_tag_list'
                            ]
#Function Definitions
def generate():
        
    #=====================================================================================
    #   Function Name  :  generate
    #   Description    :  Generates test data using base models for different data types
    #=====================================================================================

    #Print message
    print(f"\n{'='*24}\n{' '*3}Generate Test Data\n{'='*24}")
    print(f"\nTag Lists:",*LIST_TAG_LIST_FILENAMES,sep='\n')

    #Create a dict of the file paths with filenames
    dict_tag_list_filepaths =   {filename: os.path.join(utils.STR_DEFAULT_CONFIG_FILEPATH, filename+'.csv') for filename in LIST_TAG_LIST_FILENAMES}

    #Loop through all the tag lists 
    for str_tag_list_filepath in dict_tag_list_filepaths.values():
    
        try:
            #Read the tag list 
            df_tag_list     =   pd.read_csv(str_tag_list_filepath)

            #Initialize the DataFrame with a Timestamp column
            obj_start_time      =   datetime.now()
            list_timestamps     =   [obj_start_time + timedelta(minutes=i) for i in range(INT_TEST_DATA_DURATION)]
            dict_tag_data       =   {'Timestamp': list_timestamps}

            #Generate data for each register, '_' ignore timestamp column
            for _, row in df_tag_list.iterrows():

                #Define column names for the tag lists csv
                register_name   =   row['name']
                str_data_type   =   row['data type']
                scaling         =   row['scaling']
                offset          =   row['offset']
                
                #Base models for each data type
                if str_data_type == 'Short':
                    values  =   [(i % 60) - 30 for i in range(INT_TEST_DATA_DURATION)]
                elif str_data_type == 'Bool':
                    values =    [i % 2 for i in range(INT_TEST_DATA_DURATION)]
                elif str_data_type == 'Word':
                    values =    [i % 60 for i in range(INT_TEST_DATA_DURATION)]
                elif str_data_type == 'DWord':
                    values =    [i % 60 for i in range(INT_TEST_DATA_DURATION)]
                else:
                    raise ValueError(f"\nUnknown data type: {str_data_type}")

                #Apply scaling and offset
                values = [v * scaling + offset for v in values]

                #Add the values to the DataFrame
                dict_tag_data[register_name] = values
            
            #Create the DataFrame
            df = pd.DataFrame(dict_tag_data)

            #Generate the output filename by replacing "list" with "data"
            output_filename = os.path.basename(str_tag_list_filepath).replace("list", "data_auto_gen")

            #Update output path
            str_output_path = os.path.join(utils.STR_DEFAULT_CONFIG_FILEPATH, output_filename)

            #Save the DataFrame to a CSV file
            os.makedirs(os.path.dirname(str_output_path), exist_ok=True)
            df.to_csv(str_output_path, index=False)

            #Print message
            print(f"\nTest Data Generated: {os.path.basename(str_output_path)}")
        
        #Raise file exception
        except FileNotFoundError:
            print(f"\nError: The file was not found\n{str_tag_list_filepath}")

        #Raise permission exception
        except PermissionError:
            print(f"\nError: Permission denied while trying to open the file\n{str_tag_list_filepath}")

#Main entry point when script is run directly
if __name__ == '__main__':

    #Function Call
    generate()
