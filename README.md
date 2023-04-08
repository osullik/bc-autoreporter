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
  
