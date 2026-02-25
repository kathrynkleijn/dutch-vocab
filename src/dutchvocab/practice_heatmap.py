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
)
from matplotlib import pyplot as plt
from datetime import date, timedelta

log = pd.read_csv("learning_log.csv")
log.Date = pd.to_datetime(log.Date)

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
