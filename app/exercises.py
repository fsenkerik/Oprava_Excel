def _items_from_columns(sheet, rows, columns, key_start, requirements=None):
    items = []
    key_row = key_start
    for row in rows:
        for column in columns:
            cell = f"{column}{row}"
            req = requirements(cell, row, column) if requirements else None
            item = {"cell": cell, "key_row": key_row}
            if req:
                item["formula_requirements"] = req
            items.append(item)
            key_row += 1
    return items


SUM_FN = ["SUM(", "SUMA("]
AVERAGE_FN = ["AVERAGE(", "PRŮMĚR("]
MIN_FN = ["MIN("]
MAX_FN = ["MAX("]
ROUND_FN = ["ROUND(", "ZAOKROUHLIT("]
COUNT_FN = ["COUNT(", "POČET("]
COUNTA_FN = ["COUNTA(", "POČET2("]
COUNTBLANK_FN = ["COUNTBLANK(", "POČET.PRÁZDNÝCH("]
IF_FN = ["IF(", "KDYŽ("]
AND_FN = ["AND(", "A("]
OR_FN = ["OR(", "NEBO("]
COUNTIF_FN = ["COUNTIF(", "COUNTIF("]
SUMIF_FN = ["SUMIF(", "SUMIF("]
LEN_FN = ["LEN(", "DÉLKA("]
LEFT_FN = ["LEFT(", "LEVÝ(", "ZLEVA("]
RIGHT_FN = ["RIGHT(", "PRAVÝ(", "ZPRAVA("]
MID_FN = ["MID(", "ČÁST("]
SEARCH_FN = ["SEARCH(", "HLEDAT(", "NAJÍT("]
UPPER_FN = ["UPPER(", "VELKÁ("]
LOWER_FN = ["LOWER(", "MALÁ("]
CONCATENATE_FN = ["CONCATENATE(", "&"]


def _req(*any_groups, all_tokens=None, round_arg=None):
    requirements = {}
    if all_tokens:
        requirements["all"] = list(all_tokens)
    if any_groups:
        requirements["any"] = [list(group) for group in any_groups]
    if round_arg is not None:
        requirements["round_arg"] = str(round_arg)
    return requirements


def _funkce_items(answer_col, rows, key_start, requirements_by_row):
    return [
        {
            "cell": f"{answer_col}{row}",
            "key_row": key_start + index,
            "formula_requirements": requirements_by_row[row],
        }
        for index, row in enumerate(rows)
    ]


def _funkce_task4_items():
    round_args = {
        9: "1",
        10: "1",
        11: "2",
        12: "-2",
        13: "2",
        14: "1",
        15: "3",
        16: "0",
        17: "3",
        18: "-3",
    }
    return [
        {
            "cell": f"E{row}",
            "key_row": 70 + index,
            "formula_requirements": _req(ROUND_FN, all_tokens=[f"C{row}"], round_arg=arg),
        }
        for index, (row, arg) in enumerate(round_args.items())
    ]


def _funkce_task5_items():
    specs = [
        (19, 90, _req(ROUND_FN, AVERAGE_FN, round_arg="-2")),
        (20, 91, _req(MAX_FN, MIN_FN)),
        (21, 92, _req(ROUND_FN, AVERAGE_FN, round_arg="0")),
        (22, 93, _req(ROUND_FN, MAX_FN, AVERAGE_FN, round_arg="2")),
        (23, 94, _req(ROUND_FN, MIN_FN, AVERAGE_FN, round_arg="0")),
        (24, 95, _req(ROUND_FN, MAX_FN, MIN_FN, round_arg="0")),
    ]
    return [
        {
            "cell": f"H{row}",
            "key_row": key_row,
            "formula_requirements": requirements,
        }
        for row, key_row, requirements in specs
    ]


def _funkce_task6_items():
    specs = [
        (8, 110, _req(SUM_FN)),
        (9, 111, _req(ROUND_FN, AVERAGE_FN, round_arg="0")),
        (10, 112, _req(MAX_FN)),
        (11, 113, _req(MIN_FN)),
        (12, 114, _req(SUM_FN)),
        (13, 115, _req(ROUND_FN, AVERAGE_FN, round_arg="-2")),
        (14, 116, _req(MAX_FN, MIN_FN)),
        (15, 117, _req(ROUND_FN, AVERAGE_FN, round_arg="-1")),
        (16, 118, _req(SUM_FN)),
        (17, 119, _req(ROUND_FN, SUM_FN, round_arg="1")),
    ]
    return [
        {
            "cell": f"J{row}",
            "key_row": key_row,
            "formula_requirements": requirements,
        }
        for row, key_row, requirements in specs
    ]


