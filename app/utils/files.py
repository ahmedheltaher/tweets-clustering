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

def countRowsInCSV(file: str) -> int:
    '''
        Returns the number of rows in a csv file

        Parameters
        ---------- 
            file: str
                file to count rows
        Returns
        -------
            int
                number of rows in the file
        
        Example
        -------
            >>> countRowsInCSV(INPUT_FILE)
            10
    '''

    return sum(1 for line in open(file))
