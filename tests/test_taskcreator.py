import unittest
from taskcreator import TaskCreator
from jira_classes.jira import RepositoryBranch


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
        ("PROMEDWEB-12345", "PROMEDWEB-12345"),
        (
            "PROMEDWEB-000000000000000000000000000000000000",
            "PROMEDWEB-000000000000000000000000000000000000",
        ),
        ("PROMED-12345", "PROMED-12345"),
        ("PROMEDWEB-1", "PROMEDWEB-1"),
        ("P-12345", "P-12345"),
        ("-12345", Exception),
        ("p-12345", Exception),
        ("PROMEDWEB-*", Exception),
        ("PROMEDWEB", Exception),
        ("PROMEDWEB-", Exception),
        ("PROMEDWEB12345", Exception),
        ("PROMEDWEb-12345", Exception),
        ("PROMEDWEB-A", Exception),
        (" PROMEDWEB-12345 ", Exception),
        ("PROMEDWEB", Exception),
        ("P", Exception),
        ("1", Exception),
        ("-", Exception),
        (" ", Exception),
        ("", Exception),
    )

    templates_test_cases = (
        ("f7_2019_2000.rptdesign", ["f7_2019_2000.rptdesign"]),
        ("f7_2019_2000_pg.rptdesign", ["f7_2019_2000_pg.rptdesign"]),
        ("58/f7_2019_2000.rptdesign", ["f7_2019_2000.rptdesign"]),
        ("f7_2019_2000.rptdesign", ["f7_2019_2000.rptdesign"]),
        ("101/f7_2019_2000.rptdesign", ["f7_2019_2000.rptdesign"]),
        ("f7_2019_2000.rptdesign", ["f7_2019_2000.rptdesign"]),
        ("1/f7_2019_2000.rptdesign", ["f7_2019_2000.rptdesign"]),
        ("f7_2019_2000.rptdesign", ["f7_2019_2000.rptdesign"]),
        ("1010/f7_2019_2000.rptdesign", ["f7_2019_2000.rptdesign"]),
        ("f7_2019_2000.rptdesign", ["f7_2019_2000.rptdesign"]),
        (
            "r19_Registry_Svod_Para.rptdesign",
            ["r19_Registry_Svod_Para.rptdesign"],
        ),
        (
            "r19_Registry_Svod_App_Stom.rptdesign",
            ["r19_Registry_Svod_App_Stom.rptdesign"],
        ),
        ("f7_2019_2000.rptdesign", ["f7_2019_2000.rptdesign"]),
        ("f.rptdesign", ["f.rptdesign"]),
        (
            "91/r91_Rec_AnalisMedCare_MedService_pg.rptdesign",
            ["r91_Rec_AnalisMedCare_MedService_pg.rptdesign"],
        ),
        (
            "r91_Rec_AnalisMedCare_MedService_pg.rptdesign",
            ["r91_Rec_AnalisMedCare_MedService_pg.rptdesign"],
        ),
        (
            "91/r91_Rec_AnalisMedCare_MedService.rptdesign",
            ["r91_Rec_AnalisMedCare_MedService.rptdesign"],
        ),
        (
            "r91_Rec_AnalisMedCare_MedService.rptdesign",
            ["r91_Rec_AnalisMedCare_MedService.rptdesign"],
        ),
        (
            "f096u20_birthmedcard.rptdesign",
            ["f096u20_birthmedcard.rptdesign"],
        ),
        (
            "f096u20_birthmedcard_pg.rptdesign",
            ["f096u20_birthmedcard_pg.rptdesign"],
        ),
        (
            "pf_096_1y-20_MedCard.rptdesign",
            ["pf_096_1y-20_MedCard.rptdesign"],
        ),
        (
            "pf_096_1y-20_MedCard_pg.rptdesign",
            ["pf_096_1y-20_MedCard_pg.rptdesign"],
        ),
        ("/f7_2019_2000.rptdesign", ["f7_2019_2000.rptdesign"]),
        (" /f7_2019_2000.rptdesign", ["f7_2019_2000.rptdesign"]),
        ("f7_2019_2000.rptdesignn", "f7_2019_2000.rptdesign"),
        ("f7_2019_2000.rptdesiign", Exception),
        ("", Exception),
        ("f7_2019_2000rptdesign", Exception),
        (".rptdesign", Exception),
    )

    split_on_delimiters_test_cases = (
        (
            "45/f7_2019_2000.rptdesign\n101/f7_2019_2000.rptdesign f7_2019_2010.rptdesign;f7_2019_2200.rptdesign,f7_2019_2300.rptdesign",
            [
                "45/f7_2019_2000.rptdesign",
                "101/f7_2019_2000.rptdesign",
                "f7_2019_2010.rptdesign",
                "f7_2019_2200.rptdesign",
                "f7_2019_2300.rptdesign",
            ],
        ),
        (
            "45/f7_2019_2000.rptdesign\n\n101/f7_2019_2000.rptdesign  f7_2019_2010.rptdesign; f7_2019_2200.rptdesign, f7_2019_2300.rptdesign  ",
            [
                "45/f7_2019_2000.rptdesign",
                "101/f7_2019_2000.rptdesign",
                "f7_2019_2010.rptdesign",
                "f7_2019_2200.rptdesign",
                "f7_2019_2300.rptdesign",
            ],
        ),
        (
            "45/f7_2019_2000.rptdesign\n 101/f7_2019_2000.rptdesign ,f7_2019_2010.rptdesign ;f7_2019_2200.rptdesign  f7_2019_2300.rptdesign\n",
            [
                "45/f7_2019_2000.rptdesign",
                "101/f7_2019_2000.rptdesign",
                "f7_2019_2010.rptdesign",
                "f7_2019_2200.rptdesign",
                "f7_2019_2300.rptdesign",
            ],
        ),
        (
            "45/f7_2019_2000.rptdesign\r\n101/f7_2019_2000.rptdesign\r\nf7_2019_2010.rptdesign\r\nf7_2019_2200.rptdesign\nf7_2019_2300.rptdesign\r\n",
            [
                "45/f7_2019_2000.rptdesign",
                "101/f7_2019_2000.rptdesign",
                "f7_2019_2010.rptdesign",
                "f7_2019_2200.rptdesign",
                "f7_2019_2300.rptdesign",
            ],
        ),
        ("45/f7_2019_2000.rptdesign", ["45/f7_2019_2000.rptdesign"]),
        (" ", Exception),
        ("", Exception),
        ("\n", Exception),
        (",", Exception),
        (" \n ; , \n", Exception),
        ("\n;, ", Exception),
    )

    get_branches_test_cases = (
        (
            "https://git.promedweb.ru/rtmis/report_ms/-/tree/PROMEDWEB-27866\r\nhttps://git.promedweb.ru/rtmis/report_pg/-/tree/PROMEDWEB-28321",
            [
                ("PROMEDWEB-27866", "report_ms"),
                ("PROMEDWEB-28321", "report_pg"),
            ],
        ),
        (
            "https://git.promedweb.ru/rtmis/report_ms/-/tree/PROMEDWEB-27866  https://git.promedweb.ru/rtmis/report_pg/-/tree/PROMEDWEB-28321",
            [
                ("PROMEDWEB-27866", "report_ms"),
                ("PROMEDWEB-28321", "report_pg"),
            ],
        ),
        (
            "https://git.promedweb.ru/rtmis/report_pg/-/tree/PROMEDWEB-32317",
            [("PROMEDWEB-32317", "report_pg")],
        ),
        (
            "https://git.promedweb.ru/rtmis/report_pg/-/tree/PROMEDWEB-51417",
            [("PROMEDWEB-51417", "report_pg")],
        ),
        ("/-/tree/PROMEDWEB-51417", Exception),
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

    # Для выполенения тест нужно исправить выражение
    # r"(?<=(\d{1,3}/)?)[a-zA-Z_0-9]+\.rptdesign"
    # re.error: look-behind requires fixed-width pattern
    # def test_get_templates(self):
    #     for test_input, expected_result in self.templates_test_cases:
    #         if expected_result is Exception:
    #             with self.assertRaises(expected_result):
    #                 TaskCreator._get_templates(test_input[2])
    #         else:
    #             self.assertEqual(
    #                 TaskCreator._get_templates(test_input[2]), expected_result[2]
    #             )

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
                    TaskCreator._get_branches(test_input)
            else:
                branches = TaskCreator._get_branches(test_input)
                for pair in zip(branches, expected_result):
                    self.assertEqual((pair[0]._name, pair[0]._repository_name), pair[1])

    # def test_get_branches_simple(self):


if __name__ == "__main__":
    unittest.main()
