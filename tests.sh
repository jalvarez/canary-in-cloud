#!/bin/bash
trial test/test_canary.py
nosetests test/test_clients_repository.py
nosetests test/test_config.py
nosetests test/test_enviroments_repository.py
trial test/test_lambda_handlers.py
trial test/test_listener_miners.py
trial test/test_listener_miners_team.py
trial test/test_results_repository.py
#nosetests test/test_smtp_dispatcher.py
