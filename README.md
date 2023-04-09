# bc-autoreporter
Project description here

# Report Summarization
  <img src="https://github.com/osullik/bc-autoreporter/blob/main/images/summarization_diagram.png">

The Kibana Dashboard 'Report Summaries' were generated using a well-established Natural Language Processing Text-to-Text Transformer model, T5, that was trained on common crawl data. The summaries are generated via the pre-trained T5 model, which performs Abstractive Summarization, condensing the entire collection of reports for each employee into a few key takeaways about his or her performance. The original reports are stored in the database and can be accessed to verify the content of the summaries for accuracy at the time of each employee's evaluation.

<p align="center">
  <img src="https://mohitmayank.com/a_lazy_data_science_guide/imgs/nlp_transformers.png" width="300">
</p>

# Report Sentiment Analysis
Info here
___

# Project Development Plan

### Data Collection
- [X] Generate Dummy Dataset using ChatGPT @osullik
- [X] Upload Dummy Dataset to Git @osullik

### Infrastructure
- [X] Establish Elasticsearch Instance on AWS @osullik
- [X] Figure out how to push data into Elastic Instance on AWS @osullik
- [X] Establish Kibana Instance that interacts with Elastic on AWS @osullik

### Parser
- [X] Build Test Harness @osullik
- [ ] Build Framework for Input Parser (Single message --> JSON document)
  - [X] Build Entity Extractor @osullik
  - [X] Build Date Extractor @osullik
  - [X] Build Tag Extractor @osullik
  - [X] Build Sentiment Analyzer @nicoleschneider
  
### Router
- [ ] Build Service to Push JSON Document to Elasticsearch @osullik

### Dashboards:
- [X] Build Supervisor Dashboard in Kibana @nicoleschneider
- [X] Build Employee Dashboard in Kibana @nicoleschneider
- [X] Build Report Summarizer @nicoleschneider

### Input management (Extension)
- [ ] Build Message Handler

### Finalize Documentation/Artifacts and Present
- [ ] Clean up Git Repo
- [ ] Choose 3 submission categories
- [ ] Submit to Devpost by 0930
- [ ] Prep demo by 1030
  
  
<p align="center">
  <img src="https://github.com/osullik/bc-autoreporter/blob/main/images/greenHikerMarshie.svg" width="150" >
  <img src="https://github.com/osullik/bc-autoreporter/blob/main/images/redHikerMarshie.svg" width="175">
  <img src="https://github.com/osullik/bc-autoreporter/blob/main/images/blueHikerMarshie.svg" width="150">
</p>
