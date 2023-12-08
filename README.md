# General Architecture
![image](https://github.com/minhsyqt/rural-argriculture/assets/144056454/6f612d11-1293-4cd9-ab8a-7ec5d8baf518)

# General Philosophy
1. All internal microservices will communicate via `RPyC` with `JSON` payloads
2. External clients will communicate to the server via `RestAPI`
3. ~~Authentication will be handled by `OAuth2` or `OpenID Connect`~~
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
## Milestone #3
- [Milestone #3 Report](https://docs.google.com/document/d/1X4m1yLyAz9bY7qhe4nBwFgAVOJqwSWByeHbyA0mzvcg)
- [Milestone #3 Experimentation data](https://docs.google.com/spreadsheets/d/1f3lCPKhNsXz3EuZfNJqDziHZVB7Pfj-URd2D-FAIYR0)
- [Milestone #3 Presentation](https://docs.google.com/presentation/d/1JqgZ5gK7qWkhFCmMyeXYcZees6PPdlMuVDN7bgjF_j0)

# Example Start Command
terminal 1: `$ python3 weather-service.py`

terminal 2: `$ python3 mongoAPI-service.py`

main terminal: `$ python3 main-service.py`

**please import the `JSON` file in `/data/World.Farmers.json` as `World.Farmers` in `MongoDB`. 
