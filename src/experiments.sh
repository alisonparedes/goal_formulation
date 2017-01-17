python ./src/agent.py test/tiny_01.txt test/tiny_01.txt 10 10 1 10
python ./src/agent.py test/go_to_base_4x4.txt test/go_to_base_4x4.txt 10 10 0 10
python ./src/agent.py test/go_to_food_4x4.txt test/go_to_food_4x4.txt 10 10 0 20
python ./src/agent.py test/hidden_food_4x4_real.txt test/hidden_food_4x4_belief.txt 10 10 0 20
python ./src/agent.py test/hidden_food_4x4_real.txt test/hidden_food_4x4_belief.txt 10 1 2 20
python ./src/agent.py test/blocked_4x1_real.txt test/blocked_4x1_belief.txt 10 10 0 10
python ./src/agent.py test/scenario_01_4x4_01_real.txt test/scenario_01_4x4_01_belief.txt 10 2 2 100
python ./src/agent.py test/scenario_02_4x4_01_real.txt test/scenario_02_4x4_01_belief.txt 100 100 2 100