from generators.tests.chi_square import ChiSquareTest
from generators.tests.ks_test import KolmogorovSmirnovTest
from generators.tests.mean_test import MeanTest 
from generators.tests.poker_test import PokerTest
from generators.tests.runs_test import RunsTest
from generators.tests.variance_test import VarianceTest

class TestRunner:
    
    def __init__(self):
        self.chi_test = ChiSquareTest()
        self.ks_test = KolmogorovSmirnovTest()
        self.mean_test = MeanTest()
        self.poker_test = PokerTest()
        self.runs_test = RunsTest()
        self.variance_test = VarianceTest()
    
    def run_all_tests(self, numbers: list[float]) -> dict:
        results = {}

        def safe_run(name, func):
            try:
                results[name] = func()
            except Exception as e:
                results[name] = {"error": str(e), "passed": False}

        safe_run("chi_square", lambda: self.chi_test.test(numbers, 10))
        safe_run("ks_test", lambda: self.ks_test.test(numbers))
        safe_run("mean_test", lambda: self.mean_test.test(numbers))
        safe_run("poker_test", lambda: self.poker_test.test(numbers))
        safe_run("runs_test", lambda: self.runs_test.test(numbers))
        safe_run("variance_test", lambda: self.variance_test.test(numbers))

        return results