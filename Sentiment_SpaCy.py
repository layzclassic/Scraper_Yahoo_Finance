import os.path

import spacy
import textacy
from spacy import displacy
import pandas as pd
from spacy.lang.en import English
from spacy.pipeline import EntityRuler
import json
import re
from spacytextblob.spacytextblob import SpacyTextBlob

# Training_data = [(text, {'entities': [(start, end, label)]})]

# lg for accuracy
nlp = spacy.load("en_core_web_sm")

def main(ticker_list, file, path):
    # load index list
    df = load_tsv(ticker_list)
    # create trainer
    find_tickers(df)
    # load text
    data = load_text(file, path)
    # process with spacy
    doc = load_doc(data)
    # data visualization with DisplaCy
    visual_doc(doc, file)
    # save data to csv
    #save_csv(data)
    print('complete')


def load_text(file, path):
    with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
        text = f.read()
    return text


def save_file(file_name, file_type, path, data):
    # change format
    file_name = file_name.strip().split(".")[0] + file_type
    try:
        with open(os.path.join(path, file_name), 'w', encoding="utf-8") as f:
            f.write(data)
        print('file saved: ', path, ' - ', file_name)
    except Exception as e:
        print('file saved: ', file_name, ' - ', e)


def load_doc(text):
    doc = nlp(text)
    return doc


def load_tsv(ticker_list):
    df = pd.read_csv(ticker_list, sep='\t')
    return df


def save_csv(data, file_name):
    output_df = pd.DataFrame(data, index=True)
    try:
        output_df.to_csv(os.path.join(path, file_name))
        print('saved to {}'.format(path))
    except Exception as e:
        print('saving file failed: ', e)

def find_tickers(df):
    patterns = []
    patterns_config = {'overwrite_ents': 'true'}
    letters = '[A-Z]'
    symbols = df.Symbol.tolist()
    # companies = df.CompanyName.tolist()

    # list of entities and patterns
    for symbol in symbols:
        patterns.append({'label': 'STOCK', 'pattern': symbol})
        # for letter in letters:
        #     patterns.append({'label': 'STOCK', 'pattern': symbol + f".{letter}"})
    # for company in companies:
    #     patterns.append({'label': 'COMPANY', 'pattern': company})

    # create entity ruler
    ruler = nlp.add_pipe('entity_ruler', before='ner')
    #EntityRuler(nlp, config=patterns_config)
    ruler.add_patterns(patterns)


# for sentence in sentences:
#     # look for name entities
#     ents = list(sentence.ents)
#     ents_data = (ents[0].label, ents[0].label_, ents[0].text)

# for ent in ents:
#     if ent.label_ == 'PERSON':
#         people.append(ent)
#
# for token in sentences:
#     if token.pos_ == 'NOUN':
#         nouns.append(token)

# chunks = list(doc.noun_chunks)
# for chunk in chunks:
#     if '$wish' or '$WISH' in str(chunk):
#         print(chunk)

# patterns = [{'POS': 'NOUN'},{'POS': 'VERB'}, {'POS': 'ADV'}]
# verb_phrases = textacy.extract.matches.token_matches(doc, patterns=patterns)
#
# for verb_phrase in verb_phrases:
#     print(verb_phrase, verb_phrase.lemma_)

#def get_price(text):


def visual_doc(doc, file):
    # change HEX colors
    colors = {'Wish': '#66abff', 'buy': '#66ff78', 'sell': '#FF5733'}
    #options = {'ents': ['Wish', 'buy', 'sell'], 'colors':colors}
    html = displacy.render(doc, style='ent') #, options=options
    file_type = '.html'
    file_name = file
    save_file(file_name, file_type, path, html)


if __name__ == '__main__':
    file = 'Bullish_text_sample.txt'
    ticker_list = 'data/stocks.tsv'
    path = r'C:\Users\suen6\PycharmProjects\Scraper_Yahoo_Finance\data'
    main(ticker_list, file, path)
