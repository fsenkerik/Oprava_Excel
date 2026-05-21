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
}
