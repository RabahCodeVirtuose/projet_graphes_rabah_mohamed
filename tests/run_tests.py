import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from codes.Hopcroft_Karp import main


def run_all_tests():
    print("Début des tests...")

    try:
        # Pavables (doivent renvoyer True)
        assert main("fichiers_test/smallboard.txt") == True
        assert main("fichiers_test/tilable1.txt") == True
        assert main("fichiers_test/tilable2.txt") == True
        assert main("fichiers_test/tilable3.txt") == True

        # Non pavables (doivent renvoyer False)
        assert main("fichiers_test/badsmallboard.txt") == False
        assert main("fichiers_test/nottilable1.txt") == False
        assert main("fichiers_test/nottilable2.txt") == False

    except AssertionError:
        print("Un test a échoué — regarde la sortie pour identifier lequel.")
        raise
    
    
    print("Tests réussis avec succès ✔")


if __name__ == "__main__":
    run_all_tests()
