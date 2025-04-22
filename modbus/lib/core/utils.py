#=========================================================================================
#   Name        :   utils.py
#   Date        :   4/10/2023
#   Version     :   1.0
#   Author      :   Shayan Sharif Zahid
#   Description :   This is a utils module that does the following:
#                       1.  Defines default variables
#                       2.  Defines DataSimUtils class
#                       3.  Contains all utiliy functions used to run the servers
#=========================================================================================

#Set path to current directory
import sys
import os
sys.path.append(os.path.join(os.sep,"ess_datasim","modbus","lib"))

#Import libraries
import socket
import logging
import pandas as pd
import asyncio
import argparse

#Variable definition
STR_DEFAULT_CSV_DATA_PATH               =       '/csv/'
STR_DEFAULT_JSON_DATA_PATH              =       '/json/'
STR_DEFAULT_LOG_FOLDER_PATH             =       'log'
STR_DEFAULT_CONFIG_FOLDER_PATH          =       'config'
STR_DEFAULT_LIB_FOLDER_PATH             =       'lib'
STR_DEFAULT_TIME_COLUMN_IDENTIFIER      =       'Timestamp'
STR_DETAULT_PROJECT_PATH_STRING         =       'ess_datasim'
STR_DEFAULT_MODBUS_SERVER_LOG_FILENAME  =       'modbus_server_log_runtime'
STR_DEFAULT_PLOT_LOG_FILENAME           =       'plot_log_runtime'
STR_DEFAULT_LOG_FILE_EXT                =       '.txt'
STR_DEFAULT_PLOT_DATA_EXT               =       '.png'
STR_DEFAULT_ASSET_TYPE                  =       'default'
STR_DEFAULT_SERVER_TAG_DATA_FILENAME    =       'default_tag_data'
STR_DEFAULT_SERVER_TAG_LIST_FILENAME    =       'default_tag_list'
STR_DEFAULT_CONFIG_FILEPATH             =       os.path.join(os.sep,"ess_datasim","modbus","config","csv")
STR_DEFAULT_PLOT_DATA_FILENAME          =       os.path.join(os.sep,"ess_datasim","modbus","doc")
DEFAULT_SIMULATOR_DATA_DURATION         =       '5T'
FLOAT_DEFAULT_PUBLISH_INTERVAL          =       1.0
DEFAULT_HOLDING_REG_FUNCTION_CODE_HEX   =       0x03

