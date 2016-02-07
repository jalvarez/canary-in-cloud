from smtp_dispatcher import SmtpDispatcher

class Channel:
	pass

class Message:
	def __init__(self, subject, body):
		self.subject = subject
		self.body = body

	def get_subject(self):
		return self.subject

	def get_body(self):
		return self.body

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
