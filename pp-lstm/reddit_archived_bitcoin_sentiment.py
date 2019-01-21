import requests, json
import datetime
import argparse

class RedditArchivedBitcoinSentiment(object):
    """
        Get archived data from Reddit and extract sentiment data from it.
    """
    def __init__(self, havenondemand_api_key='none'):
        self.havenondemand_api_key = havenondemand_api_key

    def __get_sentiment(self, year, month, day, verbose=False):
        month_string = str(month)
        if len(month_string) < 2:
            month_string = "0" + month_string
        day_string = str(day)
        if len(day_string) < 2:
            day_string = "0" + day_string
        date = str(year) + month_string + day_string

        wayback_url = "http://archive.org/wayback/available?url=reddit.com/r/bitcoin&timestamp=" + date
        r1 = requests.get(wayback_url)

        if(r1.status_code == 200):
            data1 = json.loads(r1.text)
            if 'closest' in data1['archived_snapshots']:
                archive_url = data1['archived_snapshots']['closest']['url']
            else:
                archive_url = None
                print("closest key not present")
                print(data1)
        else:
            archive_url = None
            print("Error return code = "+str(r1.status_code))

        havenondemand_url = 'https://api.havenondemand.com/1/api/sync/analyzesentiment/v1?apikey='+self.havenondemand_api_key+'&url='+archive_url        

        r2 = requests.get(havenondemand_url)

        if verbose:
            print('wayback: '+wayback_url)
            print('havenondemand '+havenondemand_url+"\n\n")

        if(r2.status_code == 200):
            data2 = json.loads(r2.text)
            return data2['aggregate']['score']
        else:
            print("Error return code = "+str(r2.status_code))

    def make_sentiment_dataset(self, outputfile='reddit_sentiment.csv', number_of_days_back=365, starting_search_date=datetime.datetime.now().date(), verbose=False):
        scores = {}
        date = starting_search_date        
        target = open(outputfile, 'a')
        for i in range(number_of_days_back):
            value = self.__get_sentiment(date.year, date.month, date.day, verbose=verbose)
            scores[(date.year, date.month, date.day)] = value
            stamp = self.format_date(date)
            target.write(stamp+','+str(value))
            target.write('\n')
            target.flush()
            date -= datetime.timedelta(days=1)
        target.close()

    def format_date(self, date):
        month_string = str(date.month)
        if len(month_string) < 2:
            month_string = "0" + month_string
        day_string = str(date.day)
        if len(day_string) < 2:
            day_string = "0" + day_string
        date_str = str(date.year) +'-'+ month_string +'-'+ day_string
        return date_str



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--o", dest="output_file", nargs='?', default='reddit_bitcoin_sentiment.csv')
    parser.add_argument("--d", dest="date", nargs='?', default=datetime.datetime.now().date())
    parser.add_argument("--n", dest="number_days_back", nargs='?', type=int, default=365)
    parser.add_argument("--v", dest="verbose", action='store_true')
    parser.add_argument("--k", dest="havenondemand_api_key", nargs='?', default='82dac440-e844-4ea7-87be-837989b98acc')
    args = parser.parse_args()

    date = datetime.datetime.strptime(args.date, '%Y/%m/%d')
    
    rsc = RedditArchivedBitcoinSentiment(havenondemand_api_key=args.havenondemand_api_key)
    rsc.make_sentiment_dataset(outputfile=args.output_file, number_of_days_back=args.number_days_back, starting_search_date=date, verbose=args.verbose)