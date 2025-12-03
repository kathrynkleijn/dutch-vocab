import pandas as pd
from plotnine import (
    ggplot,
    aes,
    labs,
    geom_bar,
    theme,
    facet_grid,
    ylim,
    scale_fill_brewer,
    scale_fill_manual,
    element_text,
    geom_line,
    geom_point,
    scale_x_datetime,
    scale_color_brewer,
    scale_color_manual,
    geom_text,
    after_stat,
    stage,
)
from datetime import date, timedelta
from dutchvocab import lesson_objects
import numpy as np
from mizani.palettes import brewer_pal, gradient_n_pal
import matplotlib.colors as mcolors
import re
import os

## Practice Log Figures

# create colour palette with seven base colours (one per topic)
pal = brewer_pal("qual", "Paired")

base_colors = list(pal(7))

all_colors = []
for base_color in base_colors:
    # create gradient from darkened to lightened version of the base colour
    gradient = gradient_n_pal([mcolors.to_hex("black"), base_color, "white"])(
        np.linspace(0, 1, 10)
    )
    all_colors.extend(gradient)


months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

lessons_per_module = {
    topic.name: len(topic.lessons) for topic in lesson_objects.topics_all
}
lessons_per_module["all"] = sum(value for value in lessons_per_module.values()) - 6


def daily_log_module(log):
    log.Date = pd.to_datetime(log.Date)
    log = log.groupby(["Date", "Module", "Lesson"]).agg(
        Questions=("Questions", "sum"), Score=("Score", "sum")
    )
    log["Percentage"] = log.apply(
        lambda row: round(row["Score"] / row["Questions"] * 100, 1), axis=1
    )
    log = log.reset_index()
    week_beginning = date.today() - timedelta(days=date.today().weekday())
    log["Week"] = log.Date.dt.to_period("W").dt.start_time
    return log[log["Week"] == week_beginning.strftime("%Y-%m-%d")]


def weekly_log_module(log):
    log.Date = pd.to_datetime(log.Date)
    log["Week"] = log.Date.dt.to_period("W").dt.start_time
    log = log.groupby([pd.Grouper(key="Week", freq="W-MON"), "Module"]).agg(
        Questions=("Questions", "sum"), Score=("Score", "sum")
    )
    log = log.reset_index()
    log["Percentage"] = log.apply(
        lambda row: round(row["Score"] / row["Questions"] * 100, 1), axis=1
    )
    log["Normalised Questions"] = log.apply(
        lambda row: row["Questions"] / lessons_per_module[row["Module"]], axis=1
    )
    return log


def weekly_log_lesson(log):
    log.Date = pd.to_datetime(log.Date)
    log["Week"] = log.Date.dt.to_period("W").dt.start_time
    log = log.groupby([pd.Grouper(key="Week", freq="W-MON"), "Module", "Lesson"]).agg(
        Questions=("Questions", "sum"), Score=("Score", "sum")
    )
    log = log.reset_index()
    log["Percentage"] = log.apply(
        lambda row: round(row["Score"] / row["Questions"] * 100, 1), axis=1
    )
    return log


def module_log(log):
    log = log.groupby("Module").agg(
        Questions=("Questions", "sum"), Score=("Score", "sum")
    )
    log["Percentage"] = log.apply(
        lambda row: round(row["Score"] / row["Questions"] * 100, 1), axis=1
    )
    log = log.reset_index()
    log["Normalised Questions"] = log.apply(
        lambda row: row["Questions"] / lessons_per_module[row["Module"]], axis=1
    )
    return log.reset_index()


def lesson_log(log):
    log = log.groupby(["Module", "Lesson"]).agg(
        Questions=("Questions", "sum"), Score=("Score", "sum")
    )
    log["Percentage"] = log.apply(
        lambda row: round(row["Score"] / row["Questions"] * 100, 1), axis=1
    )
    return log.reset_index()


