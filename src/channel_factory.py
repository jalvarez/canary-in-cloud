class Channel:
	pass

class ChannelFactory:
	def newEmailChannel(self, email):
		return Channel()
