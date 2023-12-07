import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer,pipeline
import torch
model = AutoModelForSequenceClassification.from_pretrained('NLP-LTU/bertweet-large-sexism-detector')
tokenizer = AutoTokenizer.from_pretrained('NLP-LTU/bertweet-large-sexism-detector') 
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

# for timing
from tqdm import tqdm

df = pd.read_csv('data/forum/general-climbing-final.csv')

tqdm.pandas()

def detect_sexism(body):
    try:
        prediction = classifier(body)[0]
    except:
        prediction = None
    return prediction

sexism = df.body.sample(1000).progress_apply(lambda x: detect_sexism(x))

sexism.to_csv('data/forum/sexism.csv')