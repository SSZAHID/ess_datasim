# ESS Data Simulator (ESS DS)

The **ESS DS (ESS Data Simulator)** is a Modbus communication simulator designed to support dev teams in building HMI screens, testing control logic, and developing robust data pipelines.

It acts as a testbed where you can simulate various Modbus specs and create a testing environment tailored for your project. It supports running Docker containers for each type of hardware asset (e.g., BMS, CNV, INV), and it’s easy to extend with additional devices.

---

## Key Benefits for Your Team

### SCADA
1. Read registers as tags to support HMI screen development
2. Send variable data to HMI screens to test responsiveness
3. Provide dynamic, real-time data for HMI screen demos

### Controls
4. Inject hardware-specific data from CSVs to validate control logic
5. Simulate communication failures for fault-tolerant logic testing
6. Test scaling, data types, and register offsets from Modbus specs
7. Test/evaluate network usage calculations

### Data Engineering
8. Simulate large-scale data ingest (500k+ tags) by spinning up multiple containers
9. Analyze ETL pipeline behavior during communication failures
10. Test Redundancy of data systems
11. Ingest and test with regularly changing dynamic data
12. Benchmark your ETL server's capacity based on tag throughput

---

## Usage Guide

### `generate_docker_compose.py`
- Generates a Docker Compose file using `docker_compose_config.csv`
- Define IPs, container names, and container limits in the CSV
- Re-run this script after updates to container definitions

### `Start.py`
- This script is used to start the simulator
- This script uses auto generated csv data for each of the hardware asset(BMS/INV/CNV) 
- Runs the simulator by sending data on the defined scan rate. Currently it is set to 1s

### `Generate_test_data.py`
- This is where you should add your vendor specific Modbus specs
- This script takes in the registers that have been defined under modbus/config/ 
- Generates data for each register depending on the scaling, data type and offset
- This script also run’s itself at the start of the start.py function

---

## Simulator

### `start.py`
- Starts the simulator using auto-generated CSV data for each asset type (BMS, CNV, INV)
- Sends Modbus data on a 1s scan rate (default)
- Example:
  ```bash
  python start.py --asset bms
  python start.py --asset cnv
  python start.py --asset inv

- Defaults:
- Port 502 
- Unit ID 1 
- Type Modbus
- Sample Time 1s

---

## Configuration Example (BMS)
- Add your BMS Modbus device specs in modbus/config/csv/bms_tag_list.csv 
- Run generate_test_data.py script 
- Check if bms_tag_data_auto_gen.csv as generic test data
- Docker*: If running docker containers do add info to docker_compose_config.csv
- Docker*: Run generate_docker_compose.py script
- Docker*: This will generate docker_compose.yaml file that can be run using docker_compose
- Run the simulator



