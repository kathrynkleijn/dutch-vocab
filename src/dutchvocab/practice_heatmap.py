import pandas as pd
from plotnine import (
    ggplot,
    aes,
    geom_tile,
    scale_y_reverse,
    labs,
    theme,
    scale_x_continuous,
    element_text,
    element_blank,
    scale_fill_gradient,
    geom_bar,
    coord_flip,
    theme_classic,
    scale_fill_gradientn,
)
from datetime import date, timedelta

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
lessons.append("all")
lessons = lessons[::-1]


log = pd.read_csv("learning_log.csv")
log.Date = pd.to_datetime(log.Date)
log.Lesson = pd.Categorical(log["Lesson"], categories=lessons, ordered=True)

# Heat map

# dayplot

counts = log.groupby("Date").size().reset_index(name="value")

all_days = pd.DataFrame(
    {"Date": pd.date_range(log["Date"].min(), log["Date"].max(), freq="D")}
)
calendar = all_days.merge(counts, on="Date", how="left")
calendar["value"] = calendar["value"].fillna(0)
calendar["value_clipped"] = calendar["value"].clip(upper=20)

calendar["Weekday"] = calendar.Date.dt.weekday
calendar["Week"] = calendar.Date.dt.isocalendar().week.astype(int)

calendar["week_index"] = (calendar["Date"] - calendar["Date"].min()).dt.days // 7

calendar["YearMonth"] = calendar["Date"].dt.to_period("M")
month_breaks = calendar.groupby("YearMonth")["week_index"].min().reset_index()
month_breaks["label"] = month_breaks["YearMonth"].dt.strftime("%b %Y")

plot = (
    ggplot(calendar, aes("week_index", "Weekday", fill="value_clipped"))
    + geom_tile(width=0.9, height=0.9, color="white")
    + scale_y_reverse(
        breaks=list(range(7)), labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    )
    + scale_x_continuous(
        breaks=month_breaks["week_index"].tolist(),
        labels=month_breaks["label"].tolist(),
        expand=(0, 0),
    )
    + scale_fill_gradient(
        low="#E0DEDE",
        high="#800026",
        limits=(0, 20),
        breaks=[0, 5, 10, 15, 20],
        labels=["0", "5", "10", "15", "20+"],
    )
    + labs(x="", y="")
    + theme(
        figure_size=(10, 2),
        axis_text_x=element_text(rotation=45, hjust=1),
        legend_key_height=90,
        legend_key_width=10,
        legend_title=element_blank(),
    )
)
plot.save("heatmap.png", verbose=False)


# Bar chart


ave_log = log.groupby(["Module", "Lesson"], observed=True).agg(
    Questions=("Questions", "sum"), Score=("Score", "sum")
)
ave_log["Percentage"] = ave_log.apply(
    lambda row: round(row["Score"] / row["Questions"] * 100, 1), axis=1
)
percentage_log = ave_log.reset_index()[["Module", "Lesson", "Percentage"]]

merged = log.merge(percentage_log, on=["Module", "Lesson"], how="left")


plot = (
    ggplot(merged, aes("Lesson", fill="Percentage"))
    + geom_bar(width=0.75)
    + coord_flip()
    + theme_classic()
    + theme(figure_size=((4.5, 6)))
    + labs(y="Number of lessons")
    + scale_fill_gradientn(
        colors=["red", "red", "cornsilk", "royalblue", "royalblue"],
        values=[0.0, 0.5, 0.7, 0.9, 1.0],
        limits=[0, 100],
    )
)
plot.save("lesson_count.png", verbose=False)

question_log = ave_log.reset_index()[["Module", "Lesson", "Questions", "Percentage"]]

plot = (
    ggplot(question_log, aes(y="Questions", x="Lesson", fill="Percentage"))
    + geom_bar(stat="identity", width=0.75)
    + coord_flip()
    + theme_classic()
    + theme(figure_size=((4.5, 6)))
)
plot.save("question_count.png", verbose=False)
