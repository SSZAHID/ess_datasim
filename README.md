# ESS Data Simulator (ESS DS)

The **ESS DS (ESS Data Simulator)** is a Modbus communication simulator designed to support dev teams in building HMI screens, implementing control logic, and developing robust data pipelines.

It acts as a testbed where you can simulate hardware Modbus specs and create a testing environment tailored for your system. It supports running Docker containers for each type of hardware asset (e.g., BMS, CNV, INV), and it’s easy to extend with additional devices.

---

## Key Benefits for Your Team

### SCADA
1. Read registers as tags during HMI screen development
2. Send variable data to HMI screens to test responsiveness
3. Provide dynamic, real-time data for HMI screen demos

### Controls
4. Inject hardware-specific data from CSVs to validate control logic
5. Simulate communication failures for fault-tolerant logic testing
6. Test scaling, data types, and register offsets from Modbus specs

### Data Engineering
7. Simulate large-scale data ingest (500k+ tags) by spinning up multiple containers
8. Analyze ETL pipeline behavior during communication failures
9. Ingest and test with regularly changing dynamic data
10. Benchmark your ETL server's capacity based on tag throughput

---

## Usage Guide

### `generate_docker_compose.py`
- Generates a Docker Compose file using `docker_compose_config.csv`
- Define IPs, container names, and container limits in the CSV
- Re-run this script after updates to container definitions

---

### `start.py`
- Starts the simulator using auto-generated CSV data for each asset type (BMS, CNV, INV)
- Sends Modbus data on a 1s scan rate (default)
- Example:
  ```bash
  python start.py --asset bms
  python start.py --asset cnv
  python start.py --asset inv