def _adresace_task2_items():
    items = []
    key_row = 20
    for row in range(10, 18):
        items.append({
            "cell": f"D{row}",
            "key_row": key_row,
            "formula_requirements": {"all": [f"C{row}", "$C$7"]},
        })
        key_row += 1
        items.append({
            "cell": f"E{row}",
            "key_row": key_row,
            "formula_requirements": {"any_all": [[f"D{row}"], ["$C$7"]]},
        })
        key_row += 1
    return items


def _adresace_task3_req(cell, row, column):
    return {"all": ["$C", "$9"]}


def _adresace_task4_req(cell, row, column):
    return {"all": ["$B", "$8"]}


def _adresace_task5_req(cell, row, column):
    return {"all": ["$C", "$8"]}


def _adresace_task6_items():
    items = []
    key_row = 200
    for row in range(11, 19):
        items.append({
            "cell": f"E{row}",
            "key_row": key_row,
            "formula_requirements": {"all": [f"C{row}", f"D{row}"]},
        })
        key_row += 1
        items.append({
            "cell": f"F{row}",
            "key_row": key_row,
            "formula_requirements": {
                "all": ["$C$8"],
                "any_all": [[f"E{row}"], [f"C{row}", f"D{row}"]],
            },
        })
        key_row += 1
        items.append({
            "cell": f"G{row}",
            "key_row": key_row,
            "formula_requirements": {"all": [f"E{row}", f"F{row}"]},
        })
        key_row += 1
    return items


def _logicke_task1_items():
    return [
        {
            "cell": f"D{row}",
            "key_row": 10 + index,
            "formula_requirements": _req(IF_FN, [">=30", ">29"]),
        }
        for index, row in enumerate(range(9, 19))
    ]


def _logicke_task2_items():
    return [
        {
            "cell": f"E{row}",
            "key_row": 20 + index,
            "formula_requirements": _req(IF_FN, [">=10", ">9"]),
        }
        for index, row in enumerate(range(9, 17))
    ]


def _logicke_task3_items():
    req = _req(IF_FN, [">=90", ">89"], [">=75", ">74"], [">=60", ">59"], [">=40", ">39"])
    return [
        {
            "cell": f"D{row}",
            "key_row": 40 + index,
            "formula_requirements": req,
        }
        for index, row in enumerate(range(9, 21))
    ]


def _logicke_task4_items():
    # Část 1: E9:E15 — KDYŽ s A, podmínka >1500 nebo >=1501
    items = [
        {
            "cell": f"E{row}",
            "key_row": 60 + index,
            "formula_requirements": _req(IF_FN, AND_FN, [">1500", ">=1501"]),
        }
        for index, row in enumerate(range(9, 16))
    ]
    # Část 2: E23:E29 — KDYŽ s NEBO, musí být obě "Sobota" i "Neděle"
    items += [
        {
            "cell": f"E{row}",
            "key_row": 70 + index,
            "formula_requirements": _req(IF_FN, OR_FN, all_tokens=["Sobota", "Neděle"]),
        }
        for index, row in enumerate(range(23, 30))
    ]
    return items


def _logicke_task5_items():
    return [
        {
            "cell": f"F{row}",
            "key_row": 80 + index,
            # F15 (index 7): "Kolik žáků psalo test?" — =COUNT() i =COUNTIF() jsou platné
            "formula_requirements": _req(COUNT_FN) if index == 7 else _req(COUNTIF_FN),
        }
        for index, row in enumerate(range(8, 16))
    ]


def _logicke_task6_items():
    specs = [
        (8,  100, _req(SUMIF_FN, all_tokens=["jídlo"])),
        (9,  101, _req(SUMIF_FN, all_tokens=["doprava"])),
        (10, 102, _req(SUMIF_FN, all_tokens=["zábava"])),
        (11, 103, _req(SUMIF_FN, all_tokens=["oblečení"])),
        (12, 104, _req(SUMIF_FN, [">=1000", ">999"])),
        (13, 105, _req(COUNTIF_FN, all_tokens=["jídlo"])),
        (14, 106, _req(COUNTIF_FN, all_tokens=["zábava"])),
        (15, 107, _req(SUMIF_FN, all_tokens=["<>"])),
    ]
    return [
        {
            "cell": f"G{row}",
            "key_row": key_row,
            "formula_requirements": req,
        }
        for row, key_row, req in specs
    ]


