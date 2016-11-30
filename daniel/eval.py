import sys, os, glob

def main():
		
	cwd = os.getcwd()
	filename = cwd + '/output.txt'

	negCorrect = 0
	negClassified = 0
	negBelong = 0

	posCorrect = 0
	posClassified = 0
	posBelong = 0
	
	with open(filename, 'r', encoding='latin1') as f:
		for line in f:
			line = line.rstrip('\n')
			# count belonging
			if line.endswith('neg'):
				negBelong += 1
			if line.endswith('pos'):
				posBelong += 1
			# count classified
			if line.startswith('NEGATIVE'):
				negClassified += 1
			if line.startswith('POSITIVE'):
				posClassified += 1
			# count correctness
			if line.startswith('NEGATIVE') and line.endswith('neg'):
				negCorrect += 1
			if line.startswith('POSITIVE') and line.endswith('pos'):
				posCorrect += 1

	# calculate precision
	negPrecision = negCorrect / negClassified
	posPrecision = posCorrect / posClassified\
	# calculate recall
	negRecall = negCorrect / negBelong
	posRecall = posCorrect / posBelong
	# calculate fscore
	negFScore = 2 * negPrecision * negRecall / (negPrecision + negRecall)
	posFScore = 2 * posPrecision * posRecall / (posPrecision + posRecall)

	print('\n__ EVALUATION __')
	print('Neg Precision: ' + str(negPrecision))
	print('Neg Recall:    ' + str(negRecall))
	print('Neg F Score:   ' + str(negFScore))
	print('Pos Precision:  ' + str(posPrecision))
	print('Pos Recall:     ' + str(posRecall))
	print('Pos F Score:    ' + str(posFScore))
	print('\n')

main()