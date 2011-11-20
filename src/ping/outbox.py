
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#      sendMail.py
#
#      Copyright 2010 Ben Davenport-Ray <ben@benslaptop>
#
#      This program is free software; you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation; either version 2 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program; if not, write to the Free Software
#      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#      MA 02110-1301, USA.

import smtplib
import poplib
import imaplib
import mailbox

class Outbox:
	""" A list of mail messages that can be periodically sent to their recipients. """

	def __init__ (self, account):
		"""
		Constructor.

		account -- the account that will be used to send mail.
		"""
		self.queue = []
		self.account = account

	def add (self, message):
		""" Adds a message to the list.

		message -- The message to add.
		"""
		self.queue.append(message)

	def send_all (self, password):
		""" sends all the messages """
		print "Sendall called."
		for mNumber in self.queue:
			self.send(self.queue.pop(), password)

	def send(self, message, password):
		print "Send called: Account" + self.account.out_server
		mailServer = smtplib.SMTP(self.account.out_server, self.account.out_port)
		print "Server created."
		mailServer.ehlo()
		mailServer.starttls()
		mailServer.ehlo()
		mailServer.login(self.account.email, password)
		print "Server logged in."
		mailServer.sendmail(self.account.email, message['to'], message.as_string())
		print "Message Sent."
		# Should be mailServer.quit(), but that crashes...
		mailServer.close()
		print "Server closed."


d