from dutchvocab import lessons as lessons
from dutchvocab import vocab_functions as vf
from dutchvocab import lesson_objects as lo
from dutchvocab import pdf_constructor
from dutchvocab import figure_generator as fg
from dutchvocab import runner as rn
import pandas as pd
from datetime import date, timedelta
import os
import inquirer
import time


def main():

    # get settings
    with open("settings.txt", "r") as file:
        settings = file.read().splitlines()
    report_path = settings[0]
    report_output = settings[2]

    if report_path and not report_path.endswith("/"):
        report_path = report_path + "/"

    print("\n")
    vf.slow_print(
        f"Available lessons:\n {lo.available}\n\n",
        char_delay=0,
        line_delay=0.2,
    )
    time.sleep(0.5)
    input("\n\nPress Enter to continue")

    print("\n")
    select_setting = [
        inquirer.List("type", message="Select mode", choices=["Practice", "Test"])
    ]
    mode = inquirer.prompt(select_setting)["type"]

    practice = False
    log = pd.DataFrame(columns=["Module", "Lesson", "Questions", "Score"])
    while mode:
        if mode == "Practice":

            mode, log = rn.run_practice(log, practice)

            practice = True

        elif mode == "Test":

            mode = rn.run_test()

    print("Exiting lessons...")

    if practice:

        if os.path.isfile("learning_log.csv"):
            log.to_csv("learning_log.csv", mode="a", header=False)
        else:
            log.to_csv(
                "learning_log.csv",
                mode="a",
                header=True,
                index=True,
                index_label="Date",
            )
        vf.visualisation_today()

        # generate weekly/monthly report, ask about progress report
        if report_output == "Yes":
            print("\nUpdating reports...")

            # make directories if non-existent
            os.makedirs(f"{report_path}Reports/Weekly_Reports", exist_ok=True)
            os.makedirs(f"{report_path}Reports/Monthly_Reports", exist_ok=True)

            log_full = pd.read_csv("learning_log.csv")
            weekly_pdf = pdf_constructor.build_pdf(log_full, "Weekly")
            weekly_pdf.output(
                f"{report_path}Reports/Weekly_Reports/{(date.today() - timedelta(days=date.today().weekday())).strftime('%Y%m%d')}_Report.pdf",
                "F",
            )
            monthly_pdf = pdf_constructor.build_pdf(log_full, "Monthly")

            monthly_pdf.output(
                f"{report_path}Reports/Monthly_Reports/{date.today().strftime('%Y_%B')}_Report.pdf",
                "F",
            )

            print("\nWeekly and monthly reports updated.")
            progress = input(
                "Would you like to generate a progress report?  (Y/N)       "
            )
            if progress == "Y":
                # make directories if non-existent
                os.makedirs(f"{report_path}/Reports/Progress_Reports", exist_ok=True)
                pdf = pdf_constructor.build_pdf(log_full, "Progress")
                pdf.output(
                    f"{report_path}Reports/Progress_Reports/{date.today().strftime('%Y%m%d')}_Report.pdf",
                    "F",
                )
                print("Progress report completed.")


if __name__ == "__main__":
    main()
