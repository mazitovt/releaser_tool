import unittest
from taskcreator import TaskCreator
from jira import RepositoryBranch


class BranchMatcher:
    branch: RepositoryBranch

    def __init__(self, branch):
        self._branch = branch

    def __eq__(self, other):
        return (
            self._branch._repository_name == other.self._repository_name
            and self._branch._name == other._name
        )


class TestTaskCreator(unittest.TestCase):

    task_name_test_cases = (
        (["PROMEDWEB-12345", "", ""], "PROMEDWEB-12345"),
        (
            ["PROMEDWEB-000000000000000000000000000000000000", "", ""],
            "PROMEDWEB-000000000000000000000000000000000000",
        ),
        (["PROMED-12345", "", ""], "PROMED-12345"),
        (["PROMEDWEB-1", "", ""], "PROMEDWEB-1"),
        (["P-12345", "", ""], "P-12345"),
        (["-12345", "", ""], Exception),
        (["p-12345", "", ""], Exception),
        (["PROMEDWEB-*", "", ""], Exception),
        (["PROMEDWEB", "", ""], Exception),
        (["PROMEDWEB-", "", ""], Exception),
        (["PROMEDWEB12345", "", ""], Exception),
        (["PROMEDWEb-12345", "", ""], Exception),
        (["PROMEDWEB-A", "", ""], Exception),
        ([" PROMEDWEB-12345 ", "", ""], Exception),
        (["PROMEDWEB", "", ""], Exception),
        (["P", "", ""], Exception),
        (["1", "", ""], Exception),
        (["-", "", ""], Exception),
        ([" ", "", ""], Exception),
        (["", "", ""], Exception),
    )

    templates_test_cases = (
        (["6", "2", "f7_2019_2000.rptdesign"], ["f7_2019_2000.rptdesign"]),
        (["", "", "f7_2019_2000_pg.rptdesign"], ["f7_2019_2000_pg.rptdesign"]),
        (["", "", "58/f7_2019_2000.rptdesign"], ["f7_2019_2000.rptdesign"]),
        (["", "", "f7_2019_2000.rptdesign"], ["f7_2019_2000.rptdesign"]),
        (["", "", "101/f7_2019_2000.rptdesign"], ["f7_2019_2000.rptdesign"]),
        (["", "", "f7_2019_2000.rptdesign"], ["f7_2019_2000.rptdesign"]),
        (["", "", "1/f7_2019_2000.rptdesign"], ["f7_2019_2000.rptdesign"]),
        (["", "", "f7_2019_2000.rptdesign"], ["f7_2019_2000.rptdesign"]),
        (["", "", "1010/f7_2019_2000.rptdesign"], ["f7_2019_2000.rptdesign"]),
        (["", "", "f7_2019_2000.rptdesign"], ["f7_2019_2000.rptdesign"]),
        (
            ["", "", "r19_Registry_Svod_Para.rptdesign"],
            ["r19_Registry_Svod_Para.rptdesign"],
        ),
        (
            ["", "", "r19_Registry_Svod_App_Stom.rptdesign"],
            ["r19_Registry_Svod_App_Stom.rptdesign"],
        ),
        (["", "", "f7_2019_2000.rptdesign"], ["f7_2019_2000.rptdesign"]),
        (["", "", "f.rptdesign"], ["f.rptdesign"]),
        (
            ["", "", "91/r91_Rec_AnalisMedCare_MedService_pg.rptdesign"],
            ["r91_Rec_AnalisMedCare_MedService_pg.rptdesign"],
        ),
        (
            ["", "", "r91_Rec_AnalisMedCare_MedService_pg.rptdesign"],
            ["r91_Rec_AnalisMedCare_MedService_pg.rptdesign"],
        ),
        (
            ["", "", "91/r91_Rec_AnalisMedCare_MedService.rptdesign"],
            ["r91_Rec_AnalisMedCare_MedService.rptdesign"],
        ),
        (
            ["", "", "r91_Rec_AnalisMedCare_MedService.rptdesign"],
            ["r91_Rec_AnalisMedCare_MedService.rptdesign"],
        ),
        (
            ["", "", "f096u20_birthmedcard.rptdesign"],
            ["f096u20_birthmedcard.rptdesign"],
        ),
        (
            ["", "", "f096u20_birthmedcard_pg.rptdesign"],
            ["f096u20_birthmedcard_pg.rptdesign"],
        ),
        (
            ["", "", "pf_096_1y-20_MedCard.rptdesign"],
            ["pf_096_1y-20_MedCard.rptdesign"],
        ),
        (
            ["", "", "pf_096_1y-20_MedCard_pg.rptdesign"],
            ["pf_096_1y-20_MedCard_pg.rptdesign"],
        ),
        (["", "", "/f7_2019_2000.rptdesign"], ["f7_2019_2000.rptdesign"]),
        (["", "", " /f7_2019_2000.rptdesign"], ["f7_2019_2000.rptdesign"]),
        (["", "", "f7_2019_2000.rptdesignn"], "f7_2019_2000.rptdesign"),
        (["", "", "f7_2019_2000.rptdesiign"], Exception),
        (["", "", ""], Exception),
        (["", "", "f7_2019_2000rptdesign"], Exception),
        (["", "", ".rptdesign"], Exception),
    )

    split_on_delimiters_test_cases = (
        (
            [
                "",
                "",
                "45/f7_2019_2000.rptdesign\n101/f7_2019_2000.rptdesign f7_2019_2010.rptdesign;f7_2019_2200.rptdesign,f7_2019_2300.rptdesign",
            ],
            [
                "45/f7_2019_2000.rptdesign",
                "101/f7_2019_2000.rptdesign",
                "f7_2019_2010.rptdesign",
                "f7_2019_2200.rptdesign",
                "f7_2019_2300.rptdesign",
            ],
        ),
        (
            [
                "",
                "",
                "45/f7_2019_2000.rptdesign\n\n101/f7_2019_2000.rptdesign  f7_2019_2010.rptdesign; f7_2019_2200.rptdesign, f7_2019_2300.rptdesign  ",
            ],
            [
                "45/f7_2019_2000.rptdesign",
                "101/f7_2019_2000.rptdesign",
                "f7_2019_2010.rptdesign",
                "f7_2019_2200.rptdesign",
                "f7_2019_2300.rptdesign",
            ],
        ),
        (
            [
                "",
                "",
                "45/f7_2019_2000.rptdesign\n 101/f7_2019_2000.rptdesign ,f7_2019_2010.rptdesign ;f7_2019_2200.rptdesign  f7_2019_2300.rptdesign\n",
            ],
            [
                "45/f7_2019_2000.rptdesign",
                "101/f7_2019_2000.rptdesign",
                "f7_2019_2010.rptdesign",
                "f7_2019_2200.rptdesign",
                "f7_2019_2300.rptdesign",
            ],
        ),
        (
            [
                "",
                "",
                "45/f7_2019_2000.rptdesign\n101/f7_2019_2000.rptdesign\nf7_2019_2010.rptdesign\nf7_2019_2200.rptdesign\nf7_2019_2300.rptdesign\n",
            ],
            [
                "45/f7_2019_2000.rptdesign",
                "101/f7_2019_2000.rptdesign",
                "f7_2019_2010.rptdesign",
                "f7_2019_2200.rptdesign",
                "f7_2019_2300.rptdesign",
            ],
        ),
        (["", "", "45/f7_2019_2000.rptdesign"], ["45/f7_2019_2000.rptdesign"]),
        (["", "", " "], Exception),
        (["", "", ""], Exception),
        (["", "", "\n"], Exception),
        (["", "", ","], Exception),
        (["", "", " \n ; , \n"], Exception),
        (["", "", "\n;, "], Exception),
    )

    get_branches_test_cases = (
        (
            [
                "",
                "https://git.promedweb.ru/rtmis/report_ms/-/tree/PROMEDWEB-27866  https://git.promedweb.ru/rtmis/report_pg/-/tree/PROMEDWEB-28321",
                "",
            ],
            [
                RepositoryBranch(
                    "PROMEDWEB-27866", "https://git.promedweb.ru/rtmis/report_ms"
                ),
                RepositoryBranch(
                    "PROMEDWEB-28321", "https://git.promedweb.ru/rtmis/report_pg"
                ),
            ],
        ),
        (
            ["", "https://git.promedweb.ru/rtmis/report_pg/-/tree/PROMEDWEB-32317", ""],
            [
                RepositoryBranch(
                    "PROMEDWEB-32317", "https://git.promedweb.ru/rtmis/report_pg"
                )
            ],
        ),
        (
            ["", "https://git.promedweb.ru/rtmis/report_pg/-/tree/PROMEDWEB-51417", ""],
            [
                RepositoryBranch(
                    "PROMEDWEB-51417", "https://git.promedweb.ru/rtmis/report_pg"
                )
            ],
        ),
    )

    def test_get_task_name(self):
        for test_input, expected_result in self.task_name_test_cases:
            if expected_result is Exception:
                with self.assertRaises(expected_result):
                    TaskCreator._get_task_name(test_input)
            else:
                self.assertEqual(
                    TaskCreator._get_task_name(test_input), expected_result
                )

    # re.error: look-behind requires fixed-width pattern
    def test_get_templates(self):
        for test_input, expected_result in self.templates_test_cases:
            if expected_result is Exception:
                with self.assertRaises(expected_result):
                    TaskCreator._get_templates(test_input)
            else:
                self.assertEqual(
                    TaskCreator._get_templates(test_input), expected_result
                )

    def test_split_on_delimiters(self):
        for test_input, expected_result in self.split_on_delimiters_test_cases:
            if expected_result is Exception:
                with self.assertRaises(expected_result):
                    TaskCreator._split_on_delimiters(test_input)
            else:
                self.assertEqual(
                    TaskCreator._split_on_delimiters(test_input), expected_result
                )

    # нужен экземпляр класса TaskCreator
    # в тесткейса expected_result должен быть список экземпляров класса RepositoryBranch
    def test_get_branches(self):
        for test_input, expected_result in self.get_branches_test_cases:
            if expected_result is Exception:
                with self.assertRaises(expected_result):
                    TaskCreator()._get_branches(test_input)
            else:
                branches = TaskCreator()._get_branches(test_input)
                branches.sort()
                expected_result.sort()
                for pair in zip(branches, expected_result):
                    self.assertEqual(BranchMatcher(pair[0]), pair[1])


if __name__ == "__main__":
    unittest.main()
