# 2x2 grid, no food
python ../src/simulator.py ../test/initial_state_01.txt 0 N
python ../src/simulator.py ../test/initial_state_02.txt 0 S
python ../src/simulator.py ../test/initial_state_03.txt 0 E
python ../src/simulator.py ../test/initial_state_04.txt 0 W
python ../src/simulator.py ../test/initial_state_05.txt 0 N
python ../src/simulator.py ../test/initial_state_06.txt 0 S
python ../src/simulator.py ../test/initial_state_07.txt 0 E
python ../src/simulator.py ../test/initial_state_08.txt 0 W
# 2x2 grid, food
python ../src/simulator.py ../test/initial_state_09.txt 1 N
python ../src/simulator.py ../test/initial_state_10.txt 1 E
python ../src/simulator.py ../test/initial_state_11.txt 1 N
python ../src/simulator.py ../test/initial_state_12.txt 1 S
# 2x2 grid with obstacles, food
python ../src/simulator.py ../test/initial_state_13.txt 1 N
python ../src/simulator.py ../test/initial_state_14.txt 1 N
python ../src/simulator.py ../test/initial_state_15.txt 1 W
python ../src/simulator.py ../test/initial_state_16.txt 1 N
# 4x4 grid with obstacles, food and limited time
python ../src/simulator.py ../test/initial_state_17.txt 1 N
python ../src/simulator.py ../test/initial_state_18.txt 1 S
python ../src/simulator.py ../test/initial_state_19.txt 1 E
python ../src/simulator.py ../test/initial_state_20.txt 1 E
# 4x4 grid with obstacles, food and limited time
python ../src/simulator.py ../test/initial_state_21.txt 1 W
python ../src/simulator.py ../test/initial_state_22.txt 1 E
python ../src/simulator.py ../test/initial_state_23.txt 1 E
python ../src/simulator.py ../test/initial_state_24.txt 1 S



