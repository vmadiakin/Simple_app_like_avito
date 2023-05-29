import csv
import json

csv_file_path = './ads.csv'
json_file_path = './ads.json'

# Открыть CSV-файл и прочитать его содержимое с указанием кодировки
with open(csv_file_path, 'r', encoding='UTF-8') as csv_file:
    csv_data = csv.DictReader(csv_file)

    # Преобразовать данные в список словарей
    data_list = []
    for row in csv_data:
        data_list.append(row)

# Записать данные в JSON-файл
with open(json_file_path, 'w') as json_file:
    json.dump(data_list, json_file, indent=4)

print("Преобразование CSV в JSON завершено.")
