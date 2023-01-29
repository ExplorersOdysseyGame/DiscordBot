import interactions, discord

permissionsRole = 1069178019995992114
guildID = 1066335615517458442
modlogChannel = 1066681462855843920

class ModerationCommand(interactions.Extension):
	def __init__(self, client, dpyClient):
		self.client: interactions.Client = client
		self.dpyClient: discord.Client = dpyClient

	async def logAction(self, actionName: str, actionReason: str, target: discord.Member, actor: discord.Member, clr: str = 0xFF3333):
		# Mod data file in format of "ID:Warns,Mutes,Kicks,TempBans,Bans"
		actionType = actionName
		with open("data/moddata.txt", "r") as moddatafileREAD:
			md = moddatafileREAD.read()
			lineExists = False
			lineNumber = 0
			selectedLineCache = ""
			lines = md.split("\n")
			for line in lines:
				if line.split(":")[0] == target.id:
					lineExists = True
					selectedLineCache = line
					break
				lineNumber += 1
			if lineExists:
				newline=[]
				prevData = selectedLineCache.split(":")[1].split(",")
				if actionName == "Ban": newLineData = f"{target.id}:{int(prevData[0])},{int(prevData[1])},{int(prevData[2])},{int(prevData[3])},{int(prevData[4])+1}"
				elif actionName == "TempBan": newLineData = f"{target.id}:{int(prevData[0])},{int(prevData[1])},{int(prevData[2])},{int(prevData[3])+1},{int(prevData[4])}"
				elif actionName == "Kick": newLineData = f"{target.id}:{int(prevData[0])},{int(prevData[1])},{int(prevData[2])+1},{int(prevData[3])},{int(prevData[4])}"
				elif actionName == "Mute": newLineData = f"{target.id}:{int(prevData[0])},{int(prevData[1])+1},{int(prevData[2])},{int(prevData[3])},{int(prevData[4])}"
				else: newLineData = f"{target.id}:{int(prevData[0])+1},{int(prevData[1])},{int(prevData[2])},{int(prevData[3])},{int(prevData[4])}"
				f = open("data/moddata.txt", "w")
				data = ""
				for line in lines:
					nl = nl if nl.endsWith("\n") else nl+"\n"
					nl = nl.replace(selectedLineCache, newLineData+"\n")
				    data = data + nl
				f.write(data)
				f.close()
			else:
				with open("data/moddata.txt", "a") as moddatafileA:
					if actionName == "Ban": moddatafileA.write(f"{target.id}:0,0,0,0,1")
					elif actionName == "TempBan": moddatafileA.write(f"{target.id}:0,0,0,1,0")
					elif actionName == "Kick": moddatafileA.write(f"{target.id}:0,0,1,0,0")
					elif actionName == "Mute": moddatafileA.write(f"{target.id}:0,1,0,0,0")
					else: moddatafileA.write(f"{target.id}:1,0,0,0,0")
					moddatafileA.write("\n")

		g = None
		for guild in self.client.guilds:
			if guild.id == guildID:
				g = guild
		chan = None
		for channel in await g.get_all_channels():
			if channel.id == modlogChannel:
				chan = channel
		async with chan.typing:
			embed = interactions.Embed(
				title = actionName,
				author = interactions.EmbedAuthor(
					name=f"Acted by {actor.name}#{actor.discriminator}",
					icon_url = actor.avatar_url
				),
				color = clr,
				fields = [
					interactions.EmbedField(
						name="Action Reason",
   						value=actionReason,
						inline=False,
					),
					interactions.EmbedField(
						name="Action Target",
   						value=f"{target.name}#{target.discriminator}",
						inline=False,
					)
				]
			)
			await chan.send(embeds = embed)

	@interactions.extension_command(
		name="moderation",
		description="Moderation commands for the bot",
		scope=guildID,
		options=[
			interactions.Option(
				name="warn",
				description="Warn a member of the server",
				type=interactions.OptionType.SUB_COMMAND,
				options=[
					interactions.Option(
						name="target",
						description="The member to warn",
						type=interactions.OptionType.USER,
						required=True,
					),
					interactions.Option(
						name="reason",
						description="The reason for the warning",
						type=interactions.OptionType.STRING,
						required=False,
					),
				],
			),
			interactions.Option(
				name="mute",
				description="Mute a member of the server",
				type=interactions.OptionType.SUB_COMMAND,
				options=[
					interactions.Option(
						name="target",
						description="The member to mute",
						type=interactions.OptionType.USER,
						required=True,
					),
					interactions.Option(
						name="reason",
						description="The reason for the mute",
						type=interactions.OptionType.STRING,
						required=False,
					),
				],
			)
		]
	)
	async def moderation_command(self, ctx: interactions.CommandContext, sub_command: str = None, target: str = None, reason: str = "No specified reason."):
		roles = ctx.member.roles
		permitUsage = False
		for role in roles:
			if role == permissionsRole:
				permitUsage = True
		if permitUsage == True:
			if sub_command == "warn":
				await ctx.send(f"Warned <@{target.id}> for {reason}.", ephemeral=True)
				await self.logAction("Warn", reason, target, ctx.member, clr=0xFF8000)
			elif sub_command == "mute":
				await ctx.send(f"Muted <@{target.id}> for {reason}.", ephemeral=True)
				await self.logAction("Mute", reason, target, ctx.member, clr=0xFF3000)
			else:
				await ctx.send(f"Missing or incorrect subcommand!", ephemeral=True)
		else:
			await ctx.send("You do not have permission to use this command.", ephemeral=True)

def setup(client, dpyClient):
	ModerationCommand(client, dpyClient)