import unittest
from mock import Mock

import src

class ListenerMinerTeamTests(unittest.TestCase):
	def create_listener_mock(self):
		listener_mock = Mock()
		listener_mock.listen = Mock()
		return listener_mock
		
	def test_when_a_team_is_listen_all_members_listen(self):
		listener_A_mock = self.create_listener_mock()
		listener_B_mock = self.create_listener_mock()
		team = src.ListenerMinerTeam()
		team.add_member(listener_A_mock)
		team.add_member(listener_B_mock)

		team.listen()

		listener_A_mock.listen.assert_any_call()
		listener_B_mock.listen.assert_any_call()

	def test_when_a_team_listener_fail_isolation(self):
		listener_A_mock = self.create_listener_mock()
		listener_A_mock.listen = Mock(side_effect=Exception('something wrong'))
		listener_B_mock = self.create_listener_mock()
		team = src.ListenerMinerTeam()
		team.add_member(listener_A_mock)
		team.add_member(listener_B_mock)

		team.listen()

		listener_B_mock.listen.assert_any_call()

