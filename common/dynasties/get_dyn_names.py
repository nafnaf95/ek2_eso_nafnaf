### This was done in about 10 minutes so don't judge thank you very much
### How to use:
## 1. Put that in your common\dynasties folder
## 2. Delete the \results folder if it already exists
## 3. Run this script
## 4. You have two sets of files in the \results folder: the localization files containing the localized dynn_NAMES, and a set of files containing the raw dynn_NAMES for each culture
## 4a. This will ignore the 00_dynasties.txt file, if it exists
## 5. Make sure there isn't anything strange
## 6. Profit?

from os import walk
from os import path
from os import mkdir
from os import rename

# First, we try to create the results directory.
# If it fails, it means the user didn't delete the already existing one, which is a big nono
try:
	mkdir("results")
	mkdir("results\dynasty_names_loc")
	mkdir("results\dynasty_names_culture")
except OSError:
	print("The results directories could not be created. Please make sure to have deleted it beforehand.")
else:
	print("Successfully created the directory %s" % path)
	
	# Which files should be ignored: the 00_dynasties.txt and the current file (obviously)
	filenamesIgnore = ["00_dynasties.txt", path.basename(__file__)]

	# We build the list of files within the directory
	f = []
	for (_, _, filenames) in walk("."):
		for filename in filenames:
			if filename not in filenamesIgnore:
				f.append(filename)

	# We parse all these files, and extract the lines with name or culture in them
	# 700000 = {
		# name = "Anccermo"
		# culture = balfiera
	# }
	# 700001 = {
		# name = "Direnni"
		# culture = balfiera
	# }
	# In that we only want 'name = "Anccermo"' 'culture = balfiera' 'name = "Direnni"' and 'culture = balfiera'
	usableLines = []
	for filename in f:
		with open(filename, 'r') as file:
			fileContent = file.readlines()
			for line in fileContent:
				if "name" in line or "culture" in line:
					usedLine = line
					## Let's make this line readable: We only keep the dynasty or culture name
					# First we remove the special characters: We only have culture=CULTURE_NAME or name=DYNASTY_NAME after that point
					usedLine = usedLine.replace('\t', '').replace('\n', '').replace(' ', '')
					# Now we only take CULTURE_NAME or DYNASTY_NAME
					# Important, we keep the "" around the dynasty name!
					usedLine = usedLine.split('=')[1]
					# And we store the result
					usableLines.append(usedLine)

	# Now we have a big list or DYNASTY_NAME then CULTURE_NAME (the exact order shouldn't matter, but it's easier to keep it consistent)
	# We now create a list for each culture, containing all the names defined in this culture
	# First step is to change our big list of lines into a big list of duos DYNASTY_NAME - CULTURE_NAME, or the opposite
	culture_dynasty_duoList = []
	currentCultureName = ""
	currentDynastyName = ""
	for usableLine in usableLines:
		# We have a culture & dynasty duo, we pair them, and keep going
		if currentCultureName and currentDynastyName:
			culture_dynasty_duoList.append([currentCultureName, currentDynastyName])
			currentCultureName = ""
			currentDynastyName = ""
		if '"' in usableLine: # That's a dynasty name
			currentDynastyName = usableLine
		else: # That's a culture name
			currentCultureName = usableLine

	# Hell yeah we have our big ass list of duos, pogchamp
	# God this is way too complicated for what it is I'm sure one could do it with some grep or regex or some shit but hey, what are they gonna do, stab me?
	dict_culture_dynasties = {}
	for culture_dynasty_duo in culture_dynasty_duoList:
		# Now we buid our dictionnaries. Each culture will have its own dictionnary containing a big ass list of names
		# We create a dictionary where each culture is given an array of names
		# Keen eyes will recognize that I used this fragment of code in my other script, eheh
		if not culture_dynasty_duo[0] in dict_culture_dynasties:
			dict_culture_dynasties[culture_dynasty_duo[0]] = []
		dict_culture_dynasties[culture_dynasty_duo[0]].append(culture_dynasty_duo[1])

	# OK FINAL BIT POGGERS
	# We have our dictionnaries. Now we have to do two things: Create a loc file for each culture with each name being dynn_NAME:0 "NAME", and create a file for each culture with just the list of dynn_NAME
	for key in dict_culture_dynasties:
		print(key + " - " + ', '.join(dict_culture_dynasties[key]))
		# First, the loc file for the culture
		fileLocName = "dynasty_name_"+key+"_l_english.yml"
		with open(fileLocName, "w", encoding='utf-8-sig') as file:
			file.write("l_english:\n")
			for name in dict_culture_dynasties[key]:
				name = name.replace('"', '')
				file.write(" dynn_" + name + ":0 \"" + name + "\"\n")
		rename(fileLocName, "results/dynasty_names_loc/"+fileLocName)
		# Second, the file listing all the dynasties for the culture
		fileLocName = key+".txt"
		with open(fileLocName, "w", encoding='utf-8-sig') as file:
			for name in dict_culture_dynasties[key]:
				name = name.replace('"', '')
				file.write("dynn_" + name +" ")
		rename(fileLocName, "results/dynasty_names_culture/"+fileLocName)