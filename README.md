# bc-autoreporter
Project description here

# Report Summarization
Text summarization comes in 2 forms: *Exctractive* and *Abstractive*. Extractive summarization involves selecting a few key sentences or phrases from a long text, to produce a shorter summary, while leaving the rest of the information out. **Abstractive summarization** involves synthesizing a summary similar to an abstract, constructed of different sentences or phrases than appear in the long text being summarized. This method often involves combining dsentences that have redundant information, and skipping details that aren't key to the overall message of the text. For this project, we perform Abstractive Summarization on synthetically generated Employee Performance Reports, as part of a tool that is aimed at helping companies, supervisors, and their employees understand key performance metrics at a glance.

The [Kibana Dashboard 'Report Summaries'](https://search-bc23-autoreporter-4ob7m4onu2evrdqghxxcfoo6cu.us-east-1.es.amazonaws.com/_dashboards/goto/0d7f056268de7146bdef4d8056dbbf8b?security_tenant=global)  were generated using a well-established Natural Language Processing [Text-to-Text Transformer model, T5](https://huggingface.co/docs/transformers/model_doc/t5), that was trained on common crawl data. The summaries are generated via the pre-trained T5 model, which we modified to operate on nested batches of report data, allowing us to summarize reports chronilogically, based on when they were generated.

The model condenses the entire collection of reports for each employee into a few key takeaways about his or her performance. The original reports are stored in the database and can be accessed to verify the content of the summaries for accuracy at the time of each employee's evaluation.

<p align="center">
  <img src="https://mohitmayank.com/a_lazy_data_science_guide/imgs/nlp_transformers.png" width="300">
   <img src="https://github.com/osullik/bc-autoreporter/blob/main/images/summarization_diagram.png" width="300">
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