def _textove_task1_items():
    # Úkol 1: C=LEN, D=LEFT, E=RIGHT, rows 8-15, klíč A6-A29 (po 3)
    items = []
    key_row = 6
    for row in range(8, 16):
        items.append({"cell": f"C{row}", "key_row": key_row,     "formula_requirements": _req(LEN_FN)})
        items.append({"cell": f"D{row}", "key_row": key_row + 1, "formula_requirements": _req(LEFT_FN)})
        items.append({"cell": f"E{row}", "key_row": key_row + 2, "formula_requirements": _req(RIGHT_FN)})
        key_row += 3
    return items


def _textove_task2_items():
    # Úkol 2 část 1: D8:D11 = MID, klíč A30-A33
    items = [
        {"cell": f"D{row}", "key_row": 30 + i, "formula_requirements": _req(MID_FN)}
        for i, row in enumerate(range(8, 12))
    ]
    # Úkol 2 část 2: D18:D21 = SEARCH, klíč A34-A37
    items += [
        {"cell": f"D{row}", "key_row": 34 + i, "formula_requirements": _req(SEARCH_FN)}
        for i, row in enumerate(range(18, 22))
    ]
    return items


def _textove_task3_items():
    # Úkol 3: C=Jméno(LEFT+SEARCH), D=Příjmení(MID+SEARCH), E=email(MID+SEARCH)
    # klíč A38-A55 (po 3, interleaved C/D/E)
    items = []
    key_row = 38
    for row in range(8, 14):
        items.append({"cell": f"C{row}", "key_row": key_row,     "formula_requirements": _req(LEFT_FN, SEARCH_FN)})
        items.append({"cell": f"D{row}", "key_row": key_row + 1, "formula_requirements": _req(MID_FN, SEARCH_FN)})
        items.append({"cell": f"E{row}", "key_row": key_row + 2, "formula_requirements": _req(MID_FN, SEARCH_FN)})
        key_row += 3
    return items


def _textove_task4_items():
    # Úkol 4: F=spojení(CONCATENATE nebo &), G=ID kód(UPPER+LEFT+CONCATENATE/&)
    # klíč A56-A71 (F/G střídavě)
    items = []
    key_row = 56
    for row in range(8, 16):
        items.append({"cell": f"F{row}", "key_row": key_row,     "formula_requirements": _req(CONCATENATE_FN)})
        items.append({"cell": f"G{row}", "key_row": key_row + 1, "formula_requirements": _req(UPPER_FN, LEFT_FN, CONCATENATE_FN)})
        key_row += 2
    return items


def _textove_task5_items():
    # Úkol 5: E=ID kód(UPPER+CONCATENATE/&), F=email(LOWER+CONCATENATE/&)
    # klíč A84-A95 (E/F střídavě)
    items = []
    key_row = 84
    for row in range(9, 15):
        items.append({"cell": f"E{row}", "key_row": key_row,     "formula_requirements": _req(UPPER_FN, CONCATENATE_FN)})
        items.append({"cell": f"F{row}", "key_row": key_row + 1, "formula_requirements": _req(LOWER_FN, CONCATENATE_FN)})
        key_row += 2
    return items


