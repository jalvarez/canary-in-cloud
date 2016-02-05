from smtp_dispatcher import SmtpDispatcher

class Channel:
	pass

class EmailChannel(Channel):
	def __init__(self, config, email_to):
		self.dispatcher = SmtpDispatcher(config)
		self.email_to = email_to

	def sendMessage(self, message):
		self.dispatcher.send(self.email_to, message.get_subject(), \
							message.get_body())

class ChannelFactory:
	def __init__(self, config):
		self.config = config

	def newEmailChannel(self, email):
		return EmailChannel(self.config, email)
