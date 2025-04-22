#=========================================================================================
#   Name        :   modbus_server.py
#   Date        :   4/10/2023
#   Version     :   1.0
#   Author      :   Shayan Sharif Zahid
#   Description :   This is a modbus_server module which does the following:
#                       1.  Defines DataSimModbus class
#                       2.  This class does the following:
#                               a.  Initializes server context 
#                               b.  Intializes server identity 
#                               c.  Intializes server store 
#                       3.  Update server data each timestep
#                       4.  Start the async server 
#                       5.  Create async task to update the values
#=========================================================================================

#Set path to current directory
import sys
import os
sys.path.append(os.path.join(os.sep,"ess_datasim","modbus","lib"))

#Import libraries
from core import utils
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server import StartAsyncTcpServer

#Class definitions
class DataSimModbus:
    
    #==========================================================================================
    # Class Name     :  DataSimModbus  
    # Description    :  This class is intializing classes,packages and defining async functions
    #==========================================================================================
    
    def __init__(self):

        #initialization of classes and packages
        self.obj_utils                   =   utils.DataSimUtils()
        self.store                       =   ModbusSlaveContext()
        self.context                     =   ModbusServerContext(
                                                                    slaves  =   self.store, 
                                                                    single  =   True
                                                                )
        
        #Define the server identity
        self.identity                    =  ModbusDeviceIdentification()
        self.identity.VendorName         =  "MODBUS"
        self.identity.ProductCode        =  "DV"
        self.identity.VendorUrl          =  "https://www.modbus.org/"
        self.identity.ProductName        =  "Modbus Server"
        self.identity.ModelName          =  "Modbus Server"
        self.identity.MajorMinorRevision =  "1.0"

    async def update_server_data(self,**kwargs):
        
        #=====================================================================================
        # Function Name  :  update_server_data 
        # Description    :  This function is publishing modbus register values:
        #                       1.  By updating the context in an async for loop 
        #=====================================================================================

        #Extract keyword args
        dict_data               =   kwargs.get('dict_data',None)
        float_publish_interval  =   kwargs.get('float_publish_interval', None)
        obj_logger              =   kwargs.get('obj_logger', None)

        while True:
            
            #Async function 
            async for result in self.obj_utils.cyclic_value_generator(dict_server_data=dict_data,float_publish_interval=float_publish_interval):
                
                for int_reg_address,list_reg_value in result.items():
                    
                    #Print/Log message
                    obj_logger.info(f"Publishing Modbus Register : {int_reg_address}:{list_reg_value}")
                    #print(f"Publishing Modbus Register : {int_reg_address}:{list_reg_value}")

                    #Setting context for register
                    self.context[utils.DEFAULT_HOLDING_REG_FUNCTION_CODE_HEX].setValues(utils.DEFAULT_HOLDING_REG_FUNCTION_CODE_HEX,int_reg_address,list_reg_value)
                    
    async def start_async_server(self,**kwargs):

        #=====================================================================================
        # Function Name  :  start_async_server 
        # Description    :  This function is creating tasks for modbus server
        #                   It is also starting the async TCP server
        #=====================================================================================
        
        #Extract keyword args
        dict_data               =   kwargs.get('dict_data',None)
        str_server_ip_address   =   kwargs.get('str_server_ip_address',None)
        str_server_unit_id      =   kwargs.get('str_server_unit_id',None)
        str_server_port         =   kwargs.get('str_server_port',None)
        float_publish_interval  =   kwargs.get('float_publish_interval', None)
        obj_logger              =   kwargs.get('obj_logger', None)
        
        #Print/Log message
        print("Server Status       :   Started\n\n*Check logs for more information")

        #Creating task
        utils.asyncio.create_task(self.update_server_data   (
                                                                dict_data               =   dict_data,
                                                                float_publish_interval  =   float_publish_interval,
                                                                obj_logger              =   obj_logger
                                                            )
                            )
        
        #Start the Modbus server
        await StartAsyncTcpServer   (  
                                        context     =   self.context, 
                                        identity    =   self.identity, 
                                        address     =   (   
                                                            str_server_ip_address,
                                                            str_server_port,
                                                            str_server_unit_id
                                                        )
                                    )