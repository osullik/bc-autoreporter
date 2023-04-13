from transformers import T5Tokenizer, T5Config, T5ForConditionalGeneration
from transformers import BartTokenizer, BartForConditionalGeneration
import numpy as np
import torch
import random
import re
import nltk
#nltk.download('punkt')

class Summarizer():
	def __init__(self):

		self.device = torch.device("cpu")

		if torch.cuda.is_available():
		   print("Using GPU")
		   self.device = torch.device("cuda:0")

		# Instantiate the tokenizer 
		self.tokenizer = T5Tokenizer.from_pretrained('t5-small')
		##tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')


		# Instantiate the model 
		self.model = T5ForConditionalGeneration.from_pretrained('t5-small')
		##model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn').to(device)
     

	# generate chunks of text \ sentences <= 512 tokens
	def nest_sentences(self,document):
		nested = []
		sent = ["summarize"]  # need to provide task instruction as the first token
		length = 1
		for sentence in nltk.sent_tokenize(document):
			length += len(sentence)
			if length < 512:
				sent.append(sentence)
			else:
				nested.append(sent)
				sent = ["summarize"]  # need to provide task instruction as the first token
				length = 1

		if len(sent) > 1:
			nested.append(sent)
		
		return nested

	# generate summary on text with <= 512 tokens
	def generate_summary(self,sentences, tokenizer, model):
		input_tokenized = tokenizer.encode(sentences, truncation=True, return_tensors='pt')
		input_tokenized = input_tokenized.to(self.device)
		summary_ids = model.to(self.device).generate(input_tokenized,
												num_beams=4,
												min_length=50,
												max_length=1000,
												early_stopping=True)
		output = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids]
		return output

	def employee_summarize(self, list_of_dicts):
		employee_record = ''
		for _dict in list_of_dicts:
			employee_record = employee_record + _dict['observation'].replace("\n"," ")
    
		#self.tokenizer = T5Tokenizer.from_pretrained('t5-small')
		#model = T5ForConditionalGeneration.from_pretrained('t5-small')

		nested_text = self.nest_sentences(employee_record)

		employee_summary = []
		for i in range(len(nested_text)):
			inputs = []

			for j in nested_text[i]:
				inputs.append(j.split())

			inputs_squeezed = np.concatenate(inputs, axis=0 )
			inputs_squeezed = [j + ' ' for j in inputs_squeezed]
			employee_summary.append(self.generate_summary(' '.join(inputs_squeezed), self.tokenizer, self.model))
	
		sub_summaries = [''.join(ele) for ele in employee_summary]

		toClean = ''.join(sub_summaries)
		cleaned = re.sub("(\s)(.)(\s)",". ",toClean)	#now we have two problems...

		return cleaned
