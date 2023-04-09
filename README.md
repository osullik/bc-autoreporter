# bc-autoreporter

# ToDO

## Data Collection
- [X] Generate Dummy Dataset using ChatGPT @osullik
- [X] Upload Dummy Dataset to Git @osullik

## Infrastructure
- [X] Establish Elasticsearch Instance on AWS
- [X] Figure out how to push data into Elastic Instance on AWS
- [X] Establish Kibana Instance that interacts with Elastic on AWS

## Parser
- [X] Build Test Harness
- [ ] Build Framework for Input Parser (Single message --> JSON document)
  - [X] Build Entity Extractor
  - [X] Build Date Extractor
  - [X] Build Tag Extractor
  - [X] Build Sentiment Analyzer @nicole
  
## Router
- [ ] Build Service to Push JSON Document to Elasticsearch

## Dashboards:
- [X] Build Supervisor Dashboard in Kibana
- [X] Build Employee Dashboard in Kibana
- [X] Build Report Summarizer

## Input management (Extension)
- [ ] Build Message Handler

## Clean Up and Present
- [ ] Clean up Git Repo
- [ ] Choose 3 submission categories
- [ ] Submit to Devpost by 0930
- [ ] Prep demo by 1030
  
  
<p align="center">
  <img src="https://github.com/osullik/bc-autoreporter/blob/main/images/greenWatcherMarshie.svg" width="150" >
  <img src="https://github.com/osullik/bc-autoreporter/blob/main/images/redRiderMarshie.svg" width="175">
  <img src="https://github.com/osullik/bc-autoreporter/blob/main/images/blueHikerMarshie.svg" width="150">
</p>

# Bugs
- Some dates are being marked as adjectives from the raw text processing
