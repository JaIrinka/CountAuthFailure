from unittest import mock, TestCase
from CountAuthFailure import count_auth_failure 

class CountAuthFailureTest(TestCase):

    @mock.patch('CountAuthFailure.time', return_value=4000)
    def test_count_auth_failure(self, time_mock):
        """count_auth_failure Test"""
        journal = mock.Mock()
        journal.__iter__ = mock.Mock(return_value=iter([
            {'MESSAGE': 'user: Executing command'}, 
            {'MESSAGE': 'Registered Authentication Agent for unix-session:1'},
            {'MESSAGE': 'pam_unix(gdm-password:auth): authentication failure; logname='}
        ]))

        with mock.patch('CountAuthFailure.Reader', return_value=journal):
            self.assertEqual(
                count_auth_failure(),
                1
            )
            journal.add_match.assert_called_once_with("SYSLOG_FACILITY=10", "PRIORITY=5")
            journal.seek_realtime.assert_called_once_with(400)
        
if __name__ == '__main__':
    unittest.main()