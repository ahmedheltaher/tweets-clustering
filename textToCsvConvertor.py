import csv  # Import the csv module
import re
from datetime import datetime  # Import the datetime module
from os import listdir, mkdir  # Import the listdir function from the os module
from os.path import (  # Import the isfile and join functions from the os.path module
    exists, isfile, join)

from tqdm import tqdm  # Import the tqdm module

INPUT_DIRECTORY = './dataset/original' # The directory where the txt files are located
OUTPUT_DIRECTORY = './dataset/csv' # The directory where the csv files will be saved

PATTERN = r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))'

def filesInDirectory(dir: str) -> list[str]:
	'''
		Returns a list of files in a directory

		Parameters
		---------- 
			dir: str
				directory to search
		Returns
		-------
			list[str]
				list of files in the directory
		
		Example
		-------
			>>> filesInDirectory(INPUT_DIRECTORY)
			['foxnewshealth.txt', 'latimeshealth.txt', 'nprhealth.txt', 'NBChealth.txt', 'msnhealthnews.txt', ...]
	'''

	return [f for f in listdir(dir) if isfile(join(dir, f))]

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
		id, dateTimeText, *wholeTweet = data.split('|') # Split the data into id, dateTimeText, and the rest of the tweet
		wholeTweet = ''.join(wholeTweet) # Join the rest of the tweet
		
		# extract the link from the tweet
		extractedLinks = re.findall(PATTERN, wholeTweet) # Find all the links in the tweet
		links = '' # Initialize the link

		for extractedLink in extractedLinks: # Iterate through the links
			links += f"{extractedLink[0]}," # Add the link to the links string
			wholeTweet = wholeTweet.replace(extractedLink[0], '') # Remove the link from the tweet
			break
		
		tweet = wholeTweet.strip() # Remove the whitespace from the tweet

		if links != '': # If there are links
			links = links[:-1] if links[-1] == ',' else links # Remove the last comma if it exists
			links = links.strip() # Remove the whitespace from the link

		dateTimeObject = datetime.strptime(dateTimeText, '%a %b %d %H:%M:%S %z %Y') # Convert the dateTimeText to a datetime object
		return [id, dateTimeObject.date(), dateTimeObject.time(), tweet, links] # Return the formatted data
	except ValueError:
		# Catch the error if the data is not in the correct format and return an empty list
		# This is to prevent the program from crashing
		# Note: This is maybe not the best way to handle this error
		# Note: an empty list will be ignored by the csv.writerow() function
		return []


def textToCsv(fileName: str):
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
	with open(f'{ INPUT_DIRECTORY }/{ fileName }.txt', 'r', encoding='ISO-8859-1') as textFile:  # Open the text file
		dataLines = textFile.read().splitlines() # Get the data from the text file as a list of lines
		data = [formatData(line) for line in tqdm(dataLines, desc=f"Formating {fileName}")] # Iterate through the data and format it

		with open(f'{ OUTPUT_DIRECTORY }/{ fileName }.csv', 'w', encoding='utf-8') as csvFile: # Open the csv file
			writer = csv.writer(csvFile) # Create a csv.writer object
			writer.writerow(['id', 'date', 'time', 'tweet', 'links']) # Write the header
			# Write the data to the csv file (Note: the data is a list of lists of strings) &
			# (Note: the csv.writerow() function will ignore empty lists)
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

	if not exists(INPUT_DIRECTORY): # Check if the input directory exists
		print(f'The input directory { INPUT_DIRECTORY } does not exist\n')
		return

	if not exists(OUTPUT_DIRECTORY):  # If the output directory does not exist create it
		print(f'The out directory { INPUT_DIRECTORY } does not exist, the script will create it for you, please wait...\n')
		mkdir(OUTPUT_DIRECTORY)
		print('Finished creating the output directory\n')

	print('Converting text files to csv files...\n')

	files = filesInDirectory(INPUT_DIRECTORY) # Get the list of files in the input directory
	
	for file in tqdm(files, desc="Formating Files"): # tqdm is a progress bar
		textToCsv(file.split('.')[0]) # Splits the file name and removes the extension

	print('\nConversion is Done Successfully!') # Print a message to the console


if __name__ == '__main__':
	main()
