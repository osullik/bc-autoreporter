# bc-autoreporter

# ToDO

## Data Collection
- [X] Generate Dummy Dataset using ChatGPT @osullik
- [X] Upload Dummy Dataset to Git @osullik

## Infrastructure
- [ ] Establish Elasticsearch Instance on AWS
- [ ] Figure out how to push data into Elastic Instance on AWS
- [ ] Establish Kibana Instance that interacts with Elastic on AWS

## Parser
- [ ] Build Test Harness
- [ ] Build Framework for Input Parser (Single message --> JSON document)
  - [ ] Build Entity Extractor
  - [ ] Build Date Extractor
  - [ ] Build Tag Extractor
  - [ ] Build Sentiment Analyzer
  
## Router
- [ ] Build Service to Push JSON Document to Elasticsearch

## Dashboards:
- [ ] Build Supervisor Dashboard in Kibana
- [ ] Build Employee Dashboard in Kibana
- [ ] Build Report Summarizer

## Input management (Extension)
- [ ] Build Message Handler
  
  

<p align="center">
  <img src="https://github.com/osullik/bc-autoreporter/blob/main/green%20watcher%20marshie.svg" width="150" >
  <img src="https://github.com/osullik/bc-autoreporter/blob/main/red%20rider%20marshie.svg" width="175">
  <img src="https://github.com/osullik/bc-autoreporter/blob/main/blue%20hiker%20marshie.svg" width="150">
</p>
