requirements = ["os", "sys", "discord"];
doCloseFileAfterReq = False; # Sets to true if a required import isn't installed
for req in requirements:
	try:
		print(f"Importing {req}");
		exec(f"import {req}");
	except Exception as e:
		doCloseFileAfterReq = True;
		print(f"Missing {req} import!");
print("---")

fileArguments = sys.argv[1:]; # List of every CMD line arguments, excluding the file name
specialArguments = {"useJSONFile": False}; # Default version of special CMD line arguments

for fileArgument in fileArguments:
	if fileArgument[2:] in specialArguments:
		specialArguments[fileArgument[2:]] = True;

def extractValueFromNoneList(l: list):
	for x in l:
		if x != None: return x;
	else:
		return None;

infoArguments = {"token": "", "clisecret": "", "pubkey": "", "appid": 0, "guildid": 0};
if specialArguments["useJSONFile"] == True:
	# Read botinfo.json
	with open("botinfo.json", "r") as bij:
		bir = bij.read();
		biv = [[biw.replace(",","").replace("\t", "").replace("\"", "").strip() for biw in biw.split(":")] for biw in bir.split("\n")];biv.remove(["{"]);biv.remove(["}"]);
		for biw in biv:
			infoArguments[biw[0]] = biw[1]
		bij.close();
else:
	# Read environment variables
	for infoarg in infoArguments:
		infoArguments[infoarg] = extractValueFromNoneList([os.environ[envi] if envi == f"DISCORD_{infoarg.upper()}" else None for envi in os.environ]);

class EODCBClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = EODCBClient(intents=intents)
try:
	client.run(infoArguments["token"])
except Exception as e:
	print("No token in environment variables or botinfo.json!")