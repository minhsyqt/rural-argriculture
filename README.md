# General Architecture
![image](https://github.com/minhsyqt/rural-argriculture/assets/144056454/4bebf90a-770a-4aab-941e-f2894b3d1e8c)

# General Philosophy
1. All internal microservices will communicate via `gRPC` with `JSON` payloads
2. External clients will communicate to the server via `RestAPI`
3. Authentication will be handled by `OAuth2` or `OpenID Connect`
4. Users will primarily be categorized by area, utilizing `MongoDB`'s `Geo-Spatial index` feature

# Build
Before building, please build dependencies by running `python[3] -m pip install -r requirements.txt`

# Resources/Documentation
- [Test Bench](https://www.cloudlab.us/show-project.php?project=RuralAgriculture)
## Milestone #1
- [Milestone #1 Report](https://docs.google.com/document/d/1wjhrvLpg4ZRF1eYcNlT4u3lYyz2DlXeMc4ajwJUy_14/)
- [Milestone #1 Feedback](https://docs.google.com/document/d/1Zn1Y8vQKZL6aYxjR3r8TT7Ak-GBUqXFzhp59A0WW-64)
## Milestone #2
- [Milestone #2 Report](https://docs.google.com/document/d/1AskeTW3eZOXggBxbe1c9Rf78I3EDYl_MfDlBFyTotpQ)
- [Milestone #2 Feedback](https://docs.google.com/document/d/1qatRfsuETGv1EzvSRAw9kt9VOA9RL5TETMGMgmqQmH4)

# Example Start Command
terminal 1: `$ python3 ./server.py --host localhost --port 6789`

terminal 2: `$ python3 ./client.py --host localhost --port 6789`
