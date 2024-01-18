import csv
import smb_inspector as smb

def write_output(host, share, danger):
    file = f"{host}.txt"

    # Open the CSV file for writing
    with open(file, mode="w", newline="", encoding="utf-8") as file:
        # Create a CSV writer object
        writer = csv.writer(file)

        # Write header
        writer.writerow(["Host", "Found Shares"])

        # Write data
        for entry in share:
            writer.writerow([host, entry])

        # Write header
        writer.writerow([])
        writer.writerow(["Host", "Dangerous Shares"])

        # Write data
        for dangerous in danger:
            writer.writerow([host, dangerous])

    print(f"Data has been written to {file}")
