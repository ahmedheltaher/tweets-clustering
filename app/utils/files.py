from os import listdir  # Import the listdir function from the os module
from os.path import (  # Import the isfile and join functions from the os.path module
    isfile, join)


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
