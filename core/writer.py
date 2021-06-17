from openpyxl import Workbook


def save_to_excel(results: list):
    wb = Workbook()
    ws = wb.active

    results = results[0][1]
    index = results[0]._fields

    ws.append(index)

    for result in results:
        result = result._asdict()

        for k, v in result.items():
            if isinstance(v, list):
                result[k] = ','.join(v)

        ws.append(list(result.values()))
   
    wb.save("./check_result.xlsx")

def write(results, writer):
    d = {
        "excel": save_to_excel
    }

    print("Saving...")

    writer = d.get(writer)
    writer(results)

    print("Save successful")