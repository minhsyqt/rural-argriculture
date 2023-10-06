# General Architecture
![image](https://github.com/minhsyqt/rural-argriculture/assets/144056454/4bebf90a-770a-4aab-941e-f2894b3d1e8c)

# General Philosophy
1. All internal microservices will communicate via `gRPC` with `JSON` payloads
2. External clients will communicate to the server via `RestAPI`
3. Authentication will be handled by `OAuth2` or `OpenID Connect`
4. Users will primarily be categorized by area, utilizing `MongoDB`'s `Geo-Spatial index` feature

# Build
Before building, please build dependencies by running `python[3] -m pip install -r requirements.txt`

# Resources
[Test Bench](https://www.cloudlab.us/show-project.php?project=RuralAgriculture)

# Example Start Command
terminal 1: `$ python3 ./server.py --host localhost --port 6789`

terminal 2: `$ python3 ./client.py --host localhost --port 6789`
