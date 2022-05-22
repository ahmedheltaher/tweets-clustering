import csv  # Import the csv module
import re
from datetime import datetime  # Import the datetime module
from os import mkdir  # Import the listdir function from the os module
from os.path import exists

from tqdm import tqdm  # Import the tqdm module

from app.utils.configurationReader import \
    Configuration  # Import the Confugration class to read the config file
from app.utils.files import \
    filesInDirectory  # Import the filesInDirectory function from the files module

# The pattern to find the links in the tweet
URL_PATTERN = r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))'

def formatData(data: str) -> list[str]:
	'''
		Format the data to be in the format of:
		[id, date, time, tweet, link]
		in the csv file

		Parameters
		----------
			data: str
				The data to be formatted

		Returns
		-------
			list[str]
				The formatted data

		Example
		-------
			>>> formatData('585978391360221184|Thu Apr 09 01:31:50 +0000 2015|Breast cancer risk test devised http://bbc.in/1CimpJF')
			['585978391360221184', '2015-04-09', '01:31:50', 'Breast cancer risk test devised', 'http://bbc.in/1CimpJF']
	'''
	try:
		# Split the data into id, dateTimeText, and the rest of the tweet
		id, dateTimeText, *wholeTweet = data.split('|')
		wholeTweet = ''.join(wholeTweet)  # Join the rest of the tweet

		# Find all the links in the tweet
		extractedLinks = [url[0] for url in re.findall(URL_PATTERN, wholeTweet)] 
		links = ','.join(extractedLinks)  # Join the links
		tweet = re.sub(URL_PATTERN, '', wholeTweet)  # Remove the links from the tweet

		# clean the tweet of any special characters
		tweet = tweet.replace("Â", "").replace("â€™", "'").replace("â€œ", '"').replace('â€“', '-').replace('â€', '"').strip()

		# Convert the dateTimeText to a datetime object
		dateTimeObject = datetime.strptime(dateTimeText, '%a %b %d %H:%M:%S %z %Y')
		
		return [id, dateTimeObject.date(), dateTimeObject.time(), tweet, links]
	except ValueError:
		# Catch the error if the data is not in the correct format and return an empty list
		# This is to prevent the program from crashing
		# Note: This is maybe not the best way to handle this error
		return []


def textToCsv(inputDirectory: str, outputDirectory: str, fileName: str):
	'''
		Converts the text file to csv file
		
		Parameters
		----------
			fileName: str
				The name of the file to be converted

		Returns
		-------
			None
			
		Example
		-------
			>>> textToCsv('foxnewshealth')
			# Writes the csv file to the output directory
	'''
	with open(f'{ inputDirectory }/{ fileName }.txt', 'r', encoding='ISO-8859-1') as textFile:  # Open the text file
		# Get the data from the text file as a list of lines
		dataLines = textFile.read().splitlines()
		# Iterate through the data and format it
		data = [formatData(line) for line in tqdm(dataLines, desc=f"Formating {fileName}")]
		# Remove the empty lines
		data = [line for line in data if line != []]

		with open(f'{ outputDirectory }/{ fileName }.csv', 'w', encoding='utf-8') as csvFile:  # Open the csv file
			writer = csv.writer(csvFile)  # Create a csv.writer object
			# Write the header
			writer.writerow(['id', 'date', 'time', 'tweet', 'links'])
			# Write the data to the csv file (Note: the data is a list of lists of strings)
			writer.writerows(data)


def main():
	'''
		Convert all txt files in the input directory to csv files in the output directory

		Parameters
		----------
			None

		Returns
		-------
			None

		Example
			>>> main()
			# The main function
	'''

	config = Configuration.load_json("./config/conversion.json")

	if not exists(config["inputDirectory"]):  # Check if the input directory exists
		print(
			f'The input directory { config["inputDirectory"] } does not exist\n')
		return

	# If the output directory does not exist create it
	if not exists(config["outputDirectory"]):
		print(
			f'The out directory { config["outputDirectory"] } does not exist, the script will create it for you, please wait...\n')
		mkdir(config["outputDirectory"])
		print('Finished creating the output directory\n')

	print('Converting text files to csv files...\n')

	# Get the list of files in the input directory
	files = filesInDirectory(config["inputDirectory"])

	for file in tqdm(files, desc="Formating Files"):  # tqdm is a progress bar
		# Splits the file name and removes the extension
		textToCsv(config["inputDirectory"], config["outputDirectory"], file.split('.')[0])

	# Print a message to the console
	print('\nConversion is Done Successfully!')


if __name__ == '__main__':
	main()
