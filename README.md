# Mr. FAT (Management Reporting and Feedback Analysis Tool)
A tool to improve the feedback and report-generation process and empower people in any position of the management chain, including employees and employers, to view feedback trends over time and across several performance indicators. We accompished this by creating an end-to-end pipeline that gives structure to unstructured data and provides a modular framework, making it easy to adapt cutting edge data analysis and Natural Language Processing techniques to streamline the feedback process.

## Project Motivation
Employees often ask for (and managers seek to provide) feedback **"early and often"**. The reality of a hectic work environment means that this goal is rarely met well enough to give employees sufficient clarity about their job performance.

Both of the members of our team have been fortunate enough to work in management over the last few years. One of the most stressful times of year for supervisors and their direct reports is annual performance review time. Even those rare managers who have been diligent note-takers need to find their notes, compile them and communicate with the users. The feedback loop is too slow and too much information is lost for meaningful improvements to me made, even when everyone commits that "it will be different this year". 

Out project explores an approach to performance appraisal that is participative, transparent and almost instantaneous, all without having to fill out annoying forms or send emails back and forth.

# Primary Artifacts
- [Kibana 'Employee Deep Dive' Dashboard](https://search-bc23-autoreporter-4ob7m4onu2evrdqghxxcfoo6cu.us-east-1.es.amazonaws.com/_dashboards/goto/628493dcf3de2f1907a480f504bac7c8?security_tenant=global) 
-      USERNAME: user, PASSWORD: Bitcamp1!
- [Static version](https://github.com/osullik/bc-autoreporter/blob/main/KibanaDeepDive.pdf)
- [Kibana 'Report Summaries' Dashboard](https://search-bc23-autoreporter-4ob7m4onu2evrdqghxxcfoo6cu.us-east-1.es.amazonaws.com/_dashboards/goto/0d7f056268de7146bdef4d8056dbbf8b?security_tenant=global)
-      USERNAME: user, PASSWORD: Bitcamp1!
- [Static version](https://github.com/osullik/bc-autoreporter/blob/main/KibanaSummaries.pdf)
- A system that leverages the way that we like to communicate to facilitate making feedback more transparent.

## Technologies, Tools, and APIs Used
- Kibana
- AWS Elastic OpenSearch
- Twillio
- Python
- NLP libraries: Hugging Face, NLTK, PyTorch
- Chat-GPT

# System Design
Mr. FAT is discretized into four components. 
1. The Collection subystem.
2. The Parsing subsystem.
3. The Storage subsystem
4. The Reporting system. 

## The Collection System
The collection system aims to minimize the technical impediment to entry. The user interface requires no additional applications or web accesses to push observations into the system. We leverage [Twilio](twilio.com/)

## The Parsing System

## The Storage System

## The Reporting System

# Generating Synthetic Report Data
As we didn't have access to real performance appraisal material we elected to generate some using chatGPT. As a motivating use case, we used the setting of the Nuclear Power Plant from 'the simpsons' to give the model extra context to draw on. The model was given variants on the following prompt to generate lists in the language of performance appraisal notes:
  
    Pretend you are Mr Burns from the TV show 'The Simpsons'. In 2021 you observed Homer Simpson's work and kept a log of his performance. What are 10 entries from that log? Each entry should be of the form:

    On <date> @name was observed to perform to a <poor / satisfactory / good / very good / excellent> standard. This was evidenced by  <summary of action>. Their actions show <list attributes here that match the action, each prepended with a #>

    For each summary of action in the log, fabricate some specific examples, using other characters or locations from around the nuclear power plant in the show 'the simpsons'

Small corrections, modifications and specific event prompts were made to generate approximately 210 observations across 10 Nuclear Power Plant Employees. 
  
See [Chat-GPT](https://openai.com/blog/chatgpt) for more

# Parsing
Structured data is more useful than unstructured. It is typically also more laborious to produce and a deterrent to on-the-fly note takin. Our approach considered user ergonomics, and the knowledge that anything we can do to reduce the difficulty of use will increase likelihood of adoption. Guided by the realization that the use of very informally structured language utilizing symbols like '@' for entities and  '#' for themes we design our approach to embrace their use, rather than try to pull users towards a less natural approach. 

Our parsing approach aims to maximise the amount of infomation extracted from the logs themselves, as well as expose managers and employees to meta aspects like the sentiment of language used by individuals, changes in performance over time and themes that might cut across entire sectors of the workforce. Bringing together this information without drowning anyone in it is a key step towards an improved performance appraisal system. 

# Report Summarization
Text summarization comes in 2 forms: *Exctractive* and *Abstractive*. Extractive summarization involves selecting a few key sentences or phrases from a long text, to produce a shorter summary, while leaving the rest of the information out. **Abstractive summarization** involves synthesizing a summary similar to an abstract, constructed of different sentences or phrases than appear in the long text being summarized. This method often involves combining dsentences that have redundant information, and skipping details that aren't key to the overall message of the text. For this project, we perform Abstractive Summarization on synthetically generated Employee Performance Reports, as part of a tool that is aimed at helping companies, supervisors, and their employees understand key performance metrics at a glance.

The [Kibana Dashboard 'Report Summaries'](https://search-bc23-autoreporter-4ob7m4onu2evrdqghxxcfoo6cu.us-east-1.es.amazonaws.com/_dashboards/goto/0d7f056268de7146bdef4d8056dbbf8b?security_tenant=global)  were generated using a well-established Natural Language Processing [Text-to-Text Transformer model, T5](https://huggingface.co/docs/transformers/model_doc/t5), that was trained on common crawl data. The summaries are generated via the pre-trained T5 model, which we modified to operate on nested batches of report data, allowing us to summarize reports chronilogically, based on when they were generated.

The model condenses the entire collection of reports for each employee into a few key takeaways about his or her performance. The original reports are stored in the database and can be accessed to verify the content of the summaries for accuracy at the time of each employee's evaluation.

<p align="center">
  <img src="https://mohitmayank.com/a_lazy_data_science_guide/imgs/nlp_transformers.png" width="300">
   <img src="https://github.com/osullik/bc-autoreporter/blob/main/images/summarization_diagram.png" width="300">
</p>

# Report Sentiment Analysis
To further aid in understanding trends across reports, we used Python's [Natural Language Tool Kit NLTK](https://www.nltk.org/) to perform Part of Speech (POS) Tagging and Sentiment Analysis on the content of the reports. Linguistically, adjectives and adverbs are typically most indicative of the sentiment of a piece of text, so we exctracted those words from the reports and flagged them, creating an additional field in the ElasticSearch schema to allow for further analysis of sentiment trends via the Kibana dashboards. We also used [VADER (Valence Aware Dictionary and sEntiment Reasoner)](https://github.com/cjhutto/vaderSentiment),  an open-source lexicon and rule-based sentiment analysis tool, to compute overall sentiment scores for each report entered in the database.
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
- [X] Build Framework for Input Parser (Single message --> JSON document)
  - [X] Build Entity Extractor @osullik
  - [X] Build Date Extractor @osullik
  - [X] Build Tag Extractor @osullik
  - [X] Build Sentiment Analyzer @nicoleschneider
  
### Router
- [X] Build Service to Push JSON Document to Elasticsearch @osullik

### Dashboards:
- [X] Build Supervisor Dashboard in Kibana @nicoleschneider
- [X] Build Employee Dashboard in Kibana @nicoleschneider
- [X] Build Report Summarizer @nicoleschneider

### Input management (Extension)
- [X] Build Message Handler (Twilio)

### Finalize Documentation/Artifacts and Present
- [X] Submit to Devpost by 0930
- [X] Prep demo by 1030
  
  
<p align="center">
  <img src="https://github.com/osullik/bc-autoreporter/blob/main/images/greenHikerMarshie.svg" width="150" >
  <img src="https://github.com/osullik/bc-autoreporter/blob/main/images/redHikerMarshie.svg" width="175">
  <img src="https://github.com/osullik/bc-autoreporter/blob/main/images/blueHikerMarshie.svg" width="150">
</p>