EXERCISE_CONFIGS = {
    "03_Uvod_HZD": {
        "name": "Úvod HZD - Cvičení 3",
        "answer_key_file": "03_Uvod_HZD.xlsx",
        "tasks": [
            {
                "id": "task1",
                "name": "Adresy buněk",
                "sheet": "Úkol 1",
                "answer_col": "G",
                "answer_row_start": 17,
                "answer_row_end": 26,
                "key_sheet": "Klíč",
                "key_col": "A",
                "key_row_start": 2,
                "key_row_end": 11,
                "max_points": 10,
                "comparison": "mixed",
                "requires_formula": False,
            },
            {
                "id": "task2",
                "name": "Vzorce s operátory",
                "sheet": "Úkol 2",
                "answer_col": "D",
                "answer_row_start": 9,
                "answer_row_end": 20,
                "key_sheet": "Klíč",
                "key_col": "A",
                "key_row_start": 20,
                "key_row_end": 31,
                "max_points": 12,
                "comparison": "numeric",
                "requires_formula": True,
            },
            {
                "id": "task3",
                "name": "Vzorce s odkazy",
                "sheet": "Úkol 3",
                "answer_col": "E",
                "answer_row_start": 15,
                "answer_row_end": 22,
                "key_sheet": "Klíč",
                "key_col": "A",
                "key_row_start": 40,
                "key_row_end": 47,
                "max_points": 8,
                "comparison": "numeric",
                "requires_formula": True,
            },
            {
                "id": "task4",
                "name": "Funkce SUMA",
                "sheet": "Úkol 4",
                "answer_col": "H",
                "answer_row_start": 9,
                "answer_row_end": 16,
                "key_sheet": "Klíč",
                "key_col": "A",
                "key_row_start": 60,
                "key_row_end": 67,
                "max_points": 8,
                "comparison": "numeric",
                "requires_formula": True,
            },
            {
                "id": "task5",
                "name": "Statistické funkce",
                "sheet": "Úkol 5",
                "answer_col": "D",
                "answer_col2": "E",
                "answer_row_start": 19,
                "answer_row_end": 28,
                "key_sheet": "Klíč",
                "key_col": "A",
                "key_row_start": 80,
                "key_row_end": 89,
                "max_points": 10,
                "comparison": "numeric",
                "requires_formula": True,
            },
            {
                "id": "task6",
                "name": "Komplexní úloha",
                "sheet": "Úkol 6",
                "answer_col": "F",
                "answer_row_start": 20,
                "answer_row_end": 27,
                "key_sheet": "Klíč",
                "key_col": "A",
                "key_row_start": 100,
                "key_row_end": 107,
                "max_points": 8,
                "comparison": "numeric",
                "requires_formula": True,
            },
        ],
    },
    "03_Adresace": {
        "name": "Adresace buněk - Cvičení 3",
        "answer_key_file": "03_Adresace.xlsx",
        "tasks": [
            {
                "id": "task1",
                "name": "Relativní adresace",
                "sheet": "Úkol 1",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _items_from_columns("Úkol 1", range(9, 17), ["E"], 10),
                "max_points": 8,
                "comparison": "numeric",
                "requires_formula": True,
            },
            {
                "id": "task2",
                "name": "Absolutní adresace",
                "sheet": "Úkol 2",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _adresace_task2_items(),
                "max_points": 16,
                "comparison": "numeric",
                "requires_formula": True,
            },
            {
                "id": "task3",
                "name": "Smíšená adresace - řádek",
                "sheet": "Úkol 3",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _items_from_columns("Úkol 3", range(10, 16), ["D", "E", "F"], 40, _adresace_task3_req),
                "max_points": 18,
                "comparison": "numeric",
                "requires_formula": True,
            },
            {
                "id": "task4",
                "name": "Smíšená adresace - sloupec",
                "sheet": "Úkol 4",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _items_from_columns("Úkol 4", range(9, 15), ["C", "D", "E", "F"], 80, _adresace_task4_req),
                "max_points": 24,
                "comparison": "numeric",
                "requires_formula": True,
            },
            {
                "id": "task5",
                "name": "Násobilka jediným vzorcem",
                "sheet": "Úkol 5",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _items_from_columns("Úkol 5", range(9, 16), ["D", "E", "F", "G", "H", "I", "J"], 120, _adresace_task5_req),
                "max_points": 49,
                "comparison": "numeric",
                "requires_formula": True,
            },
            {
                "id": "task6",
                "name": "Komplexní úloha - výplaty",
                "sheet": "Úkol 6",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _adresace_task6_items(),
                "max_points": 24,
                "comparison": "numeric",
                "requires_formula": True,
            },
        ],
    },
    "03_Logicke": {
        "name": "Logické funkce - Cvičení 3",
        "answer_key_file": "03_Logicke.xlsx",
        "tasks": [
            {
                "id": "task1",
                "name": "Funkce KDYŽ",
                "sheet": "Úkol 1",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _logicke_task1_items(),
                "max_points": 10,
                "comparison": "text",
                "requires_formula": True,
            },
            {
                "id": "task2",
                "name": "KDYŽ s číselným výstupem",
                "sheet": "Úkol 2",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _logicke_task2_items(),
                "max_points": 8,
                "comparison": "numeric",
                "requires_formula": True,
            },
            {
                "id": "task3",
                "name": "Vnořené KDYŽ",
                "sheet": "Úkol 3",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _logicke_task3_items(),
                "max_points": 12,
                "comparison": "numeric",
                "requires_formula": True,
            },
            {
                "id": "task4",
                "name": "KDYŽ s A/NEBO",
                "sheet": "Úkol 4",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _logicke_task4_items(),
                "max_points": 14,
                "comparison": "text",
                "requires_formula": True,
            },
            {
                "id": "task5",
                "name": "COUNTIF",
                "sheet": "Úkol 5",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _logicke_task5_items(),
                "max_points": 8,
                "comparison": "numeric",
                "requires_formula": True,
            },
            {
                "id": "task6",
                "name": "SUMIF",
                "sheet": "Úkol 6",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _logicke_task6_items(),
                "max_points": 8,
                "comparison": "numeric",
                "requires_formula": True,
            },
        ],
    },
    "03_Textove": {
        "name": "Textové funkce - Cvičení 3",
        "answer_key_file": "03_Textove.xlsx",
        "tasks": [
            {
                "id": "task1",
                "name": "DÉLKA, LEVÝ, PRAVÝ",
                "sheet": "Úkol 1",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _textove_task1_items(),
                "max_points": 24,
                "comparison": "mixed",
                "requires_formula": True,
            },
            {
                "id": "task2",
                "name": "ČÁST a HLEDAT",
                "sheet": "Úkol 2",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _textove_task2_items(),
                "max_points": 8,
                "comparison": "mixed",
                "requires_formula": True,
            },
            {
                "id": "task3",
                "name": "Rozdělení řádku",
                "sheet": "Úkol 3",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _textove_task3_items(),
                "max_points": 18,
                "comparison": "text",
                "requires_formula": True,
            },
            {
                "id": "task4",
                "name": "Spojování textu a ID kódy",
                "sheet": "Úkol 4",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _textove_task4_items(),
                "max_points": 16,
                "comparison": "text",
                "requires_formula": True,
            },
            {
                "id": "task5",
                "name": "Kapitánský úkol",
                "sheet": "Úkol 5",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _textove_task5_items(),
                "max_points": 12,
                "comparison": "text",
                "requires_formula": True,
            },
        ],
    },
    "03_Funkce": {
        "name": "Matematické a statistické funkce - Cvičení 3",
        "answer_key_file": "03_Funkce.xlsx",
        "tasks": [
            {
                "id": "task1",
                "name": "Funkce SUMA",
                "sheet": "Úkol 1",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _funkce_items("H", range(17, 27), 10, {
                    17: _req(SUM_FN),
                    18: _req(SUM_FN),
                    19: _req(SUM_FN),
                    20: _req(SUM_FN),
                    21: _req(SUM_FN),
                    22: _req(SUM_FN),
                    23: _req(MIN_FN),
                    24: _req(SUM_FN),
                    25: _req(AVERAGE_FN),
                    26: _req(AVERAGE_FN),
                }),
                "max_points": 10,
                "comparison": "numeric",
                "requires_formula": True,
            },
            {
                "id": "task2",
                "name": "PRŮMĚR, MIN, MAX",
                "sheet": "Úkol 2",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _funkce_items("I", range(20, 28), 30, {
                    20: _req(AVERAGE_FN),
                    21: _req(MAX_FN),
                    22: _req(MIN_FN),
                    23: _req(AVERAGE_FN),
                    24: _req(AVERAGE_FN),
                    25: _req(MAX_FN, MIN_FN),
                    26: _req(AVERAGE_FN),
                    27: _req(SUM_FN),
                }),
                "max_points": 8,
                "comparison": "numeric",
                "requires_formula": True,
            },
            {
                "id": "task3",
                "name": "POČET, POČET2, POČET.PRÁZDNÝCH",
                "sheet": "Úkol 3",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _funkce_items("J", range(8, 14), 50, {
                    8: _req(COUNT_FN),
                    9: _req(COUNTA_FN),
                    10: _req(COUNTBLANK_FN),
                    11: _req(COUNT_FN),
                    12: _req(COUNTBLANK_FN),
                    13: _req(COUNTA_FN),
                }),
                "max_points": 6,
                "comparison": "numeric",
                "requires_formula": True,
            },
            {
                "id": "task4",
                "name": "ZAOKROUHLIT",
                "sheet": "Úkol 4",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _funkce_task4_items(),
                "max_points": 10,
                "comparison": "numeric",
                "requires_formula": True,
            },
            {
                "id": "task5",
                "name": "Kombinace funkcí",
                "sheet": "Úkol 5",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _funkce_task5_items(),
                "max_points": 6,
                "comparison": "numeric",
                "requires_formula": True,
            },
            {
                "id": "task6",
                "name": "Komplexní úloha",
                "sheet": "Úkol 6",
                "key_sheet": "Klíč",
                "key_col": "A",
                "items": _funkce_task6_items(),
                "max_points": 10,
                "comparison": "numeric",
                "requires_formula": True,
            },
        ],
    },
}