#Class definitions
class DataSimUtils:

    #=====================================================================================
    #   Class Name     :    DataSimUtils
    #   Description    :    Defines functions used for data server simulators
    #=====================================================================================

    def __init__(self):
        
        # All initialization happens in server level packages and classes 
        pass

    def get_ip_address(self, mode='dhcp',**kwargs):

        #=====================================================================================
        #   Function Name  :    get_ip_address
        #   Description    :    Gets the IP address of the machine where the script is running
        #=====================================================================================

        # Extract Keyword args
        obj_logger      =   kwargs.get('obj_logger', None)

        # Default IP address
        str_ip_address      =   "127.0.0.1"  

        try:
            # Check if obj_logger is provided and not None
            if obj_logger is not None:
                obj_logger.info(f"{'='*24}")
                obj_logger.info(f" Data Simulator Modbus \n{'='*24}")

            # Check the mode selected to determine how to get the IP address
            if mode     ==      'localhost':
                # If mode is 'localhost', set the IP address to the local loopback address
                str_ip_address      =   "127.0.0.1"

                # If obj_logger is provided, log the IP address being used
                if obj_logger:
                    obj_logger.info(f"Using Localhost IP: {str_ip_address}")

            elif mode   ==      'dhcp':
                # If mode is 'dhcp', get the hostname of the machine
                str_hostname    =   socket.gethostname()

                # Resolve the hostname to get the IP address
                str_ip_address  =   socket.gethostbyname(str_hostname)

                # If obj_logger is provided, log the server name and IP address
                if obj_logger:
                    obj_logger.info(f"Server Name   : {str_hostname}")
                    obj_logger.info(f"IP (DHCP)     : {str_ip_address}")
            else:
                # For any other mode, default to the local loopback address
                str_ip_address  =   "127.0.0.1"

                # If obj_logger is provided, log the default IP address being used
                if obj_logger:
                    obj_logger.info(f"Defaulting to Localhost IP: {str_ip_address}")

        except Exception as e:
            # In case of an exception, default to the local loopback address
            str_ip_address      =   "127.0.0.1"

            # If obj_logger is provided, log the error and the default IP address
            if obj_logger:
                obj_logger.info(f"Error in fetching IP, defaulting to {str_ip_address}. Exception: {e}")

        # Return the determined IP address
        return str_ip_address


    def set_logger(self,**kwargs):

        #=====================================================================================
        #   Function Name  :    set_logger
        #   Description    :    This function does the following:
        #                           1.  Sets up the logger object
        #                           2.  Sets the logger level as info
        #                           3.  Returns the logger object
        #=====================================================================================

        #Extract keyword args
        str_log_filename      =   kwargs.get('str_log_filename', None)
        
        # Create and configure logger
        logging.basicConfig(    
                                filename    =   "/ess_datasim/modbus/log/"+str_log_filename+STR_DEFAULT_LOG_FILE_EXT,
                                format      =   '%(message)s',
                                filemode    =   'w'
                            )

        # Creating an object
        obj_logger  =    logging.getLogger()

        # Setting the threshold of logger to INFO
        obj_logger.setLevel(logging.INFO)

        return obj_logger

    def get_lib_path(self, **kwargs):

        #=====================================================================================
        #   Function Name  :    get_lib_path
        #   Description    :    Returns the library path
        #=====================================================================================

        #Extract keyword args
        obj_logger      =   kwargs.get('obj_logger', None)

        print(f"\nPath Configuration:\n{'='*19}")

        #Get the list of system paths
        list_sys_path   =   sys.path

        #Loop through all paths in system path list
        for str_system_path in list_sys_path:
            
            #Check if data simulators string is found in the path
            if STR_DETAULT_PROJECT_PATH_STRING in str_system_path:
                
                #Check if lib string is in paths
                if 'lib' in str_system_path:
                    
                    #Log and print message
                    obj_logger.info(f"Lib Path      : {str_system_path}")
                    print(f"Lib Path Set        :   {str_system_path}")
                    
                    #Return path string
                    return str_system_path

    def get_config_path(self, **kwargs):

        #=====================================================================================
        #   Function Name  :    get_config_path
        #   Description    :    Returns the config path
        #=====================================================================================

        #Extract keyword args
        obj_logger              =   kwargs.get('obj_logger', None)

        try:
            str_lib_path        =   kwargs.get('str_lib_path', None)
            
            #Set config path by replacing 'lib' with 'config'
            str_config_path     =   str_lib_path.replace(STR_DEFAULT_LIB_FOLDER_PATH,STR_DEFAULT_CONFIG_FOLDER_PATH)
            
            #Log the config path
            obj_logger.info(f"Config Path   : {str_config_path}")
            
            print(f"Config Path Set     :   {str_config_path}")
            
            return str_config_path

        except:
            
            #Log error message
            obj_logger.info("Config Path Not Found")
            
            raise Exception("Config Path Not Found")

    def get_log_path(self, **kwargs):

        #=====================================================================================
        #   Function Name  :    get_log_path
        #   Description    :    Returns the log path
        #=====================================================================================

        #Extract keyword args
        obj_logger          =   kwargs.get('obj_logger', None)

        try:
            str_lib_path    =   kwargs.get('str_lib_path', None)
              
            #Set log path by replacing 'lib' with 'log'
            str_log_path    =   str_lib_path.replace(STR_DEFAULT_LIB_FOLDER_PATH,STR_DEFAULT_LOG_FOLDER_PATH)
            
            #Log/print message
            obj_logger.info(f"Log Path      : {str_log_path}")
            print(f"Log Path Set        :   {str_log_path}")
            
            return str_log_path

        except:
            
            #Log error message
            obj_logger.info("Log Path Not Found")
            
            raise Exception("Log Path Not Found")
        
    def convert_to_twos_complement(self,**kwargs):

        #=====================================================================================
        #   Function Name  :    
        #   Description    :    
        #                           
        #                  
        #=====================================================================================

        #Extract keyword args
        int_value                =   kwargs.get('int_value', None)

        if int_value < 0:

            return int(int_value + (1 << 16))
        
        return int_value
    
    def get_server_tag_list(self, **kwargs):

        #=======================================================================================
        #   Function Name  :    get_server_tag_list
        #   Description    :    This function does the following:
        #                       1.  Reads server tag list from a CSV
        #                       2.  Uses the dataframe to create a new dict with only addresses
        #                           and tag names in it.                      
        #=======================================================================================

        #Extract keyword args
        str_asset_type      =       kwargs.get('str_asset_type',None)
        str_filepath        =       kwargs.get('str_filepath', None)
        obj_logger          =       kwargs.get('obj_logger', None)

        #Initialize the dictionary
        dict_server_tags    =      {}

        #Create full path to CSV file
        csv_data_file_path  =     os.path.join(os.sep,str_filepath,str_asset_type+"_tag_list.csv")
        
        #Read the CSV file into a DataFrame
        df                  =      pd.read_csv(csv_data_file_path)
        
        #Iterate over DataFrame rows
        for _, row in df.iterrows():
            
            #Remove spaces from the 'name' value
            name        =    row['name'].replace(' ', '')
            
            #Get the 'address' value
            address     =    row['address']
            
            #Add the key-value pair to the dictionary
            dict_server_tags[name]  =   address
            
        #Log the server data tag generated
        obj_logger.info("Server Data Tag List Generated")

        return dict_server_tags
    
    def get_server_tag_data(self, **kwargs):

        #=====================================================================================
        #   Function Name  :    get_server_data
        #   Description    :    This function does the following:
        #                           1.  Read server data csv
        #                           2.  Remove 'Time' from the dataframe
        #                           3.  Return a new dict with tag name and its data as a list
        #=====================================================================================

        #Extract keyword args
        str_asset_type                  =   kwargs.get('str_asset_type',None)
        str_filepath                    =   kwargs.get('str_filepath', None)
        str_data_sample_duration        =   kwargs.get('str_data_sample_duration', None)
        obj_logger                      =   kwargs.get('obj_logger', None)

        #Initialize the dictionary
        dict_server_data    =    {}

        #Create full path to CSV file
        csv_data_file_path  =   os.path.join(os.sep,str_filepath,str_asset_type+"_tag_data_auto_gen.csv")

        #Read the CSV file into a DataFrame
        df  =   pd.read_csv(csv_data_file_path)
        
        #Resample dataframe according to the input
        print(f"Resample Duration   :   {str_data_sample_duration}")
        
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
       
        df.set_index('Timestamp',inplace=True)
       
        df  =   df.map(lambda x: self.convert_to_twos_complement(int_value=x) if x < 0 else x)
        
        #Convert DataFrame to dictionary
        dict_server_data     =  df.to_dict(orient='list')

        #Remove 'Time' key if it exists
        if STR_DEFAULT_TIME_COLUMN_IDENTIFIER in dict_server_data:
            del dict_server_data[STR_DEFAULT_TIME_COLUMN_IDENTIFIER]

       #Log the server data generated
        obj_logger.info(f"\n{'='*18}")
        obj_logger.info(f"  Data Generation \n{'='*18}")
        obj_logger.info("Server Data Generated")
        
        return dict_server_data

    def get_server_data_per_timestep(self,**kwargs):

        #=============================================================================================
        #   Function Name  :    get_server_data_per_timestep
        #   Description    :    This function does the following:
        #                           1.  Merges server_data dict and server_tag_list dict
        #                           2.  It takes the tag name(key) and its data as a list(value)
        #                           3.  Returns a dict like this : {'tag_name': [0,2,03,04,50]}
        #=============================================================================================

        #Extract keyword args
        dict_server_data        =   kwargs.get('dict_server_data', None)
        dict_server_tag_list    =   kwargs.get('dict_server_tag_list', None)
        obj_logger              =   kwargs.get('obj_logger', None)
        
        #Initialize variables
        dict_server_data_per_timestep = {}

        #Loop through all data tags
        for key in dict_server_data.keys():

            #Assign the Tag name as key and tag data(list) as value            
            dict_server_data_per_timestep[dict_server_tag_list[key]] = dict_server_data[key]
            
        # Node Data Added
        obj_logger.info(f"Node Data Added     :  {bool(dict_server_data_per_timestep)}")     
        
        return dict_server_data_per_timestep

    async def cyclic_value_generator(self,**kwargs):

        #=====================================================================================
        #   Function Name  :    cyclic_value_generator
        #   Description    :    This is an async function does the following:
        #                           1.  Generates cyclic values from a dictionary
        #                           2.  Outpus a generator that cycles through values 
        #                               everytime we call this function
        #=====================================================================================

        #Extract keyword args
        dict_server_data        =   kwargs.get('dict_server_data', None)
        float_publish_interval  =   kwargs.get('float_publish_interval', None)
        
        #Initialize variables
        index                   =   0
        dict_server_data_cyclic =   {}

        while True:
            
            for key, value_list in dict_server_data.items():
                
                #Compute the index using modulo operation
               
                computed_index                  =   index % len(value_list)
              
                #Retrieve the value from value_list using the computed index
                retrieved_value                 =   value_list[computed_index]
         
                #Wrap the retrieved value in a list
                wrapped_value                   =   [int(retrieved_value)]
               
                #Assign this list to the result dictionary with the key
                dict_server_data_cyclic[key]    =   wrapped_value
            
            yield dict_server_data_cyclic
            
            #Increment index
            index += 1
            await asyncio.sleep(float_publish_interval)