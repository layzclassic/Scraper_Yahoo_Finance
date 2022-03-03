import os.path
import spacy
import textacy
from spacy import displacy
import pandas as pd
from spacy.pipeline import EntityRuler
from collections import Counter
from spacytextblob.spacytextblob import SpacyTextBlob

# Training_data = [(text, {'entities': [(start, end, label)]})]
# pip install spacy[transformers]

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
    visual_doc(doc)
    # save data to csv
    ent_count(doc)
    print('complete')


def load_text(file, path):
    with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
        text = f.read()
    return text


def remove_file_type(file_name):
    name = file_name.strip().split(".")[0]
    return name


def save_file(file, file_name, path, data):
    # change format
    outname = remove_file_type(file) + file_name
    try:
        with open(os.path.join(path, outname), 'w', encoding="utf-8") as f:
            f.write(data)
        print('file saved: ', path, ' - ', outname)
    except Exception as e:
        print('file saved: ', outname, ' - ', e)


def load_doc(text):
    doc = nlp(text)
    return doc


def load_tsv(ticker_list):
    df = pd.read_csv(ticker_list, sep='\t')
    return df


def save_csv(file, data, path, file_name):
    outname = remove_file_type(file) + '_' + file_name + '.csv'
    output_df = pd.DataFrame(data, index=None)
    try:
        output_df.to_csv(os.path.join(path, outname))
        print('csv saved to {} - '.format(path), outname)
    except Exception as e:
        print('saving csv file failed: ', e)


def find_tickers(df):
    patterns = [{"label": "BUY", "pattern": '(?i)buy'}, {"label": "SELL", "pattern": '(?i)sell'}, {"label": "STOCK", "pattern": '(?i)wish'}]
    letters = '[A-Z]'
    symbols = df.Symbol.tolist()
    companies = df.CompanyName.tolist()

    # list of entities and patterns
    for symbol in symbols:
        patterns.append({'label': 'STOCK', 'pattern': symbol})
        for letter in letters:
            patterns.append({'label': 'STOCK', 'pattern': symbol + f".{letter}"})
    for company in companies:
        patterns.append({'label': 'COMPANY', 'pattern': company})

    # Construction via add_pipe
    # config = {"phrase_matcher_attr": "LOWER", 'overwrite_ents': 'true'}
    ruler = nlp.add_pipe('entity_ruler', config={'overwrite_ents': 'true'}, before='ner')  # add config
    # Construction from class
    # entity_ruler = nlp.add_pipe("entity_ruler", after='parser')
    # entity_ruler.initialize(lambda: [], nlp=nlp, patterns=patterns)

    ruler.add_patterns(patterns)


def ent_count(doc):
    money = []
    stock = []
    final_list = []

    for ent in doc.ents:
        if ent.label_ == 'MONEY':
            money.append(str(ent))
        elif ent.label_ == "STOCK":
            stock.append(str(ent))

    cm = Counter(money)
    for p, count in cm.most_common():
        final_list.append({
            'name': p,
            'type': 'MONEY',
            'frequency': count
        })

    cs = Counter(stock)
    for l, count in cs.most_common():
        final_list.append({
            'name': l,
            'type': 'STOCK',
            'frequency': count
        })
    file_name= 'ent_counter'
    save_csv(file, final_list, path, file_name)


def visual_doc(doc):
    # change HEX colors
    colors = {'Wish': '#66abff', 'buy': '#66ff78', 'sell': '#FF5733'}
    #options = {'ents': ['Wish', 'buy', 'sell'], 'colors':colors}
    html = displacy.render(doc, style='ent') #, options=options
    file_name = '_displacy_visual.html'
    save_file(file, file_name, path, html)


if __name__ == '__main__':
    file = 'Bullish_text_sample.txt'
    ticker_list = 'data/stocks.tsv'
    path = r'C:\Users\suen6\PycharmProjects\Scraper_Yahoo_Finance\data'
    main(ticker_list, file, path)

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