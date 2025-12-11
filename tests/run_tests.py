import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from codes.Hopcroft_Karp import main


def run_all_tests():
    print("Début des tests...")

    try:
        # Pavables (doivent renvoyer True)
        assert main("fichiers_test/smallboard.txt", debug_mode=False) == True
        assert main("fichiers_test/tilable1.txt",  debug_mode=False) == True
        assert main("fichiers_test/tilable2.txt",  debug_mode=False) == True
        assert main("fichiers_test/tilable3.txt",  debug_mode=False) == True

        # Non pavables (doivent renvoyer False)
        assert main("fichiers_test/badsmallboard.txt", debug_mode=False) == False
        assert main("fichiers_test/nottilable1.txt",   debug_mode=False) == False
        assert main("fichiers_test/nottilable2.txt",   debug_mode=False) == False

    except AssertionError:
        print("Un test a échoué — regarde la sortie pour identifier lequel.")
        raise
    
    
    print("Tests réussis avec succès ✔")


if __name__ == "__main__":
    run_all_tests()
