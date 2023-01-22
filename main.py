requirements = ["os", "sys", "discord", "asyncio"];
doCloseFileAfterReq = False; # Sets to true if a required import isn't installed
for req in requirements:
	try:
		print(f"Importing {req}");
		exec(f"import {req}");
	except Exception as e:
		doCloseFileAfterReq = True;
		print(f"Missing {req} import!");

if doCloseFileAfterReq:
	input("")
	exit()
print("---")

fileArguments = sys.argv[1:]; # List of every CMD line arguments, excluding the file name
specialArguments = { # Default version of special CMD line arguments
	"useJSONFile": False, # Whether or not to use botinfo.json in your local directory (must have same entry names as infoArguments)
	"useTestRun": False # Whether or not to stop the run after a short amount of time, useful for GitHub actions testing
};

for fileArgument in fileArguments: # Loop through every CMD line argument, and change special arguments value if specified
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
		self.messageLog = []
		print(f'Logged on as {self.user}!')
		print(f'Retrieved app ID {infoArguments["appid"]} and main guild ID {infoArguments["guildid"]}')
		if specialArguments["useTestRun"] == True: # Close bot after [sts] seconds to stop test run
			print(f'Using test run mode, beginning stop countdown')
			sts = 30
			for i in range(sts):
				print(f'{sts} seconds until stopping')
				sts -= 1
				await asyncio.sleep(1)
			print(f'Stopping discord bot')
			await self.close() # Close the bot
			raise SystemExit # Exit the program

	async def on_message(self, message):
		self.messageLog.append([message.author, message.content])
		self.messageLog = self.messageLog[-25:] # Only cache the most recent 25 messages

intents = discord.Intents.default()
intents.message_content = True

client = EODCBClient(intents=intents)
try:
	client.run(infoArguments["token"])
except TypeError as e:
	print("No token in environment variables or botinfo.json!")