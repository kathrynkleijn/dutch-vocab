import random
from dutchvocab import lessons as lessons
import copy
from dutchvocab import vocab_functions as vf
import pandas as pd
from dutchvocab import lesson_objects as lo
from dutchvocab import pdf_constructor
from datetime import date, timedelta


def main():

    playing = True
    log = pd.DataFrame(columns=["Module", "Lesson", "Questions", "Score"])
    while playing:

        print(f"Available lessons:\n {lo.available}\n\n")

        topic_enquiry = input(
            "Select a topic, choose random or choose 'all'        "
        ).lower()

        if topic_enquiry == "random":
            topic = random.choice(lessons.topics)
        else:
            topic = topic_enquiry

        print(f"You have selected {topic.capitalize()}.")

        if topic == "core":
            lesson = vf.select_lesson(lo.core)
            questions = vf.select_questions(lesson)

            correct = vf.randomly_generated_lesson(lesson, questions)
            log = vf.update_log(log, topic, lesson.name, questions, correct)

        elif topic == "fiction":
            lesson = vf.select_lesson(lo.fiction)
            questions = vf.select_questions(lesson)

            correct = vf.randomly_generated_lesson(lesson, questions)
            log = vf.update_log(log, topic, lesson.name, questions, correct)

        elif topic == "newspapers":
            lesson = vf.select_lesson(lo.newspapers)
            questions = vf.select_questions(lesson)

            correct = vf.randomly_generated_lesson(lesson, questions)
            log = vf.update_log(log, topic, lesson.name, questions, correct)

        elif topic == "spoken":
            lesson = vf.select_lesson(lo.spoken)
            questions = vf.select_questions(lesson)

            correct = vf.randomly_generated_lesson(lesson, questions)
            log = vf.update_log(log, topic, lesson.name, questions, correct)

        elif topic == "web":
            lesson = vf.select_lesson(lo.web)
            questions = vf.select_questions(lesson)

            correct = vf.randomly_generated_lesson(lesson, questions)
            log = vf.update_log(log, topic, lesson.name, questions, correct)

        elif topic == "general":
            lesson = vf.select_lesson(lo.general)
            questions = vf.select_questions(lesson)

            correct = vf.randomly_generated_lesson(lesson, questions)
            log = vf.update_log(log, topic, lesson.name, questions, correct)

        elif topic == "all":
            lesson = lo.overall.all
            questions = vf.select_questions(lesson)

            correct = vf.randomly_generated_lesson(lesson, questions)
            log = vf.update_log(log, topic, "all", questions, correct)
        else:
            print("Topic not recognised, please try again")
            correct = 1
            questions = 1

        if topic != "all":
            if (correct / questions) * 100 < 50:
                again = input("\nScore less than 50% - try again?  (Y/N)       ")
                print("\n")
                if again == "Y":
                    print(f"Retrying lesson {lesson.number} from {topic} ...\n")
                    if topic == "core":
                        lesson = copy.deepcopy(lo.core.lessons[int(lesson.number) - 1])
                    elif topic == "fiction":
                        lesson = copy.deepcopy(
                            lo.fiction.lessons[int(lesson.number) - 1]
                        )
                    elif topic == "newspapers":
                        lesson = copy.deepcopy(
                            lo.newspapers.lessons[int(lesson.number) - 1]
                        )
                    elif topic == "spoken":
                        lesson = copy.deepcopy(
                            lo.spoken.lessons[int(lesson.number) - 1]
                        )
                    elif topic == "web":
                        lesson = copy.deepcopy(lo.web.lessons[int(lesson.number) - 1])
                    elif topic == "general":
                        lesson = copy.deepcopy(
                            lo.general.lessons[int(lesson.number) - 1]
                        )
                    correct = vf.randomly_generated_lesson(lesson, questions)
                    log = vf.update_log(log, topic, lesson.name, questions, correct)

        again = input("\nWould you like to do another lesson?  (Y/N)       ")
        if again == "N":
            playing = False
            print("\nEnd of lessons")

    log.to_csv("learning_log.csv", mode="a", header=False)
    vf.visualisation_today()
    # generate weekly/monthly report, ask about progress report
    print("\nUpdating reports...")
    log_full = pd.read_csv("learning_log.csv")
    weekly_pdf = pdf_constructor.build_pdf(log_full, "Weekly")
    weekly_pdf.output(
        f"Reports/Weekly_Reports/{(date.today() - timedelta(days=date.today().weekday())).strftime('%Y%m%d')}_Report.pdf",
        "F",
    )
    monthly_pdf = pdf_constructor.build_pdf(log_full, "Monthly")
    monthly_pdf.output(
        f"Reports/Monthly_Reports/{date.today().strftime('%Y_%B')}_Report.pdf",
        "F",
    )
    print("\nWeekly and monthly reports updated.")
    progress = input("Would you like to generate a progress report?  (Y/N)       ")
    if progress == "Y":
        pdf = pdf_constructor.build_pdf(log_full, "Progress")
        pdf.output(
            f"Reports/Progress_Reports/{date.today().strftime('%Y%m%d')}_Report.pdf",
            "F",
        )
        print("Progress report completed.")


if __name__ == "__main__":
    main()
