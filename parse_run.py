from concurrent.futures import ProcessPoolExecutor, as_completed
import re
from datetime import datetime
import pandas as pd
from tqdm.notebook import tqdm

event_pattern = r"^.*(?:\d{4}-\d{2}-\d{2})?(\d{2}:\d{2}:\d{2})(?:,\d+)?.*start processing event #\d+, run #\d+.*"

def _parse_run(run):
    log_file = run / "log.RAWtoALL"
    # print(run.name)
    if log_file.exists():
        logs = list(run.glob("athenaMP*/worker_*/AthenaMP.log"))
    else:
        # print(run)
        logs = list(run.glob("proc_*/log.RAWtoALL"))

    timestamps = []
    count = []

    day = None

    if len(logs) == 0:
        # parse from main file
        # print("MAIN", log_file)
        with log_file.open("r") as f:
            for line in f:
                if day is None:
                    # 16:31:42 Fri Jun 13 16:31:42 CEST 2025
                    # print(line)
                    match = re.match(
                        r"^(\d{2}:\d{2}:\d{2}) (Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{2}) .* (\d{4})",
                        line,
                    )
                    if match is not None:
                        (
                            time_str,
                            _,
                            month,
                            day,
                            year,
                        ) = match.groups()
                        day = datetime.strptime(f"{day} {month} {year}", "%d %b %Y")

                match = re.match(event_pattern, line)
                if match is not None:
                    (time,) = match.groups()
                    hours, minutes, seconds = map(int, time.split(":"))
                    timestamp = day.replace(hour=hours, minute=minutes, second=seconds)
                    timestamps.append(timestamp)
                    count.append(1)

    else:
        for log in logs:
            with log.open("r") as f:
                for line in f:
                    if day is None:
                        # 16:31:42 Fri Jun 13 16:31:42 CEST 2025
                        # print(line)
                        match = re.match(
                            r"^(\d{2}:\d{2}:\d{2}) (Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{2}) .* (\d{4})",
                            line,
                        )
                        if match is not None:
                            (
                                time_str,
                                _,
                                month,
                                day,
                                year,
                            ) = match.groups()
                            day = datetime.strptime(f"{day} {month} {year}", "%d %b %Y")
                    match = re.match(event_pattern, line)
                    if match is not None:
                        if day is None:
                            m = re.match(r"^(\d{4})-(\d{2})-(\d{2}).*", line)
                            if m is None:
                                raise ValueError(
                                    "Have no day yet but encountered event"
                                )
                            year, month, day = map(int, m.groups())
                            day = datetime(year=year, month=month, day=day)
                        (time,) = match.groups()
                        hours, minutes, seconds = map(int, time.split(":"))
                        timestamp = day.replace(
                            hour=hours, minute=minutes, second=seconds
                        )
                        # print(timestamp)
                        timestamps.append(timestamp)
                        count.append(1)
                        # print(match.group(0))
    events_df = pd.DataFrame(
        data={"timestamp": pd.to_datetime(timestamps), "count": count}
    )
    events_df = events_df.sort_values(by="timestamp")
    events_df["events_done"] = events_df["count"].cumsum()
    events_df.index = events_df["timestamp"]

    return run, events_df

def parse_runs(runs, n=None):
    with ProcessPoolExecutor(max_workers=n) as executor:
        futures = [executor.submit(_parse_run, run) for run in runs]
        parsed_runs = []
        for _ in tqdm(as_completed(futures), total=len(futures)):
            pass

        for future in futures:
            run, events_df = future.result()
            parsed_runs.append((run, events_df))
        return parsed_runs