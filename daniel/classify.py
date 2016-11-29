# Naive Bayes

import sys, os, re, json, math

def main():

	cwd = os.getcwd()
	modelName = cwd + '/model.txt'
	outputName = cwd + '/output.txt'

	testDirectory = cwd + '/imdb/test'

	imdb = False
	tomato = True

	# load model data
	model = {}
	with open(modelName, 'r', encoding='latin1') as f:
		model = json.load(f)

	reviewCount = model['neg'] + model['pos']
	polarityProbabilities = { 'neg': model['neg'] / reviewCount, 'pos': model['pos'] / reviewCount }

	negCount = model['neg']
	posCount = model['pos']
	totCount = negCount + posCount

	outputFile = open(outputName, 'w', encoding='latin1')

	if imdb:
		for dirName, subDirs, files in os.walk(testDirectory):
			for filename in files:
				if filename.endswith('.txt'):
					with open(dirName + '/' + filename, 'r', encoding='latin1') as f:
						data = f.read()
						words = re.split(r'[\s\n]+', data)

						pGivenNeg = 0
						pGivenPos = 0

						for word in words:
							if word in model['data']:
								pNeg = (model['data'][word]['neg'] + 1) / (negCount + totCount)
								pPos = (model['data'][word]['pos'] + 1) / (posCount + totCount)
								# count + 1 / totalClass + total
								pGivenNeg += math.log(pNeg)
								pGivenPos += math.log(pPos)
						
						pNegGivenReview = polarityProbabilities['neg'] + pGivenNeg
						pPosGivenReview = polarityProbabilities['pos'] + pGivenPos

						neutralReview = False
						pDif = abs(abs(pNegGivenReview) - abs(pPosGivenReview))
						if pDif < abs(pNegGivenReview / 200) or pDif < abs(pPosGivenReview / 200):
							neutralReview = True

						finalPolarity = 'NEGATIVE' if pNegGivenReview > pPosGivenReview else 'POSITIVE'
						outputFile.write(finalPolarity + ' | ' + data + ' | ' + dirName + '\n')

						# if neutralReview:
						# 	print('Neutral ' + str(pDif) + '  :  ' + str(pNegGivenReview) + ' - ' + str(pPosGivenReview))
						# elif pNegGivenReview > pPosGivenReview:
						# 	print('Negative')
						# elif pPosGivenReview > pNegGivenReview:
						# 	print('Positive')
						# else:
						# 	print('Huh?')

	elif tomato:
		with open('reviews_final.txt', 'r', encoding='latin1') as f:
			data = f.readlines()

			# iterate through every movie review in the training data
			for line in data:

				# parse movie review
				movieReview = line.split('|')
				name = movieReview[1]
				review = movieReview[2]
				polarity = movieReview[3]

				if 'NEGATIVE' in polarity:
					polarity = 'neg'
				elif 'POSITIVE' in polarity:
					polarity = 'pos'

				reviewWords = re.split(r'[;,\s.!?:#]\s*', review.lower())

				pGivenNeg = 0
				pGivenPos = 0

				for word in reviewWords:
					if word in model['data']:
						pNeg = (model['data'][word]['neg'] + 1) / (negCount + totCount)
						pPos = (model['data'][word]['pos'] + 1) / (posCount + totCount)
						# count + 1 / totalClass + total
						pGivenNeg += math.log(pNeg)
						pGivenPos += math.log(pPos)
				
				pNegGivenReview = polarityProbabilities['neg'] + pGivenNeg
				pPosGivenReview = polarityProbabilities['pos'] + pGivenPos

				neutralReview = False
				pDif = abs(abs(pNegGivenReview) - abs(pPosGivenReview))
				if pDif < abs(pNegGivenReview / 200) or pDif < abs(pPosGivenReview / 200):
					neutralReview = True

				finalPolarity = 'NEGATIVE' if pNegGivenReview > pPosGivenReview else 'POSITIVE'
				print(finalPolarity + '   |   ' + polarity)
				outputFile.write(finalPolarity + ' | ' + ' | ' + polarity + '\n')

main()