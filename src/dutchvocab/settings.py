import inquirer

print("Welcome to Settings")

# default settings
report_path = ""  # save to working folder

options = ["Report Save Folder", "Plots Save Folder"]
select_setting = [
    inquirer.List("setting", message="Select setting to edit", choices=options)
]
selected = inquirer.prompt(select_setting)
print("Going to Report Save Folder setting...\n")


if selected["setting"] == "Report Save Folder":
    report_path = input("Insert path for saving reports: ")


with open("settings.txt", "w") as file:
    file.write(report_path)

print("\nYour settings have been saved.")