def monthly_log_lesson(log):
    log.Date = pd.to_datetime(log.Date)
    log["Year"] = log["Date"].dt.year.astype("Int64")
    log["Year"] = log["Year"].astype(str)
    log = log.groupby([log.Year, log.Date.dt.month, "Module", "Lesson"]).agg(
        Questions=("Questions", "sum"), Score=("Score", "sum")
    )
    log = log.reset_index()
    log["Date"] = pd.to_datetime(log["Date"], format="%m")
    log["Date"] = log["Date"].dt.strftime("%B")
    log["Date"] = pd.Categorical(log["Date"], categories=months, ordered=True)
    log["Percentage"] = log.apply(
        lambda row: round(row["Score"] / row["Questions"] * 100, 1), axis=1
    )
    return log


def monthly_log_module(log):
    log.Date = pd.to_datetime(log.Date)
    log["Year"] = log["Date"].dt.year.astype("Int64")
    log["Year"] = log["Year"].astype(str)
    log = log.groupby([log.Year, log.Date.dt.month, "Module"]).agg(
        Questions=("Questions", "sum"), Score=("Score", "sum")
    )
    log = log.reset_index()
    log["Date"] = pd.to_datetime(log["Date"], format="%m")
    log["Date"] = log["Date"].dt.strftime("%B")
    log["Date"] = pd.Categorical(log["Date"], categories=months, ordered=True)
    log["Percentage"] = log.apply(
        lambda row: round(row["Score"] / row["Questions"] * 100, 1), axis=1
    )
    log["Normalised Questions"] = log.apply(
        lambda row: row["Questions"] / lessons_per_module[row["Module"]], axis=1
    )
    return log


def monthly_log(log):
    log.Date = pd.to_datetime(log.Date)
    log["Year"] = log["Date"].dt.year.astype("Int64")
    log["Year"] = log["Year"].astype(str)
    log = log.groupby([log.Year, log.Date.dt.month]).agg(
        Questions=("Questions", "sum"), Score=("Score", "sum")
    )
    log = log.reset_index()
    log["Date"] = pd.to_datetime(log["Date"], format="%m")
    log["Date"] = log["Date"].dt.strftime("%B")
    log["Date"] = pd.Categorical(log["Date"], categories=months, ordered=True)
    log["Percentage"] = log.apply(
        lambda row: round(row["Score"] / row["Questions"] * 100, 1), axis=1
    )
    return log


def log_maker(report_title, log, debug=False, debug_week=False):
    logs = []
    if report_title == "Weekly":
        week_beginning = date.today() - timedelta(days=date.today().weekday())
        if debug:
            week_beginning = debug_week
        log_1 = weekly_log_module(log)
        log_2 = weekly_log_lesson(log)
        logs.extend(
            [
                log_1[log_1["Week"] == week_beginning.strftime("%Y-%m-%d")],
                log_2[log_2["Week"] == week_beginning.strftime("%Y-%m-%d")],
                daily_log_module(log),
            ]
        )
    elif report_title == "Monthly":
        logs.extend([monthly_log_module(log), monthly_log_lesson(log)])
    elif report_title == "Progress":
        logs.extend(
            [
                log,
                module_log(log),
                lesson_log(log),
                monthly_log_module(log),
                monthly_log_lesson(log),
                monthly_log(log),
                weekly_log_lesson(log),
            ]
        )
    return logs


