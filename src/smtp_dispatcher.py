import smtplib

class SmtpDispatcher:
	def __init__(self, config):
		self.config = config

	def send(self, email_to, subject, body):
		email_from = self.config.get('SMTP_USER')
		message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % \
					(email_from, email_to, subject, body)
		email_host = self.config.get('SMTP_HOST')
		email_port = self.config.get('SMTP_PORT')
		email_user = self.config.get('SMTP_USER')
		email_pass = self.config.get('SMTP_PASS')

		try:
			server = smtplib.SMTP(email_host, email_port)
			server.ehlo()
			server.starttls()
			server.login(email_user, email_pass)
			server.sendmail(email_from, email_to, message)
		finally:
			try:
				server.close()
			except:
				pass

