#=========================================================================================
#   Name        :   modbus_simulator.py
#   Date        :   4/10/2023
#   Version     :   1.0
#   Author      :   Shayan Sharif Zahid
#   Description :   This is a modbus server module which has classes for Modbus Simulator
#                   The class DataSimStartServer does the following:
#                       1.  Read configs
#                       2.  Get data for modbus server
#                       3.  Start modbus server
#=========================================================================================

#Set path to current directory
import sys
import os
sys.path.append(os.path.join(os.sep,"ess_datasim","modbus","lib"))

#Import Libraries
from core import utils
from core import modbus_server

#Main function for server deployment
class DataSimStartServer:

    #=============================================================================================
    #   Class Name     :    DataSimStartServer  
    #   Description    :    This class does the followng:
    #                           1.  Runs the async helper function
    #                           2.  The aysnc helper function contains start async server function
    #                           3.  Intializes variables used for start async server function
    #                           4.  Runs the async helper function as a co routine.
    #=============================================================================================

    def __init__(self,**kwargs):

        #Extract keyword args
        self.str_server_port            =   kwargs.get('str_server_port')
        self.str_server_unit_id         =   kwargs.get('str_server_unit_id')
        self.str_data_sample_duration   =   kwargs.get('str_data_sample_duration')
        self.str_asset_type             =   kwargs.get('str_asset_type')
        self.float_publish_interval     =   kwargs.get('float_publish_interval')

        #Intialize classes
        self.obj_utils              =   utils.DataSimUtils()
        self.obj_modbus_server      =   modbus_server.DataSimModbus()
    
        #Initialize attributes
        self.obj_logger             =   self.obj_utils.set_logger(str_log_filename  =   utils.STR_DEFAULT_MODBUS_SERVER_LOG_FILENAME)

        #Getting ip address
        self.str_server_ip_address  =   self.obj_utils.get_ip_address(obj_logger    =   self.obj_logger)
        
        #Log the port 
        self.obj_logger.info(f"Port          :  { self.str_server_port}")
        
        #Log the unit id 
        self.obj_logger.info(f"Unit ID       :  {self.str_server_unit_id}")
        
        #Path operations
        self.str_lib_path           =   self.obj_utils.get_lib_path(
                                                                        obj_logger      =   self.obj_logger
                                                                    )
        self.str_log_path           =   self.obj_utils.get_log_path(    
                                                                        str_lib_path    =   self.str_lib_path,
                                                                        obj_logger      =   self.obj_logger
                                                                    )
        self.str_config_path        =   self.obj_utils.get_config_path  (
                                                                            str_lib_path    =   self.str_lib_path,
                                                                            obj_logger      =   self.obj_logger
                                                                        )

        #CSV operations 
        self.dict_server_data       =   self.obj_utils.get_server_tag_data  (
                                                                                str_filepath                =   utils.STR_DEFAULT_CONFIG_FILEPATH,
                                                                                str_asset_type              =   self.str_asset_type,
                                                                                str_data_sample_duration    =   self.str_data_sample_duration,
                                                                                obj_logger                  =   self.obj_logger                             
                                                                            )
        self.dict_server_tag_list   =   self.obj_utils.get_server_tag_list(
                                                                                str_filepath    =   utils.STR_DEFAULT_CONFIG_FILEPATH,
                                                                                str_asset_type  =   self.str_asset_type,
                                                                                obj_logger      =   self.obj_logger          
                                                                        )
        self.dict_add_csv           =   self.obj_utils.get_server_data_per_timestep(
                                                                                        dict_server_data        =   self.dict_server_data,
                                                                                        dict_server_tag_list    =   self.dict_server_tag_list,
                                                                                        obj_logger              =   self.obj_logger   
                                                                                )
        #Run the async modbus server function
        #Starting point of the async coroutine
        #Manages event loop and context of async functions
        utils.asyncio.run(self.async_helper(),debug=True) 

    async def async_helper(self):
        
        #=====================================================================================
        #   Function Name  :  async_helper
        #   Description    :  An async helper function that does the following:
        #                       1.  Uses await to pass the execution of an async coroutine
        #                       2.  Starts the async modbus server
        #=====================================================================================

        #Calling async server
        await self.obj_modbus_server.start_async_server   (  
                                                            dict_data               =   self.dict_add_csv,          
                                                            str_server_ip_address   =   self.str_server_ip_address,
                                                            str_server_port         =   self.str_server_port, 
                                                            str_server_unit_id      =   self.str_server_unit_id,
                                                            float_publish_interval  =   self.float_publish_interval,
                                                            obj_logger              =   self.obj_logger
                                                        )