import argparse
parser = argparse.ArgumentParser(description='argparse testing')
parser.add_argument('--name','-n',type=str, default = "bk",required=True,help="a programmer's name")
parser.add_argument('--age','-a',type=int, default=35,help='age of the programmer')
parser.add_argument('--sex','-s',type=str, default='male')
parser.add_argument('--favorite','-f',type=str, nargs="+",required=False,help="favorite of the programmer")

args = parser.parse_args()

print(args.name)
print(args.age)
print(args.sex)
print(args.favorite)