#  Naive Bayes

import sys, os, re, json

def main():
		
	cwd = os.getcwd()

	modelName = cwd + '/model.txt'
	trainingFile = 'reviews_final.txt'
	trainingDirectory = cwd + '/imdb/train'

	# JSON model for outputing to text file
	model = {
		'neg': 0,
		'pos': 0,
		'data': {}
	}

	for dirName, subDirs, files in os.walk(trainingDirectory):
		for filename in files:
			if filename.endswith('.txt'):

				with open(dirName + '/' + filename, 'r', encoding='latin1') as f:
					data = f.read()

					# iterate through every movie review in the training data
					# for line in data:

						# parse movie review
						# movieReview = line.split('|')
						# name = movieReview[1]
						# review = movieReview[2]
						# polarity = movieReview[3]

					# reviewWords = re.split(r'[;,\s.!?:#]\s*', review.lower())
					polarity = 'NEGATIVE' if 'neg' in dirName else 'POSITIVE'
					reviewWords = re.split(r'[\s\n]+', data)

					if 'POSITIVE' in polarity:
						model['neg'] += len(reviewWords)
					elif 'NEGATIVE' in polarity:
						model['pos'] += len(reviewWords)

					# update model for every word in the review
					for word in reviewWords:
						if not len(word) == 0:
							
							# put word in model if it's a new word
							if word not in model['data']:
								model['data'][word] = {
									'neg': 0,
									'pos': 0
								}

							# add polarity counts for the word
							if 'NEGATIVE' in polarity:
								model['data'][word]['neg'] += 1
							elif 'POSITIVE' in polarity:
								model['data'][word]['pos'] += 1

	# open a file to write the model data to
	with open(modelName, 'w', encoding='latin1') as f:
		json.dump(model, f)


# Run the script
main()