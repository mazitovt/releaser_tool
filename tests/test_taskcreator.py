import unittest
from taskcreator import TaskCreator
from regex_patterns import match_template_pattern, split_on_delimiters


class TestTaskCreator(unittest.TestCase):
    """
    Тестирвоание статических методов класса TaskCreator:
        _get_task_name, _get_templates, _get_branches
    """

    # Словари использовались в закоментированнных методах
    # Закоментированные методы были заменены одиночными методами

    task_name_test_cases = (
        ("PROMEDWEB-12345", "PROMEDWEB-12345"),
        (
            "PROMEDWEB-000000000000000000000000000000000000",
            "PROMEDWEB-000000000000000000000000000000000000",
        ),
        # TODO: правильное название или это исключение?
        (" PROMEDWEB-12345 ", Exception),
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
        ("f7_2019_2000.rptdesignn", ["f7_2019_2000.rptdesign"]),
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
        (" \r\n;, ", Exception),
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

    match_template_pattern = {}

    # def test_get_task_name(self):
    #     print(len(self.task_name_test_cases))
    #     # index = 0
    #     for test_input, expected_result in self.task_name_test_cases:
    #         if expected_result is Exception:
    #             # print(
    #             #     f"def test_get_task_name_{index}(self):\n\twith self.assertRaises({expected_result.__name__}):\n\t\tTaskCreator._get_task_name(\"{test_input}\")")
    #             # index += 1
    #             with self.assertRaises(expected_result):
    #                 TaskCreator._get_task_name(test_input)
    #
    #         else:
    #             # print(
    #             #     f"def test_get_task_name_{index}(self):\n\tself.assertEqual(TaskCreator._get_task_name(\"{test_input}\"), \"{expected_result}\")")
    #             # index += 1
    #             self.assertEqual(
    #                 TaskCreator._get_task_name(test_input), expected_result
    #             )

    # Для выполенения тест нужно исправить выражение
    # r"(?<=(\d{1,3}/)?)[a-zA-Z_0-9]+\.rptdesign"
    # re.error: look-behind requires fixed-width pattern
    # def test_get_templates(self):
    #     index = 1
    #     for test_input, expected_result in self.templates_test_cases:
    #         if expected_result is Exception:
    #             print(f'def test_get_templates_{index}(self):\n\twith self.assertRaises({expected_result.__name__}):\n\t\tTaskCreator._get_templates("{test_input}")'
    #                         )
    #             index += 1
    #             with self.assertRaises(expected_result):
    #                 TaskCreator._get_templates(test_input)
    #         else:
    #             print(
    #                 f'def test_split_on_delimiters_{index}(self):\n\tself.assertEqual(TaskCreator._get_templates("{test_input}"), {expected_result})'
    #             )
    #             index += 1
    #             self.assertEqual(
    #                 TaskCreator._get_templates(test_input), expected_result
    #             )

    # def test_split_on_delimiters(self):
    #     index = 0
    #     for test_input, expected_result in self.split_on_delimiters_test_cases:
    #         if expected_result is Exception:
    #             print(
    #                 f'def test_split_on_delimiters_{index}(self):\n\twith self.assertRaises({expected_result.__name__}):\n\t\tTaskCreator._split_on_delimiters("{test_input}")'
    #             )
    #             index += 1
    #             with self.assertRaises(expected_result):
    #                 TaskCreator._split_on_delimiters(test_input)
    #         else:
    #             print(
    #                 f'def test_split_on_delimiters_{index}(self):\n\tself.assertEqual(TaskCreator._split_on_delimiters("{test_input}"), "{expected_result}")'
    #             )
    #             index += 1
    #             self.assertEqual(
    #                 TaskCreator._split_on_delimiters(test_input), expected_result
    #             )

    # def test_get_branches(self):
    #     index = 0
    #     for test_input, expected_result in self.get_branches_test_cases:
    #         if expected_result is Exception:
    #             print(
    #                 f'def test_get_branches_{index}(self):\n\twith self.assertRaises({expected_result.__name__}):\n\t\tTaskCreator._get_branches("{test_input}")'
    #             )
    #             index += 1
    #             with self.assertRaises(expected_result):
    #                 TaskCreator._get_branches(test_input)
    #         else:
    #             print(
    #                 f'def test_get_branches_{index}(self):\n\tfor pair in zip(TaskCreator._get_branches(\"{test_input}\"), {expected_result}):'
    #             )
    #             index += 1
    #             for pair in zip(TaskCreator._get_branches(test_input), expected_result):
    #                 print(f'\t\tself.assertEqual((pair[0]._name, pair[0]._repository_name), {pair[1]})')
    #                 self.assertEqual((pair[0]._name, pair[0]._repository_name), pair[1])

    # ======= Start of testing _get_task_name # =======

    def test_get_task_name_01(self):
        self.assertEqual(
            TaskCreator._get_task_name("PROMEDWEB-12345"), "PROMEDWEB-12345"
        )

    def test_get_task_name_02(self):
        with self.assertRaises(Exception):
            TaskCreator._get_task_name(" PROMEDWEB-12345 ")

    def test_get_task_name_03(self):
        self.assertEqual(TaskCreator._get_task_name("PROMED-12345"), "PROMED-12345")

    def test_get_task_name_04(self):
        self.assertEqual(TaskCreator._get_task_name("PROMEDWEB-1"), "PROMEDWEB-1")

    def test_get_task_name_05(self):
        self.assertEqual(TaskCreator._get_task_name("P-12345"), "P-12345")

    def test_get_task_name_06(self):
        with self.assertRaises(Exception):
            TaskCreator._get_task_name("-12345")

    def test_get_task_name_07(self):
        with self.assertRaises(Exception):
            TaskCreator._get_task_name("p-12345")

    def test_get_task_name_08(self):
        with self.assertRaises(Exception):
            TaskCreator._get_task_name("PROMEDWEB-*")

    def test_get_task_name_09(self):
        with self.assertRaises(Exception):
            TaskCreator._get_task_name("PROMEDWEB")

    def test_get_task_name_10(self):
        with self.assertRaises(Exception):
            TaskCreator._get_task_name("PROMEDWEB-")

    def test_get_task_name_11(self):
        with self.assertRaises(Exception):
            TaskCreator._get_task_name("PROMEDWEB12345")

    def test_get_task_name_12(self):
        with self.assertRaises(Exception):
            TaskCreator._get_task_name("PROMEDWEb-12345")

    def test_get_task_name_13(self):
        with self.assertRaises(Exception):
            TaskCreator._get_task_name("PROMEDWEB-A")

    def test_get_task_name_14(self):
        with self.assertRaises(Exception):
            TaskCreator._get_task_name("PROMEDWEB")

    def test_get_task_name_15(self):
        with self.assertRaises(Exception):
            TaskCreator._get_task_name("P")

    def test_get_task_name_16(self):
        with self.assertRaises(Exception):
            TaskCreator._get_task_name("1")

    def test_get_task_name_17(self):
        with self.assertRaises(Exception):
            TaskCreator._get_task_name("-")

    def test_get_task_name_18(self):
        with self.assertRaises(Exception):
            TaskCreator._get_task_name(" ")

    def test_get_task_name_19(self):
        with self.assertRaises(Exception):
            TaskCreator._get_task_name("")

    # ======= End of testing _get_task_name # =======

    # ======= Start of testing _get_templates # =======

    def test_get_templates_01(self):
        self.assertEqual(
            TaskCreator._get_templates("f7_2019_2000.rptdesign"),
            ["f7_2019_2000.rptdesign"],
        )

    def test_get_templates_02(self):
        self.assertEqual(
            TaskCreator._get_templates("f7_2019_2000_pg.rptdesign"),
            ["f7_2019_2000_pg.rptdesign"],
        )

    def test_get_templates_03(self):
        self.assertEqual(
            TaskCreator._get_templates("58/f7_2019_2000.rptdesign"),
            ["f7_2019_2000.rptdesign"],
        )

    def test_get_templates_04(self):
        self.assertEqual(
            TaskCreator._get_templates("f7_2019_2000.rptdesign"),
            ["f7_2019_2000.rptdesign"],
        )

    def test_get_templates_05(self):
        self.assertEqual(
            TaskCreator._get_templates("101/f7_2019_2000.rptdesign"),
            ["f7_2019_2000.rptdesign"],
        )

    def test_get_templates_06(self):
        self.assertEqual(
            TaskCreator._get_templates("f7_2019_2000.rptdesign"),
            ["f7_2019_2000.rptdesign"],
        )

    def test_get_templates_07(self):
        self.assertEqual(
            TaskCreator._get_templates("1/f7_2019_2000.rptdesign"),
            ["f7_2019_2000.rptdesign"],
        )

    def test_get_templates_08(self):
        self.assertEqual(
            TaskCreator._get_templates("f7_2019_2000.rptdesign"),
            ["f7_2019_2000.rptdesign"],
        )

    def test_get_templates_09(self):
        with self.assertRaises(Exception):
            self.assertEqual(
                TaskCreator._get_templates("1010/f7_2019_2000.rptdesign"),
                ["f7_2019_2000.rptdesign"],
            )

    def test_get_templates_10(self):
        self.assertEqual(
            TaskCreator._get_templates("f7_2019_2000.rptdesign"),
            ["f7_2019_2000.rptdesign"],
        )

    def test_get_templates_11(self):
        self.assertEqual(
            TaskCreator._get_templates("r19_Registry_Svod_Para.rptdesign"),
            ["r19_Registry_Svod_Para.rptdesign"],
        )

    def test_get_templates_12(self):
        self.assertEqual(
            TaskCreator._get_templates("r19_Registry_Svod_App_Stom.rptdesign"),
            ["r19_Registry_Svod_App_Stom.rptdesign"],
        )

    def test_get_templates_13(self):
        self.assertEqual(
            TaskCreator._get_templates("f7_2019_2000.rptdesign"),
            ["f7_2019_2000.rptdesign"],
        )

    def test_get_templates_14(self):
        self.assertEqual(TaskCreator._get_templates("f.rptdesign"), ["f.rptdesign"])

    def test_get_templates_15(self):
        self.assertEqual(
            TaskCreator._get_templates(
                "91/r91_Rec_AnalisMedCare_MedService_pg.rptdesign"
            ),
            ["r91_Rec_AnalisMedCare_MedService_pg.rptdesign"],
        )

    def test_get_templates_16(self):
        self.assertEqual(
            TaskCreator._get_templates("r91_Rec_AnalisMedCare_MedService_pg.rptdesign"),
            ["r91_Rec_AnalisMedCare_MedService_pg.rptdesign"],
        )

    def test_get_templates_17(self):
        self.assertEqual(
            TaskCreator._get_templates("91/r91_Rec_AnalisMedCare_MedService.rptdesign"),
            ["r91_Rec_AnalisMedCare_MedService.rptdesign"],
        )

    def test_get_templates_18(self):
        self.assertEqual(
            TaskCreator._get_templates("r91_Rec_AnalisMedCare_MedService.rptdesign"),
            ["r91_Rec_AnalisMedCare_MedService.rptdesign"],
        )

    def test_get_templates_19(self):
        self.assertEqual(
            TaskCreator._get_templates("f096u20_birthmedcard.rptdesign"),
            ["f096u20_birthmedcard.rptdesign"],
        )

    def test_get_templates_20(self):
        self.assertEqual(
            TaskCreator._get_templates("f096u20_birthmedcard_pg.rptdesign"),
            ["f096u20_birthmedcard_pg.rptdesign"],
        )

    def test_get_templates_21(self):
        self.assertEqual(
            TaskCreator._get_templates("pf_096_1y-20_MedCard.rptdesign"),
            ["pf_096_1y-20_MedCard.rptdesign"],
        )

    def test_get_templates_22(self):
        self.assertEqual(
            TaskCreator._get_templates("pf_096_1y-20_MedCard_pg.rptdesign"),
            ["pf_096_1y-20_MedCard_pg.rptdesign"],
        )

    def test_get_templates_23(self):
        with self.assertRaises(Exception):
            TaskCreator._get_templates("/f7_2019_2000.rptdesign")

    def test_get_templates_24(self):
        with self.assertRaises(Exception):
            TaskCreator._get_templates(" /f7_2019_2000.rptdesign")

    def test_get_templates_25(self):
        with self.assertRaises(Exception):
            TaskCreator._get_templates("f7_2019_2000.rptdesignn")

    def test_get_templates_26(self):
        with self.assertRaises(Exception):
            TaskCreator._get_templates("f7_2019_2000.rptdesiign")

    def test_get_templates_27(self):
        self.assertEqual(TaskCreator._get_templates(""), [])

    def test_get_templates_28(self):
        with self.assertRaises(Exception):
            TaskCreator._get_templates("f7_2019_2000rptdesign")

    def test_get_templates_29(self):
        with self.assertRaises(Exception):
            TaskCreator._get_templates(".rptdesign")

    # ======= End of testing _get_templates # =======

    # ======= Start of testing _get_branches # =======

    def test_get_branches_01(self):
        branches = TaskCreator._get_branches(
            "https://git.promedweb.ru/rtmis/report_ms/-/tree/PROMEDWEB-27866\r\nhttps://git.promedweb.ru/rtmis/report_pg/-/tree/PROMEDWEB-28321"
        )
        self.assertEqual(
            (branches[0]._name, branches[0]._repository_name),
            ("PROMEDWEB-27866", "report_ms"),
        )
        self.assertEqual(
            (branches[1]._name, branches[1]._repository_name),
            ("PROMEDWEB-28321", "report_pg"),
        )

    def test_get_branches_02(self):
        branches = TaskCreator._get_branches(
            "https://git.promedweb.ru/rtmis/report_ms/-/tree/PROMEDWEB-27866  https://git.promedweb.ru/rtmis/report_pg/-/tree/PROMEDWEB-28321"
        )
        self.assertEqual(
            (branches[0]._name, branches[0]._repository_name),
            ("PROMEDWEB-27866", "report_ms"),
        )
        self.assertEqual(
            (branches[1]._name, branches[1]._repository_name),
            ("PROMEDWEB-28321", "report_pg"),
        )

    def test_get_branches_03(self):
        branches = TaskCreator._get_branches(
            "https://git.promedweb.ru/rtmis/report_pg/-/tree/PROMEDWEB-32317"
        )
        self.assertEqual(
            (branches[0]._name, branches[0]._repository_name),
            ("PROMEDWEB-32317", "report_pg"),
        )

    def test_get_branches_04(self):
        branches = TaskCreator._get_branches(
            "https://git.promedweb.ru/rtmis/report_pg/-/tree/PROMEDWEB-51417"
        )
        self.assertEqual(
            (branches[0]._name, branches[0]._repository_name),
            ("PROMEDWEB-51417", "report_pg"),
        )

    def test_get_branches_05(self):
        with self.assertRaises(Exception):
            TaskCreator._get_branches("/-/tree/PROMEDWEB-51417")

    # ======= End of testing _get_branches # =======


class TestRegexPatterns(unittest.TestCase):
    """
    Тестирование функций с ругулярными выражениями:
        split_on_delimiters, match_template_pattern
    """

    # ======= Start of testing _split_on_delimiters # =======

    def test_split_on_delimiters_01(self):
        self.assertEqual(
            split_on_delimiters(
                "45/f7_2019_2000.rptdesign\n101/f7_2019_2000.rptdesign f7_2019_2010.rptdesign;f7_2019_2200.rptdesign,f7_2019_2300.rptdesign"
            ),
            [
                "45/f7_2019_2000.rptdesign",
                "101/f7_2019_2000.rptdesign",
                "f7_2019_2010.rptdesign",
                "f7_2019_2200.rptdesign",
                "f7_2019_2300.rptdesign",
            ],
        )

    def test_split_on_delimiters_02(self):
        self.assertEqual(
            split_on_delimiters(
                "45/f7_2019_2000.rptdesign\n\n101/f7_2019_2000.rptdesign  f7_2019_2010.rptdesign; f7_2019_2200.rptdesign, f7_2019_2300.rptdesign  "
            ),
            [
                "45/f7_2019_2000.rptdesign",
                "101/f7_2019_2000.rptdesign",
                "f7_2019_2010.rptdesign",
                "f7_2019_2200.rptdesign",
                "f7_2019_2300.rptdesign",
            ],
        )

    def test_split_on_delimiters_03(self):
        self.assertEqual(
            split_on_delimiters(
                "45/f7_2019_2000.rptdesign\n 101/f7_2019_2000.rptdesign ,f7_2019_2010.rptdesign ;f7_2019_2200.rptdesign  f7_2019_2300.rptdesign\n"
            ),
            [
                "45/f7_2019_2000.rptdesign",
                "101/f7_2019_2000.rptdesign",
                "f7_2019_2010.rptdesign",
                "f7_2019_2200.rptdesign",
                "f7_2019_2300.rptdesign",
            ],
        )

    def test_split_on_delimiters_04(self):
        self.assertEqual(
            split_on_delimiters(
                "45/f7_2019_2000.rptdesign\r\n101/f7_2019_2000.rptdesign\r\nf7_2019_2010.rptdesign\r\nf7_2019_2200.rptdesign\nf7_2019_2300.rptdesign\r\n"
            ),
            [
                "45/f7_2019_2000.rptdesign",
                "101/f7_2019_2000.rptdesign",
                "f7_2019_2010.rptdesign",
                "f7_2019_2200.rptdesign",
                "f7_2019_2300.rptdesign",
            ],
        )

    def test_split_on_delimiters_05(self):
        self.assertEqual(
            split_on_delimiters("45/f7_2019_2000.rptdesign"),
            ["45/f7_2019_2000.rptdesign"],
        )

    def test_split_on_delimiters_06(self):
        with self.assertRaises(Exception):
            split_on_delimiters(" ")

    def test_split_on_delimiters_07(self):
        with self.assertRaises(Exception):
            split_on_delimiters("\n")

    def test_split_on_delimiters_08(self):
        with self.assertRaises(Exception):
            split_on_delimiters(",")

    def test_split_on_delimiters_09(self):
        with self.assertRaises(Exception):
            split_on_delimiters(" \n ; ,\r\n")

    def test_split_on_delimiters_10(self):
        with self.assertRaises(Exception):
            split_on_delimiters("\n;, ")

    def test_split_on_delimiters_11(self):
        with self.assertRaises(Exception):
            split_on_delimiters(" \r\n;, ")

    def test_split_on_delimiters_12(self):
        with self.assertRaises(Exception):
            split_on_delimiters("")

    # ======= End of testing _split_on_delimiters # ========

    # ======= Start of testing match_template_pattern # =======

    def test_match_template_pattern_01(self):
        self.assertEqual(
            match_template_pattern("f7_2019_2000.rptdesign"), "f7_2019_2000.rptdesign"
        )

    def test_match_template_pattern_02(self):
        self.assertEqual(
            match_template_pattern("1/f7_2019_2000.rptdesign"), "f7_2019_2000.rptdesign"
        )

    def test_match_template_pattern_03(self):
        self.assertEqual(
            match_template_pattern("58/f7_2019_2000.rptdesign"),
            "f7_2019_2000.rptdesign",
        )

    def test_match_template_pattern_04(self):
        self.assertEqual(
            match_template_pattern("101/f7_2019_2000.rptdesign"),
            "f7_2019_2000.rptdesign",
        )

    def test_match_template_pattern_05(self):
        with self.assertRaises(Exception):
            match_template_pattern("1010/f7_2019_2000.rptdesign")

    def test_match_template_pattern_06(self):
        with self.assertRaises(Exception):
            match_template_pattern("/f7_2019_2000.rptdesign")

    # ======= End of testing match_template_pattern # =======


if __name__ == "__main__":
    unittest.main()