def generate_figures(report_title, logs):

    numbers = [x for x in range(1, 11)]
    topics = [
        "core",
        "fiction",
        "newspapers",
        "spoken",
        "web",
        "general",
        "all",
    ]
    lessons = []
    for topic in topics:
        for num in numbers:
            lessons.append(topic + str(num))
    log.Lesson = pd.Categorical(log["Lesson"], categories=lessons, ordered=True)

    with open("settings.txt", "r") as file:
        settings = file.read().splitlines()
    plot_path = settings[1]

    if plot_path and not plot_path.endswith("/"):
        plot_path = plot_path + "/"

    os.makedirs(f"{plot_path}plots/weekly", exist_ok=True)
    os.makedirs(f"{plot_path}plots/monthly", exist_ok=True)
    os.makedirs(f"{plot_path}plots/progress", exist_ok=True)

    if report_title == "Weekly":
        print(logs[0])

        plot1 = (
            ggplot(logs[0], aes(x="Module", y="Questions", fill="Module"))
            + geom_bar(stat="identity", width=0.5, show_legend=False)
            + scale_fill_brewer(type="qual", palette="Paired")
            + labs(
                x="Module",
                y="Total Questions Answered",
                title="Total Questions Answered Per Module",
            )
            + theme(figure_size=(10, 6))
        )
        plot1a = (
            ggplot(
                logs[0],
                aes(x="Module", y="Normalised Questions", fill="Module"),
            )
            + geom_bar(stat="identity", width=0.5, show_legend=False)
            + scale_fill_brewer(type="qual", palette="Paired")
            + labs(
                x="Module",
                y="Normalised Questions Answered",
                title="Questions Answered Per Module, Normalised by Number of Lessons",
            )
            + theme(figure_size=(10, 6))
        )
        plot2 = (
            ggplot(
                logs[0],
                aes(x="Module", y="Score/Questions*100", fill="Module"),
            )
            + geom_bar(stat="identity", width=0.5, show_legend=False)
            + scale_fill_brewer(type="qual", palette="Paired")
            + labs(
                x="Module",
                y="Percentage",
                title="Percentage Score Per Module",
            )
            + ylim((0, 100))
            + theme(figure_size=(10, 6))
        )
        plot3 = (
            ggplot(logs[1], aes(x="Lesson", y="Questions", fill="Module"))
            + geom_bar(stat="identity", width=0.5, show_legend=False)
            + scale_fill_brewer(type="qual", palette="Paired")
            + labs(
                x="Lesson",
                y="Total Questions Answered",
                title="Total Questions Answered Per Lesson",
            )
            + theme(figure_size=(10, 6), axis_text_x=element_text(rotation=45, hjust=1))
        )
        plot4 = (
            ggplot(logs[1], aes(x="Lesson", y="Score/Questions*100", fill="Module"))
            + geom_bar(stat="identity", width=0.5, show_legend=False)
            + scale_fill_brewer(type="qual", palette="Paired")
            + labs(
                x="Lesson",
                y="Percentage",
                title="Percentage Score Per Lesson",
            )
            + ylim((0, 100))
            + theme(figure_size=(10, 6), axis_text_x=element_text(rotation=45, hjust=1))
        )

        plot1.save(f"{plot_path}plots/weekly/1.png", verbose=False)
        plot1a.save(f"{plot_path}plots/weekly/1a.png", verbose=False)
        plot2.save(f"{plot_path}plots/weekly/2.png", verbose=False)
        plot3.save(f"{plot_path}plots/weekly/3.png", verbose=False)
        plot4.save(f"{plot_path}plots/weekly/4.png", verbose=False)

        plot5 = (
            ggplot(
                logs[2],
                aes(x="Date", y="Score/Questions*100", group="Lesson", color="Lesson"),
            )
            + geom_line()
            + geom_point()
            + scale_color_brewer(type="qual", palette="Paired")
            + labs(
                x="Date",
                y="Percentage",
                title="Percentage Score Per Day",
            )
            + theme(figure_size=(10, 6))
            + scale_x_datetime(breaks="1 days")
        )

        plot5.save(f"{plot_path}plots/weekly/5.png", verbose=False)

    elif report_title == "Monthly":
        logs[0] = logs[0][logs[0].Year == date.today().strftime("%Y")]
        logs[1] = logs[1][logs[1].Year == date.today().strftime("%Y")]
        plot1 = (
            ggplot(
                logs[0][logs[0].Date == date.today().strftime("%B")],
                aes(x="Module", y="Questions", fill="Module"),
            )
            + geom_bar(stat="identity", width=0.5, show_legend=False)
            + scale_fill_brewer(type="qual", palette="Paired")
            + labs(
                x="Module",
                y="Total Questions Answered",
                title="Total Questions Answered Per Module",
            )
            + theme(figure_size=(10, 6))
        )

        plot1a = (
            ggplot(
                logs[0][logs[0].Date == date.today().strftime("%B")],
                aes(x="Module", y="Normalised Questions", fill="Module"),
            )
            + geom_bar(stat="identity", width=0.5, show_legend=False)
            + scale_fill_brewer(type="qual", palette="Paired")
            + labs(
                x="Module",
                y="Normalised Questions Answered",
                title="Questions Answered Per Module, Normalised by Number of Lessons",
            )
            + theme(figure_size=(10, 6))
        )
        plot2 = (
            ggplot(
                logs[0][logs[0].Date == date.today().strftime("%B")],
                aes(x="Module", y="Score/Questions*100", fill="Module"),
            )
            + geom_bar(stat="identity", width=0.5, show_legend=False)
            + scale_fill_brewer(type="qual", palette="Paired")
            + labs(
                x="Module",
                y="Percentage",
                title="Percentage Score Per Module",
            )
            + ylim((0, 100))
            + theme(figure_size=(10, 6))
        )
        plot3 = (
            ggplot(
                logs[1][logs[1].Date == date.today().strftime("%B")],
                aes(x="Lesson", y="Questions", fill="Module"),
            )
            + geom_bar(stat="identity", width=0.5, show_legend=False)
            + scale_fill_brewer(type="qual", palette="Paired")
            + labs(
                x="Lesson",
                y="Total Questions Answered",
                title="Total Questions Answered Per Lesson",
            )
            + theme(figure_size=(10, 6), axis_text_x=element_text(rotation=45, hjust=1))
        )
        plot4 = (
            ggplot(
                logs[1][logs[1].Date == date.today().strftime("%B")],
                aes(x="Lesson", y="Score/Questions*100", fill="Module"),
            )
            + geom_bar(stat="identity", width=0.5, show_legend=False)
            + scale_fill_brewer(type="qual", palette="Paired")
            + labs(
                x="Lesson",
                y="Percentage",
                title="Percentage Score Per Lesson",
            )
            + ylim((0, 100))
            + theme(figure_size=(10, 6), axis_text_x=element_text(rotation=45, hjust=1))
        )

        plot1.save(f"{plot_path}plots/monthly/1.png", verbose=False)
        plot1a.save(f"{plot_path}plots/monthly/1a.png", verbose=False)
        plot2.save(f"{plot_path}plots/monthly/2.png", verbose=False)
        plot3.save(f"{plot_path}plots/monthly/3.png", verbose=False)
        plot4.save(f"{plot_path}plots/monthly/4.png", verbose=False)

    elif report_title == "Progress":
        plot1 = (
            ggplot(
                logs[0], aes(x="Module", y="Questions", group="Module", fill="Module")
            )
            + geom_bar(
                stat="identity",
                width=0.5,
                show_legend=False,
            )
            + scale_fill_brewer(type="qual", palette="Paired")
            + labs(
                x="Module",
                y="Total Questions Answered",
                title="Number of Questions Answered Per Module, All Time",
            )
            + theme(figure_size=(10, 6))
        )
        plot1a = (
            ggplot(
                logs[1],
                aes(x="Module", y="Normalised Questions", fill="Module"),
            )
            + geom_bar(stat="identity", width=0.5, show_legend=False)
            + scale_fill_brewer(type="qual", palette="Paired")
            + labs(
                x="Module",
                y="Normalised Questions Answered",
                title="Questions Answered Per Module, Normalised by Number of Lessons",
            )
            + theme(figure_size=(10, 6))
        )
        plot3 = (
            ggplot(
                logs[0], aes(x="Lesson", y="Questions", group="Lesson", fill="Module")
            )
            + geom_bar(stat="identity", width=0.5, show_legend=False)
            + scale_fill_brewer(type="qual", palette="Paired")
            + labs(
                x="Lesson",
                y="Total Questions Answered",
                title="Number of Questions Answered Per Lesson, All Time",
            )
            + theme(figure_size=(10, 6), axis_text_x=element_text(rotation=45, hjust=1))
        )
        plot2 = (
            ggplot(logs[1], aes(x="Module", y="Score/Questions*100", fill="Module"))
            + geom_bar(stat="identity", width=0.5, show_legend=False)
            + scale_fill_brewer(type="qual", palette="Paired")
            + labs(
                x="Module",
                y="Percentage",
                title="Percentage Score Per Module, All Time",
            )
            + ylim((0, 100))
            + theme(figure_size=(10, 6))
        )
        plot4 = (
            ggplot(logs[2], aes(x="Lesson", y="Score/Questions*100", fill="Module"))
            + geom_bar(stat="identity", width=0.5, show_legend=False)
            + scale_fill_brewer(type="qual", palette="Paired")
            + labs(
                x="Lesson",
                y="Percentage",
                title="Percentage Score Per Lesson, All Time",
            )
            + ylim((0, 100))
            + theme(figure_size=(10, 6), axis_text_x=element_text(rotation=45, hjust=1))
        )

        logs[6]["Year"] = logs[6]["Week"].dt.year.astype("Int64")
        logs[6]["Year"] = logs[6]["Year"].astype(str)
        weekly_log = logs[6][logs[6].Year == date.today().strftime("%Y")]
        start_week = weekly_log["Week"].iloc[0]
        week_beginning = date.today() - timedelta(days=date.today().weekday())
        number_of_weeks = start_week.date() - week_beginning
        breaks = [
            week_beginning - timedelta(7 * week)
            for week in range(abs(int(number_of_weeks.days / 7)) + 1)
        ]
        breaks = breaks[::-1]
        plot4a = (
            ggplot(
                logs[6],
                aes(x="Week", y="Score/Questions*100", group="Lesson", color="Lesson"),
            )
            + geom_line()
            + geom_point()
            + scale_color_manual(values=all_colors)
            + labs(
                x="Week Beginning",
                y="Percentage",
                title="Percentage Score Per Week",
            )
            + theme(figure_size=(10, 6))
            + scale_x_datetime(breaks=breaks)
        )

        plot1.save(f"{plot_path}plots/progress/1.png", verbose=False)
        plot1a.save(f"{plot_path}plots/progress/1a.png", verbose=False)
        plot2.save(f"{plot_path}plots/progress/2.png", verbose=False)
        plot3.save(f"{plot_path}plots/progress/3.png", verbose=False)
        plot4.save(f"{plot_path}plots/progress/4.png", verbose=False)
        plot4a.save(f"{plot_path}plots/progress/4a.png", verbose=False)

        plot5 = (
            ggplot(logs[3], aes(x="Module", y="Questions", fill="Module"))
            + facet_grid(rows="Date")
            + geom_bar(stat="identity", width=0.5, show_legend=False)
            + scale_fill_brewer(type="qual", palette="Paired")
            + labs(
                x="Module",
                y="Total Questions Answered",
                title="Number of Questions Answered Per Module, Per Month",
            )
            + theme(figure_size=(10, 12))
        )
        plot5a = (
            ggplot(
                logs[3],
                aes(x="Module", y="Normalised Questions", fill="Module"),
            )
            + facet_grid(rows="Date")
            + geom_bar(stat="identity", width=0.5, show_legend=False)
            + scale_fill_brewer(type="qual", palette="Paired")
            + labs(
                x="Module",
                y="Normalised Questions Answered",
                title="Questions Answered Per Module, Per Month, Normalised by Number of Lessons",
            )
            + theme(figure_size=(10, 12))
        )
        plot6 = (
            ggplot(
                logs[3],
                aes(x="Module", y="Score/Questions*100", fill="Module"),
            )
            + facet_grid(rows="Date")
            + geom_bar(stat="identity", width=0.5, show_legend=False)
            + scale_fill_brewer(type="qual", palette="Paired")
            + labs(
                x="Module",
                y="Percentage",
                title="Percentage Score Per Module, Per Month",
            )
            + ylim((0, 100))
            + theme(figure_size=(10, 12))
        )
        plot7 = (
            ggplot(logs[4], aes(x="Lesson", y="Questions", fill="Module"))
            + facet_grid(rows="Date")
            + geom_bar(stat="identity", width=0.5, show_legend=False)
            + scale_fill_brewer(type="qual", palette="Paired")
            + labs(
                x="Lesson",
                y="Total Questions Answered",
                title="Number of Questions Answered Per Lesson, Per Month",
            )
            + theme(
                figure_size=(10, 12), axis_text_x=element_text(rotation=45, hjust=1)
            )
        )
        plot8 = (
            ggplot(logs[4], aes(x="Lesson", y="Score/Questions*100", fill="Module"))
            + facet_grid(rows="Date")
            + geom_bar(stat="identity", width=0.5, show_legend=False)
            + scale_fill_brewer(type="qual", palette="Paired")
            + labs(
                x="Module",
                y="Percentage",
                title="Percentage Score Per Lesson, Per Month",
            )
            + ylim((0, 100))
            + theme(
                figure_size=(10, 12), axis_text_x=element_text(rotation=45, hjust=1)
            )
        )

        plot5.save(f"{plot_path}plots/progress/5.png", verbose=False)
        plot5a.save(f"{plot_path}plots/progress/5a.png", verbose=False)
        plot6.save(f"{plot_path}plots/progress/6.png", verbose=False)
        plot7.save(f"{plot_path}plots/progress/7.png", verbose=False)
        plot8.save(f"{plot_path}plots/progress/8.png", verbose=False)

        plot9 = (
            ggplot(
                logs[5][logs[5].Year == date.today().strftime("%Y")],
                aes(x="Date", y="Score/Questions*100", fill="Date"),
            )
            + geom_bar(stat="identity", width=0.5, show_legend=False)
            + labs(
                x="Month",
                y="Percentage",
                title="Overall Percentage Score Per Month",
            )
            + ylim((0, 100))
            + theme(figure_size=(10, 6))
        )

        # plot9 = (
        #     ggplot(
        #         logs[5],
        #         aes(x="Date", y="Score/Questions*100", fill="Date"),
        #     )
        #     + facet_grid(rows="Year")
        #     + geom_bar(stat="identity", width=0.5, show_legend=False)
        #     + labs(
        #         x="Month",
        #         y="Percentage",
        #         title="Overall Percentage Score Per Month",
        #     )
        #     + ylim((0, 100))
        #     + theme(figure_size=(10, 6))
        # )

        plot9.save(f"{plot_path}plots/progress/9.png", verbose=False)


