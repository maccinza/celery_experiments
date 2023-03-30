from collections import defaultdict
from csv import DictReader
import click
from datetime import datetime
from pathlib import Path
import json

import matplotlib.pyplot as plt

from utils.log import get_logger

logger = get_logger(__name__)


def parse_data(path):
    logger.info("Parsing data...")
    parsed_data = defaultdict(list)

    with open(path, encoding="utf-8") as input_data:
        reader = DictReader(input_data, delimiter=",")
        for row in reader:
            if row["PID"] == "PID":
                continue
            parsed_data[row["PID"]].append({
                "datetime": f"{row['DATE']}T{row['TIME']}",
                "cpu": float(row["CPU"]),
                "rss": int(row["RSS"]),
            })

    return parsed_data


def clean_data(parsed_data, directory):
    logger.info("Cleaning data...")

    cleaned_data = defaultdict(list)
    to_remove = defaultdict(list)

    for pid, data in parsed_data.items():
        previous_index = 0
        for i in range(1, len(data) - 1):
            current_index = i
            conditions = [
                data[current_index]["cpu"] == data[previous_index]["cpu"],
                data[current_index]["rss"] == data[previous_index]["rss"],
            ]
            if all(conditions):
                to_remove[pid].append(current_index)
            else:
                previous_index = current_index

    for pid, data in parsed_data.items():
        if pid in to_remove:
            cleaned_data[pid] = [
                d for _index, d in enumerate(data) if _index not in to_remove[pid]
            ]
        else:
            cleaned_data[pid] = data

    with open(f"{directory}/cleaned_data.json", "w") as ofile:
        ofile.write(json.dumps(cleaned_data, indent=2))

    return cleaned_data


def plot_data(data, directory):
    logger.info("Plotting data and saving file...")
    for pid, dataset in data.items():
        figure, main_ax = plt.subplots()
        figure.subplots_adjust(right=0.75)

        twin_ax = main_ax.twinx()
        main_ax.set_title(f"PID {pid}")

        time_data = [datetime.strptime(d["datetime"], "%Y-%m-%dT%H:%M:%S") for d in dataset]
        cpu_data = [d["cpu"] for d in dataset]
        rss_data = [d["rss"] for d in dataset]

        rss_plot, = main_ax.plot(time_data, rss_data, "g-", label="RSS")
        cpu_plot, = twin_ax.plot(time_data, cpu_data, "r-", alpha=0.7, label="CPU")

        figure.autofmt_xdate()

        main_ax.set_xlabel("datetime")
        main_ax.set_ylabel("RSS (kB)")
        twin_ax.set_ylabel("CPU (%)")

        main_ax.yaxis.label.set_color(rss_plot.get_color())
        twin_ax.yaxis.label.set_color(cpu_plot.get_color())

        tkw = dict(size=4, width=1.5)
        main_ax.tick_params(axis='y', colors=rss_plot.get_color(), **tkw)
        twin_ax.tick_params(axis='y', colors=cpu_plot.get_color(), **tkw)
        main_ax.tick_params(axis='x', **tkw)

        main_ax.legend(handles=[rss_plot, cpu_plot])

        plt.savefig(f"{directory}/plot-{pid}.png")


@click.command()
@click.option("--path",  required=True, type=str)
def main(path):
    directory = Path(path).parent
    parsed_data = parse_data(path)
    cleaned_data = clean_data(parsed_data, directory)
    plot_data(cleaned_data, directory)


if __name__ == "__main__":
    main()
