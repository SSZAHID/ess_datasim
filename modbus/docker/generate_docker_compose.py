#============================================================================================
#   Name        :   generate_docker_compose.py
#   Date        :   4/10/2023
#   Version     :   1.0
#   Author      :   Shayan Sharif Zahid
#   Description :   This module does the following:
#                  
#============================================================================================

#Set path to current directory
import sys
import os
sys.path.append(os.path.join(os.sep,"ess_datasim","modbus","lib"))

#Import libraries
import pandas as pd
import yaml
import psutil
import subprocess
import socket

#Default values
STR_DEFAULT_NETWORK_NAME            =   "ess_datasim_network"
STR_DEFAULT_DRIVER_TYPE             =   "ipvlan"
STR_DEFAULT_PARENT_ETH              =   "enp2s0"
STR_DEFAULT_SUBNET                  =   "10.0.0.0/24"
STR_DEFAULT_GATEWAY                 =   "10.0.0.2"
STR_DEFAULT_DOCKER_COMPOSE_FILENAME =   "docker_compose"


# Read the CSV file and generate docker-compose.yml
def generate_docker_compose(**kwargs):

    #Print message
    print(f"\n{'='*24}\n{' '*8}Generate\n{' '*5}Docker Compose\n{'='*24}")

    #Config filename for docker compose
    str_config_filename         =       kwargs.get('str_docker_compose_config_filename', None)
   
    #Print the current file path
    str_current_working_dir     =   os.path.dirname(os.path.abspath(__file__))
    print(f"\nCurrent Directory : {str_current_working_dir}")

    #Create full path to CSV file
    csv_data_file_path          =     os.path.join(os.sep,str_current_working_dir,str_config_filename+".csv")
    
    #Read the CSV file into a DataFrame
    df_services                 =      pd.read_csv(csv_data_file_path)

    #Group dataframe according to servers
    df_grouped_servers          =      df_services.groupby("server_name")

    for server_name,server_group in df_grouped_servers:


        #Define the docker-compose data structure
        docker_compose              =   {
                                            "networks": {
                                                STR_DEFAULT_NETWORK_NAME: {
                                                    "driver": STR_DEFAULT_DRIVER_TYPE,
                                                    "driver_opts": {
                                                        "parent": STR_DEFAULT_PARENT_ETH
                                                    },
                                                    "ipam": {
                                                        "config": [
                                                            {"subnet": STR_DEFAULT_SUBNET, "gateway": STR_DEFAULT_GATEWAY}
                                                        ]
                                                    }
                                                }
                                            },
                                            "services": {}
                                        }
        
        #Populate services section
        for _,row in server_group.iterrows():
            
            service                 =   row.to_dict()
            list_services           =   []
            list_services.append(service)

            for service in list_services:

                docker_compose["services"][str(service["service_name"])] = {
                    "build": {
                        "context": "./",
                        "dockerfile": str(service["dockerfile"])
                    },
                    "container_name": str(service["container_name"]),
                    "networks": {
                        STR_DEFAULT_NETWORK_NAME: {
                            "ipv4_address": service["ipv4_address"]
                        }
                    },
                    "ports": [
                        "502:502"
                    ],
                    "restart": "always",
                    "deploy": {
                    "resources": {
                        "limits": {
                            "cpus": str(service["limits_cpus"]),
                            "memory": str(service["limits_memory"]),
                        },
                        "reservations": {
                            "cpus": str(service["reservations_cpus"]),
                            "memory": str(service["reservations_memory"]),
                        }
                    }
                },
                "mem_limit": str(service["mem_limit"]),
                "memswap_limit": str(service["memswap_limit"])
                }

        #Print Message
        print(f"Config Status     : YAML Generated")

        #Convert to YAML format and write to docker-compose.yml
        str_modbus_path = str_current_working_dir.replace(os.path.join("modbus", "docker"),"")
        str_docker_compose_filepath = os.path.join(str_modbus_path,server_name+'_'+STR_DEFAULT_DOCKER_COMPOSE_FILENAME+".yml")

        #Write values to the yaml file
        with open(str_docker_compose_filepath, 'w') as yaml_file:
            
            yaml.dump(docker_compose, yaml_file, default_flow_style=False)

        #Print Message
        print(f"File Generated    : {str_docker_compose_filepath}\n")

#Main entry point when script is run directly
if __name__ == '__main__':
    
    # Call the function to generate the docker-compose.yml
    generate_docker_compose(str_docker_compose_config_filename="docker_compose_config")