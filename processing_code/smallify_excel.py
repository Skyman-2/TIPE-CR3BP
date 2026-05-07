import csv

# Path to your CSV file
file_path = "./processing_code/output.csv"

# Convert CSV to a list
with open(file_path, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    data_list = list(reader)


epurated_list = []

former = data_list[0]
for i in range(len(data_list)//5):
    # if data_list[i][1] != former[1]:
    #     epurated_list.append(data_list[i])
    # former = data_list[i]
    epurated_list.append(data_list[i*5])


with open(file_path, mode="w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(epurated_list)