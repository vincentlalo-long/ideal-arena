"""Unit tests for Problem Domain and Registry."""

import unittest

from ideal_arena.core.base import ProblemDomain
from ideal_arena.core.registry import get_problem, list_domains, list_problems


class TestRegistry(unittest.TestCase):
    def test_domains_list(self):
        domains = list_domains()
        self.assertIn(ProblemDomain.GAME_THEORY, domains)
        self.assertIn(ProblemDomain.OPTIMIZATION, domains)
        self.assertIn(ProblemDomain.SIMULATION, domains)

    def test_registered_problems(self):
        problems = list_problems()
        self.assertGreaterEqual(len(problems), 1)
        axelrod = get_problem("axelrod")
        self.assertEqual(axelrod.problem_id, "axelrod")
        self.assertEqual(axelrod.domain, ProblemDomain.GAME_THEORY)
        baselines = axelrod.get_baselines()
        self.assertEqual(len(baselines), 9)


if __name__ == "__main__":
    unittest.main()
