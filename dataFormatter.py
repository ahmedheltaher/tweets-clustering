import csv
import re
from os import mkdir
from os.path import exists
from typing import List

from tqdm import tqdm  # Import the tqdm module

from app.utils.configrationReader import Confugration
from app.utils.files import filesInDirectory

MENTION_PATTERN = r'@([a-zA-Z0-9-_]{1,})'
HASHTAG_PATTERN = r'#([a-zA-Z0-9-_]{1,})'

def formatLine(line: List[str]) -> None:
	'''
		This function formats a line of data

		Parameters
		----------
			line: List[str]
				A list of strings representing a line of data

		Returns
		-------
			None

		Example
		-------
			>>> formatLine(['1', '2020-01-01', '12:00:00', 'This is a tweet from @user1 mentioning @user2 #hashtag1 #hashtag2', 'https://www.google.com'])
			['1', '2020-01-01', '12:00:00', 'this is a tweet mentioning', 'https://www.google.com', '@user1, @user2', '#hashtag1, #hashtag2']

	'''
	id, date, time, tweet, links, *_ = line # Get the data from the line and ignore the rest using the *_

	extractedMentions = re.findall(MENTION_PATTERN, tweet) # Extract the mentions from the tweet
	mentions = ','.join(extractedMentions) # combine the mentions into a string
	tweet = re.sub(MENTION_PATTERN, '', tweet) # Remove the mentions from the tweet

	extractedHashtags = re.findall(HASHTAG_PATTERN, tweet) # Extract the hashtags from the tweet
	hashtags = ','.join(extractedHashtags) # combine the hashtags into a string
	tweet = re.sub(HASHTAG_PATTERN, '', tweet) # Remove the hashtags from the tweet

	tweet = tweet.replace(" : ", "").strip() # Remove the : from the tweet and trim the spaces

	tweet = tweet.lower() # Convert the tweet to lower case

	return [id, date, time, tweet, links, mentions, hashtags] 


def formatFile(inputDirectory: str, outputDirectory: str, fileName: str) -> None:
	'''
		This function formats a file of data

		Parameters
		----------
			inputDirectory: str
				The directory of the input file

			outputDirectory: str
				The directory of the output file

			fileName: str
				The name of the file

		Returns
		-------
			None

		Example
		-------
			>>> formatFile('data/raw/', 'data/formatted/', 'tweets.csv')
			# This will format the file tweets.csv in the data/raw/ directory and save it in the data/formatted/ directory
	'''
	with open(f'{ inputDirectory }/{ fileName }.csv', 'r', encoding='utf-8') as file:  # Open the text file

		reader = csv.reader(file)
		next(reader)  # Skip the first line

		data = [formatLine(row) for row in tqdm(reader, desc=f'Formatting { fileName }')] # Format the data
		data = [row for row in data if row is not None or row != []] # Remove the None values
		with open(f'{ outputDirectory }/{ fileName }.csv', 'w', encoding='utf-8') as csvFile:  # Open the csv file
			writer = csv.writer(csvFile)  # Create a csv.writer object
			# Write the header
			writer.writerow(['id', 'date', 'time', 'tweet', 'links', 'mentions', 'hashtags'])
			# Write the data to the csv file (Note: the data is a list of lists of strings)
			writer.writerows(data)


def main():
	'''
		This function formats the data

		Parameters
		----------
			None

		Returns
		-------
			None

		Example
		-------
			>>> main()
			# This will format the data
	'''

	config = Confugration.load_json("./config/formatting.json") # Load the config file

	if not exists(config["inputDirectory"]):  # Check if the input directory exists
		print(f'The input directory { config["inputDirectory"] } does not exist\n')
		return

	if not exists(config["outputDirectory"]):  # If the output directory does not exist create it
		print(
			f'The out directory { config["outputDirectory"] } does not exist, the script will create it for you, please wait...\n')
		mkdir(config["outputDirectory"])
		print('Finished creating the output directory\n')

	files = filesInDirectory(config["inputDirectory"]) # Get the list of files in the input directory

	print('Formatting Data...\n')


	for file in tqdm(files, desc="Formating Files"):  # tqdm is a progress bar
		# Splits the file name and removes the extension
		formatFile(config["inputDirectory"], config["outputDirectory"], file.split('.')[0])

	print('\nFormatting is Done Successfully!')  # Print a message to the console
	

	pass


if __name__ == '__main__':
	main()
