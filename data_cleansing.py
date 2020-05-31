import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('input_file', type=str)
parser.add_argument('output_file', type=str)

args = parser.parse_args()

normal = 0
nan = 0
with open(args.input_file, 'rb') as f:
	with open(args.output_file, 'wb') as w:
		for line in f:
			try:
				json.loads(line)
				w.write(line)
				normal += 1
			except Exception as e:
				print(e)
				print(line)
				nan += 1

print(normal, nan, float(normal) / (normal + nan))