import spacy
import pandas as pd
import os
from datetime import datetime
import os
import os.path

# lg for accuracy
nlp = spacy.load("en_core_web_sm")

class Sentiment:
    def __init__(self, sentiment_type):
        self.name = sentiment_type
        self.total_upvote = 0
        self.total_downvote = 0
        self.count = 0
        self.message = []
        self.doc = ''

    def add_data_row(self, data_row):
        self.count += 1
        self.total_upvote += data_row.upvote
        self.total_downvote += data_row.downvote
        self.message.append(data_row.message)

    def list_to_doc(self, list):
        text = ''
        self.doc = nlp(text.join(list))

class Sentiment_data_row:
    def __init__(self, index, row):
        self.sentiment_type = index
        self.upvote = row[0]
        self.downvote = row[1]
        self.message = row[2]


bullish = Sentiment('Bullish')
bearish = Sentiment('Bearish')
neutral = Sentiment('Neutral')

sentiment_types = {'Bullish': bullish, 'Bearish': bearish, 'Neutral': neutral}


def main(file, path):
    df = pd.read_csv(os.path.join(path, file), index_col=None)
    # drop null values and set 'Sentiment as index
    cleaned_data = clean_dataframe(df)
    # append messages to respective list
    parse_data(cleaned_data)
    # process messages

    # save(summary, file, path)
    save(file, path)


def clean_dataframe(unfiltered_data):
    # remove characters that are not a string
    unfiltered_data.drop(unfiltered_data.columns[[0, 1, 2]], axis=1, inplace=True)
    # reset index to 'Sentiment'
    unfiltered_data.set_index('Sentiment', inplace=True)
    # remove null units in 'Sentiment'
    data = unfiltered_data[unfiltered_data.index.notnull()]
    # data = unfiltered_data[unfiltered_data.index.notna()]
    # convert the two columns with NaNs to 0
    data.update(data[['Upvote', 'Downvote']].fillna(0))

    """
    # SettingWithCopyWarning: pandas sees these operations as separate events,
    so it has to treat them as linear operations, they happen one after another.
    Other ways:
    data.update(data[["Upvote", "Downvote"]].fillna(0, inplace=True))

    for col in ['Upvote', 'Downvote']:
        data[col].fillna(0, inplace=True)

    # The following creates 
    data = unfiltered_data.loc[unfiltered_data.index.dropna(how='any', inplace=True)]

    # can't remove index with this function: 
    unfiltered_data['Sentiment'].dropna(how='all')

    # duplicated the entire dataframe at least 6 times
    data = unfiltered_data.loc[unfiltered_data.index.dropna(how='all]
    """
    return data


def parse_data(cleaned_data):
    for index, row in cleaned_data.iterrows():
        data = Sentiment_data_row(index, row)
        if data.sentiment_type:
            # match row to dictionary
            sentiment = sentiment_types[data.sentiment_type]
            sentiment.add_data_row(data)
    for sentiment_type in sentiment_types.values():
        # convert object to string and create Doc container
        sentiment_type.str = sentiment_type.list_to_doc(sentiment_type.message)


def save(file, path):
    directory = file[:-4] + '_analysis.csv'
    output_dic = {}
    for name, sentiment_type in sentiment_types.items():
        array = []
        array.append(sentiment_type.total_upvote)
        array.append(sentiment_type.total_downvote)
        array.append(sentiment_type.count)
        output_dic[sentiment_type.name] = array
    indexes = ('Upvote Count', 'Downvote Count', 'Post Count')
    output_df = pd.DataFrame(output_dic, index=indexes)
    try:
        output_df.to_csv(os.path.join(path, directory))
        print('saved to {}'.format(path))
    except Exception as e:
        print('saving file failed: ', e)


if __name__ == '__main__':
    file = '220218_Top_Reactions_20_pages_WISH.csv'
    path = r'C:\Users\suen6\PycharmProjects\Scraper_Yahoo_Finance\data'
    main(file, path)