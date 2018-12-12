import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--look_back", dest="look_back", nargs='?', type=int, default=2)
parser.add_argument("--sent", dest="use_sentiment", action='store_true')
args = parser.parse_args()
print(args.look_back)
print(args.use_sentiment)

