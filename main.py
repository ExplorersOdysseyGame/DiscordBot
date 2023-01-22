requirements = ["os", "sys", "discord"]
doCloseFileAfterReq = False # Sets to true if a required import isn't installed
for req in requirements:
  try:
    print(f"Importing {req}")
    exec(f"import {req}")
  except Exception as e:
    doCloseFileAfterReq = True
    print(f"Missing {req} import!")

fileArguments = sys.argv[1:] # List of every CMD line arguments, excluding the file name
specialArguments = {"useJSONFile": False} # Default version of special CMD line arguments

for fileArgument in fileArguments:
  print(fileArgument[2:])
  if fileArgument[2:] in specialArguments:
    specialArguments[fileArgument[2:]] = True

if specialArguments["useJSONFile"] == True:
	# Read botinfo.json
	pass
else:
	# Read environment variables
	pass

print(specialArguments, doCloseFileAfterReq)
