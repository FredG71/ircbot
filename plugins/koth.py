import logging
log = logging.getLogger(__name__)

import collections

import ircbot.plugin


class KothPlugin(ircbot.plugin.Plugin):
	def __init__(self, bot, channel):
		super().__init__(bot, channel)
		self.is_active = False
		self.signups_open = False
		self.queue = None

	@ircbot.plugin.command('koth')
	def cmd(self, cmd):
		if not cmd.args or cmd.args[0] == 'list':
			return self.list()
		if cmd.user.is_admin:
			if cmd.args[0] == 'start':
				return self.start()
			if cmd.args[0] == 'next':
				return self.next()
			if cmd.args[0] == 'close':
				return self.close()
			if cmd.args[0] == 'end':
				return self.end()
		if cmd.args[0] == 'add':
			return self.add(cmd.user)
		if cmd.args[0] == 'remove':
			return self.remove(cmd.user)

	def start(self):
		if self.is_active:
			return 'King of the hill already active!'

		self.queue = collections.deque()
		self.is_active = True
		self.signups_open = True
		return 'King of the hill started! Type \x02!koth add\x0F to add yourself!'

	def list(self):
		if not self.is_active:
			return 'No king of the hill active! Type \x02!koth start\x0F to start one.'
		if not self.queue:
			return 'Queue is empty!'

		return 'Signed up: ' + ', '.join([user.nick for user in self.queue])

	def next(self):
		if not self.is_active:
			return 'No king of the hill active! Type \x02!koth start\x0F to start one.'
		if not self.queue:
			return 'Queue is empty!'

		user = self.queue.popleft()

		if self.queue:
			return 'First in queue: {} - Next up: {}'.format(user.nick, self.queue[0].nick)

		return 'Last in queue: {} - queue empty!'.format(user.nick)

	def close(self):
		if not self.is_active:
			return 'No king of the hill active!'
		if not self.signups_open:
			return 'Signups have already been closed!'

		self.signups_open = False
		return 'Signups are now closed!'

	def end(self):
		if not self.is_active:
			return 'No king of the hill active! Type \x02!koth start\x0F to start one.'

		self.queue = None
		self.is_active = False
		self.signups_open = False
		return 'King of the hill ended, queue cleared!'

	def add(self, user):
		if not self.is_active:
			return 'No king of the hill active.'
		if not self.signups_open:
			return 'Signups are closed!'
		if user in self.queue:
			return 'You are already in the queue!'

		self.queue.append(user)
		return 'You were added to the queue in position {}!'.format(len(self.queue))

	def remove(self, user):
		if not self.is_active:
			return 'No king of the hill active.'
		if not user in self.queue:
			return 'You are not in the queue!'

		self.queue.remove(user)
		return 'You were removed from the queue!'
