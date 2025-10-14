import inquirer
import os


def main():

    print("Welcome to Settings")

    # default settings if not preset
    report_path = ""  # save to working Path
    plot_path = ""  # save to working Path
    output = "Yes"  # output reports after each session

    if os.path.isfile("settings.txt"):
        with open("settings.txt", "r") as file:
            settings = file.read().splitlines()
        report_path = settings[0].rstrip("/")
        plot_path = settings[1].rstrip("/")
        output = settings[2]

    print(
        "\nOptional settings:\nPath to save learning reports\nPath to save temporary plots for building reports\nAutomatic output of weekly and monthly reports\n"
    )

    if not report_path:
        report_path_out = "current directory"
    else:
        report_path_out = report_path

    if not plot_path:
        plot_path_out = "current directory"
    else:
        plot_path_out = plot_path

    print(
        f"\nCurrent settings:\nReport Save Path      {report_path_out}\nPlots Save Path       {plot_path_out}\nReport Output         {output}"
    )

    edit_settings = input("\nDo you want to edit any settings? (Y/N) ")
    if edit_settings.upper() != "Y":
        setting = False
    else:
        setting = True

    while setting == True:

        options = ["Report Save Path", "Plots Save Path", "Report Output"]
        select_setting = [
            inquirer.List("setting", message="Select setting to edit", choices=options)
        ]
        selected = inquirer.prompt(select_setting)
        print(f"Going to {selected['setting']} setting...\n")

        if selected["setting"] == "Report Save Path":
            report_path = input("Insert path for saving reports: ")
            print(f"\nReports will be saved in {report_path.rstrip('/')}/Reports")

        elif selected["setting"] == "Plots Save Path":
            plot_path = input("Insert path for saving plots: ")
            print(f"\nPlots will be saved in {plot_path.rstrip('/')}/plots")

        elif selected["setting"] == "Report Output":
            select_output = [
                inquirer.List(
                    "setting",
                    message="Do you want to output reports at the end of each session?",
                    choices=["Yes", "No"],
                )
            ]
            output = inquirer.prompt(select_output)
            output = output["setting"]
            if output == "Yes":
                print("Reports will be output at the end of each session.")
            elif output == "No":
                print("Reports will not be output at the end of each session.")

        continue_setting = input("\nChange other settings? (Y/N) ")
        if continue_setting.upper() != "Y":
            setting = False
            break

    with open("settings.txt", "w") as file:
        file.write(report_path)
        file.write("\n")
        file.write(plot_path)
        file.write("\n")
        file.write(output)

    print("\nYour settings have been saved.")
