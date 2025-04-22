#=========================================================================================
#   Name        :   start.py
#   Date        :   4/10/2023
#   Version     :   1.0
#   Author      :   Shayan Sharif Zahid
#   Description :   This module does the following:
#                   1.  Gets inputs using argument parser:
#                       a.  str_server_type
#                       b.  str_server_port
#                       c.  str_server_unit_id
#                   2.  Select and start the required data simulator:
#                       a.  mobdus
#=========================================================================================

#Set path to current directory
import sys
import os
sys.path.append(os.path.join(os.sep,"ess_datasim","modbus","lib"))

#Import libraries
from core import utils 
from server import modbus_simulator 
import generate_test_data

#Initialize argument parser
parser = utils.argparse.ArgumentParser(description='Arguments for Starting Data Simulator')

#Define command line arguments
parser.add_argument(
                        '--type',
                        type    =   str,
                        help    =   'Enter the type of server you want to deploy: modbus',
                        default =   'modbus'
                    )
parser.add_argument(
                        '--port',
                        type    =   str,
                        help    =   'Enter the server Port',
                        default =   '502'
                    )
parser.add_argument(
                        '--unit_id',
                        type    =   str,
                        help    =   'Enter the server Unit ID',
                        default =    '1'
                    )
parser.add_argument(
                        '--sample_duration',
                        type    =   str,
                        help    =   'Enter the time duration for data simulation',
                        default =    '1T'
                    )
parser.add_argument(
                        '--asset',
                        type    =   str,
                        help    =   'Enter the asset type that you want to simulate modbus data for',
                        default =    utils.STR_DEFAULT_ASSET_TYPE
                    )
parser.add_argument(
                        '--pub_int',
                        type    =   float,
                        help    =   'Enter the publish interval of data',
                        default =    utils.FLOAT_DEFAULT_PUBLISH_INTERVAL
                    )

#Parse command line arguments
args                        =   parser.parse_args()
str_type                    =   args.type
str_port                    =   args.port
str_unit_id                 =   args.unit_id
str_sample_duration         =   args.sample_duration
str_asset_type              =   args.asset
float_publish_interval      =   args.pub_int

#Main entry point when script is run directly
if __name__ == '__main__':

    #If server type is modbus
    if str_type  ==  'modbus':

        #Generate the latest test data before the start of the program
        generate_test_data.generate()

        #Log/print message
        print(f"\n{'='*30}\n{' '*4}Modbus Server Simulator\n{' '*10}Starting\n{'='*30}")

        #Start modbus server with specified port and unit id
        modbus_simulator.DataSimStartServer (
                                                str_server_port             =   str_port,
                                                str_server_unit_id          =   str_unit_id,
                                                str_data_sample_duration    =   str_sample_duration,
                                                str_asset_type              =   str_asset_type,
                                                float_publish_interval      =   float_publish_interval,
                                            )
    
    else:
        
        #Raise an error if server type is not recognized
        raise Exception(f"Unrecognized Server Type: {str_type}")
