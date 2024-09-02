import timeit as t
from bowling_test import BowlingTest
# Définition d'une fonction à tester
tester = BowlingTest()

# Test de rapidité
num_runs: int = 500000
elapsed_time = t.timeit(tester.test_all_strikes_is_a_perfect_game,number=num_runs)
print(f"Temps moyen pour {num_runs}: {elapsed_time:.6f} secondes")