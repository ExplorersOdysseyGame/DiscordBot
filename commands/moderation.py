import interactions, discord

permissionsRole = 1069178019995992114
guildID = 1066335615517458442
modlogChannel = 1066681462855843920
globalDpyClient = None

class ModerationCommand(interactions.Extension):
	def __init__(self, client, dpyClient):
		global globalDpyClient
		self.client: interactions.Client = client
		globalDpyClient = dpyClient
		self.dpyClient: discord.Client = dpyClient

	async def logAction(self, actionName: str, actionReason: str, target: discord.Member, actor: discord.Member, clr: str = 0xFF3333):
		# Mod data file in format of "ID:Warns,Mutes,Kicks,TempBans,Bans"
		actionType = actionName
		with open("data/modrecord.txt", "r") as moddatafileREAD:
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
				backup = md
				try:
					newline=[]
					prevData = selectedLineCache.split(":")[1].split(",")
					if actionName == "Ban": newLineData = f"{target.id}:{int(prevData[0])},{int(prevData[1])},{int(prevData[2])},{int(prevData[3])},{int(prevData[4])+1}"
					elif actionName == "TempBan": newLineData = f"{target.id}:{int(prevData[0])},{int(prevData[1])},{int(prevData[2])},{int(prevData[3])+1},{int(prevData[4])}"
					elif actionName == "Kick": newLineData = f"{target.id}:{int(prevData[0])},{int(prevData[1])},{int(prevData[2])+1},{int(prevData[3])},{int(prevData[4])}"
					elif actionName == "Mute": newLineData = f"{target.id}:{int(prevData[0])},{int(prevData[1])+1},{int(prevData[2])},{int(prevData[3])},{int(prevData[4])}"
					else: newLineData = f"{target.id}:{int(prevData[0])+1},{int(prevData[1])},{int(prevData[2])},{int(prevData[3])},{int(prevData[4])}"
					f = open("data/modrecord.txt", "w")
					data = ""
					for line in lines:
						nl = line
						nl = nl if nl.endswith("\n") else nl+"\n"
						nl = nl.replace(selectedLineCache, newLineData+"\n")
						data = data + nl
					f.write(data)
					f.close()
				except Exception as e:
					with open("data/modrecord.txt", "w") as f: f.write(backup)
			else:
				with open("data/modrecord.txt", "a") as moddatafileA:
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
		scope=guildID
	)
	async def moderation_command(self, ctx: interactions.CommandContext):
		global globalDpyClient
		roles = ctx.member.roles
		permitUsage = False
		for role in roles:
				if role == permissionsRole:
					permitUsage = True
		if permitUsage == True:
			modal = interactions.Modal(
				title="Moderation Form",
				custom_id="moderation_actform",
				components=[
					interactions.TextInput(
						style=interactions.TextStyleType.SHORT,
						label="Punishment (Warn, Mute, Kick, TempBan or Ban)",
						custom_id="moderation_actform_respun",
						min_length=1,
						max_length=9,
						required=True
					),
					interactions.TextInput(
						style=interactions.TextStyleType.SHORT,
						label="User ID",
						custom_id="moderation_actform_resid",
						min_length=1,
						max_length=20,
						required=True
					),
					interactions.TextInput(
						style=interactions.TextStyleType.SHORT,
						label="Reason for Punishment",
						custom_id="moderation_actform_reswhy",
						min_length=1,
						max_length=128,
						required=False
					)
				],
			)

			await ctx.popup(modal)
			@self.client.modal("moderation_actform")
			async def moderation_actform_response(self, moderation_actform_respun,moderation_actform_resid,moderation_actform_reswhy):
				target = await interactions.get(self.client, interactions.Member, parent_id=guildID, object_id=int(moderation_actform_resid))
				if moderation_actform_respun.lower() == "warn":
					await ctx.send(f"Warned <@{target.id}> for {reason}.", ephemeral=True)
					await self.logAction("Warn", moderation_actform_reswhy, target, ctx.member, clr=0xFF8000)
				elif moderation_actform_respun.lower() == "mute":
					await ctx.send(f"Muted <@{target.id}> for {reason}.", ephemeral=True)
					await self.logAction("Mute", moderation_actform_reswhy, target, ctx.member, clr=0xFA2AAB)
				elif moderation_actform_respun.lower() == "kick":
					await ctx.send(f"Kicked <@{target.id}> for {reason}.", ephemeral=True)
					await self.logAction("Kick", moderation_actform_reswhy, target, ctx.member, clr=0xF4D556)
				elif moderation_actform_respun.lower() == "tempban":
					await ctx.send(f"Temporarily banned <@{target.id}> for {reason}.", ephemeral=True)
					await self.logAction("TempBan", moderation_actform_reswhy, target, ctx.member, clr=0xEF8001)
				elif moderation_actform_respun.lower() == "ban":
					await ctx.send(f"Permanently banned <@{target.id}> for {reason}.", ephemeral=True)
					await self.logAction("Ban", moderation_actform_reswhy, target, ctx.member, clr=0xEA2AAC)
				else:
					await ctx.send(f"Missing or incorrect subcommand!", ephemeral=True)
		else:
			await ctx.send("You do not have permission to use this command.", ephemeral=True)

def setup(client, dpyClient):
	ModerationCommand(client, dpyClient)