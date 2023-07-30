import argparse

# parser = argparse.ArgumentParser(description='Process some integers.')
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')

# args = parser.parse_args()
# print(args.accumulate(args.integers))


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--my-foo', default='foobar')
parser.add_argument('-b', '--bar-value', default=3.14)
args = parser.parse_args()
argsdict = vars(args)
print(argsdict['my_foo'])
print(argsdict['bar_value'])
