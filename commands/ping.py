import interactions, discord

class PingCommand(interactions.Extension):
	def __init__(self, client, dpyClient):
		self.client: interactions.Client = client
		self.dpyClient: discord.Client = dpyClient

	@interactions.extension_command(
		name="ping",
    	description="Get the latency of the bot"
    )
	async def ping_command(self, ctx: interactions.CommandContext):
		await ctx.send(f"Ping! Latency is {round(self.dpyClient.latency*1000)}ms")

def setup(client, dpyClient):
	PingCommand(client, dpyClient)