## Test Log Figures


def test_log_single():
    pass


def test_log():
    pass


def generate_test_figures(log, single=True):

    with open("settings.txt", "r") as file:
        settings = file.read().splitlines()
        plot_path = settings[1]

    if plot_path and not plot_path.endswith("/"):
        plot_path = plot_path + "/"

    os.makedirs(f"{plot_path}plots/tests", exist_ok=True)

    if single:
        plot1 = (
            ggplot(log, aes("Result", fill="Error"))
            + geom_bar(width=0.5)
            + scale_fill_brewer("qual", "Paired")
            + labs(
                y="Total Questions",
                title="Results of Test",
            )
            + geom_text(
                aes(
                    label=after_stat("count"),
                    y=stage(after_stat="count", after_scale="y+.15"),
                ),
                stat="count",
                position="stack",
            )
        )
        plot1.save(f"{plot_path}plots/tests/1.png", verbose=False)
    else:
        pass


## Generate text for reports


def text_generator(report_title, logs):
    if report_title == "Weekly":
        text = "this week "
    elif report_title == "Monthly":
        text = "this month "
        logs[0] = logs[0][logs[0].Date == date.today().strftime("%B")]
        logs[1] = logs[1][logs[1].Date == date.today().strftime("%B")]
    elif report_title == "Progress":
        text = ""
        logs = logs[1:]
    best_module_idx = logs[0]["Percentage"].idxmax()
    best_module = logs[0]["Module"][best_module_idx]
    module_percentage = logs[0]["Percentage"][best_module_idx]
    modules = []
    for module in logs[0]["Module"]:
        if module != "all":
            log_module = logs[1][logs[1]["Module"] == module]
            best_lesson_idx = log_module["Percentage"].idxmax()
            best_lesson = re.findall(r"\d+", log_module["Lesson"][best_lesson_idx])[0]
            lesson_percentage = log_module["Percentage"][best_lesson_idx]
            line1 = f"   {module.capitalize()}"
            line2 = f"{best_lesson}       {lesson_percentage}%"
            modules.append(line1)
            modules.append(line2)
    full_text = [
        f"Best module {text}is {best_module.capitalize()} with total percentage {module_percentage}%.",
        "Best lesson in each module, with percentage correct, is:",
    ]
    full_text.extend(modules)
    return full_text


if __name__ == "__main__":

    log = pd.read_csv("testing_log.csv")
    logs = log_maker("Weekly", log, debug=True, debug_week=date(2025, 8, 18))
    print(text_generator("Weekly", logs))
    generate_figures("Weekly", logs)

    log2 = pd.read_csv("test_log1.csv")
    generate_test_figures(log2)
