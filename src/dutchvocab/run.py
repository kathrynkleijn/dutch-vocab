from dutchvocab import lessons as lessons
from dutchvocab import vocab_functions as vf
from dutchvocab import lesson_objects as lo
from dutchvocab import pdf_constructor
from dutchvocab import figure_generator as fg
from dutchvocab import runner as rn
from dutchvocab import settings as st
import pandas as pd
from datetime import date, timedelta
import os
import inquirer
import time


def main():

    # get settings
    if not os.path.isfile("settings.txt"):
        st.main(init=True)
        returning = None
    else:
        returning = True

    with open("settings.txt", "r") as file:
        settings = file.read().splitlines()
        report_path = settings[0]
        report_output = settings[2]
        messages = settings[3]

    # check for trailing "/"
    if report_path and not report_path.endswith("/"):
        report_path = report_path + "/"

    if returning is None:
        print("\n")
        vf.slow_print(
            """Welcome!\n\nThis package allows you to learn Dutch vocabulary through flashcards and practising translating words and phrases.
The words are split into different categories based on their usage.\nThere is also the ability to test your knowledge in a testing mode.\n\n
            (This and subsequent messages can be removed in the settings)""",
            0.05,
            0.5,
        )
    elif messages == "On":
        print("\n")
        vf.slow_print(
            """Welcome back!\n\nThis package allows you to learn Dutch vocabulary through flashcards and practising translating words and phrases.
The words are split into different categories based on their usage.\nThere is also the ability to test your knowledge in a testing mode.\n\n"""
        )
    elif messages == "Off":
        print("\n")
        print("Welcome back!")

    if returning is None:
        messages = "On"

    print("\n")
    vf.slow_print(
        f"Available lessons:\n{lo.available}\n\n",
        char_delay=0,
        line_delay=0.2,
    )
    time.sleep(0.5)
    input("\n\nPress Enter to continue")

    print("\n")
    select_setting = [
        inquirer.List(
            "type",
            message="Select mode",
            choices=["Learning", "Practice", "Test", "Exit"],
        )
    ]
    mode = inquirer.prompt(select_setting)["type"]
    if mode == "Exit":
        mode = False

    practice = False
    test = False
    log = pd.DataFrame(
        columns=["Module", "Lesson", "Questions", "Score", "Type", "Typos English"]
    )
    test_log = pd.DataFrame(columns=["Lesson", "Result", "Error"])
    while mode:
        if mode == "Learning":

            mode = rn.run_learning(messages)

        elif mode == "Practice":

            mode, log = rn.run_practice(log, practice, messages)

            practice = True

        elif mode == "Test":

            mode, tlog = rn.run_test(messages)
            if tlog is not None:
                test_log = pd.concat([test_log, tlog])

                test = True

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

    if test:

        if os.path.isfile("testing_log.csv"):
            test_log.to_csv("testing_log.csv", mode="a", header=False)
        else:
            test_log.to_csv(
                "testing_log.csv",
                mode="a",
                header=True,
                index=True,
                index_label="Date",
            )

        log_full = pd.read_csv("testing_log.csv")
        fg.generate_test_figures(log_full, single=False)


if __name__ == "__main__":
    main()
