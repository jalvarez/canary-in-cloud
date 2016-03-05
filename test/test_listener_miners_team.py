import unittest
from mock import Mock

import src

class ListenerMinerTeamTests(unittest.TestCase):
    def setUp(self):
        self.callback_mock = Mock()
        self.cage = [self._create_canary_mock()]

    def _create_listener_mock(self):
        listener_mock = Mock()
        listener_mock.listen = Mock(side_effect=[])
        return listener_mock

    def _create_canary_mock(self):
        canary_mock = Mock()
        canary_mock.check_and_register = Mock()
        return canary_mock
        
    def test_when_a_team_is_listen_all_members_listen(self):
        listener_A_mock = self._create_listener_mock()
        listener_B_mock = self._create_listener_mock()
        team = src.ListenerMinerTeam()
        team.add_member(listener_A_mock)
        team.add_member(listener_B_mock)

        team.listen(self.cage, self.callback_mock)

        listener_A_mock.listen.assert_called_with(self.cage, self.callback_mock)
        listener_B_mock.listen.assert_called_with(self.cage, self.callback_mock)

    def test_when_a_team_listener_fail_isolation(self):
        listener_A_mock = self._create_listener_mock()
        listener_A_mock.listen = Mock(side_effect=Exception('something wrong'))
        listener_B_mock = self._create_listener_mock()
        team = src.ListenerMinerTeam()
        team.add_member(listener_A_mock)
        team.add_member(listener_B_mock)

        team.listen(self.cage, self.callback_mock)

        listener_B_mock.listen.assert_called_with(self.cage, self.callback_mock)
