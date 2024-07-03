import csv
import smb_inspector as smb

def write_output(host, foundfiles, danger, shares):
    file_shares=f"{host}_shares.txt"
    file_interesting=f"{host}_interesting.txt"
    file_danger=f"{host}_dangers.txt"

    # Open the CSV file for writing
    with open(file_shares, mode="w", newline="", encoding="utf-8") as file_shares_out:
        # Create a CSV writer object
        writer = csv.writer(file_shares_out)

        # Write header
        writer.writerow(["Host", "Found Shares"])

        # Write data
        for entry in shares:
            writer.writerow([host, entry])

    with open(file_interesting, mode="w", newline="", encoding="utf-8") as file_interesting_out:
        # Create a CSV writer object
        writer = csv.writer(file_interesting_out)

        # Write header
        writer.writerow(["Host", "Interesting Shares"])

        # Write data
        for interesting in foundfiles:
            writer.writerow([host, interesting])

    with open(file_danger, mode="w", newline="", encoding="utf-8") as file_danger_out:
        # Create a CSV writer object
        writer = csv.writer(file_danger_out)

        # Write header
        writer.writerow(["Host", "Dangerous Shares"])

        # Write data
        for dangerous in danger:
            writer.writerow([host, dangerous])

    print("Data has been written to this directory.")

