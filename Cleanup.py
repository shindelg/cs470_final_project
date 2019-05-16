import os, shutil, csv

from time import gmtime, strftime
from datetime import datetime
from glob import glob

# Method to update names
def update_name(filename, tmp):
	new_name = tmp
	new_name += executionTime
	new_name += ".csv"
	os.rename(filename, new_name)

# Current time at the start of the script, to keep things consistent
# executionTime = strftime("%Y-%m-%d %H:%M:%S", gmtime.now())
now = datetime.now()
executionTime = now.strftime('%Y-%m-%d %H:%M:%S')

check_dir = './Version_History'

fullpath1 = os.path.join

if not os.path.exists(check_dir):
	os.mkdir(check_dir)

new_dir = './Version_History/Data '
new_dir += executionTime


fullpath = os.path.join

os.mkdir(new_dir)

# Change name of various files in the directory
for filename in os.listdir("."):

	if filename.startswith("public"):
		update_name(filename, "publicComp ")

	elif filename.startswith("Failed"):
		update_name(filename, "FailedTickers ")

	elif filename.startswith("Success"):
		update_name(filename, "SuccessTickers ")

	elif filename.startswith("exchange"):
		update_name(filename, "exchangeRate ")

	elif filename.startswith("Updated"):
		update_name(filename, "UpdatedCompanyInformation ")

# Move files into a subdirectory; remove unnecessary files
for filename in os.listdir("."):

	if filename.startswith("output"):
		os.remove(filename)

	elif filename.endswith(".csv"):
		shutil.move(filename, new_dir)
