"""Calculate gaps between consecutive video files"""
import glob
import os
import pdb
import sys
from argparse import ArgumentParser
from datetime import datetime, timedelta
from pathlib import Path

import cv2
import pandas as pd


def create_sorted_df(folder_path: str) -> pd.DataFrame:
    """Given folder of .mkv files sort then in date order and populate a dataframe
    with the columns:

                 datestring  filepaths               datetimes
    3  23-04-13_21-50-27-63  xxxpath1 2023-04-13 21:50:27.630
    2  23-04-13_21-52-01-19  xxxpath2 2023-04-13 21:52:01.190
    1  23-04-13_21-55-01-20  xxxpath3 2023-04-13 21:55:01.200

    :param folder_path: the path to folder containing .mkv exported by AXIS to FTP/SFTP server
    """
    glob_string = os.path.join(folder_path, "*.mkv")
    files = glob.glob(glob_string)
    base_filenames = [os.path.basename(fn)[:-10].split("video")[1] for fn in files]
    df = pd.DataFrame(base_filenames, columns=["datestring"])
    df["filepaths"] = files
    df["datetimes"] = df["datestring"].apply(
        lambda dt: datetime.strptime(dt, "%y-%m-%d_%H-%M-%S-%f"))
    df = df.sort_values("datetimes")
    return df


def print_gaps(df: pd.DataFrame) -> None:
    """Prints the gaps between each file, and export a .csv summarising the findings.

    :param df: A pandas dataframe with files sorted by datetime
    """
    gaps = []
    old_datetime_at_end_of_video = None
    for index, row in df.iterrows():
        filename = row["filepaths"]
        start_datetime = row["datetimes"]
        print(f"Loading filename: {Path(filename).name} starts at {start_datetime}. ")

        if old_datetime_at_end_of_video is not None:
            print(f"The previous file ended on timestamp {old_datetime_at_end_of_video} "
                  f"so we lost {start_datetime - old_datetime_at_end_of_video} seconds "
                  f"of video.")
            gaps.append((start_datetime - old_datetime_at_end_of_video).seconds)

        cap = cv2.VideoCapture(filename)
        frame_count = 0

        while True:
            ret, img = cap.read()
            if not ret:
                break
            frame_count += 1
            cv2.imshow("img", img)
            k = cv2.waitKey(1)
            if ord("q") == k:
                break
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps != 30:
            raise UserWarning("This script currently assumes 30 FPS")
        seconds = frame_count / 30
        print(f"{filename} had: {frame_count} frames which is {seconds:.2f} seconds duration.")
        old_datetime_at_end_of_video = start_datetime + timedelta(seconds=seconds)
        cv2.destroyAllWindows()
    print("Gaps were", gaps)
    pd.Series(gaps).to_csv("gaps.csv")


def main():
    """Perform analysis of the file gaps."""
    parser = ArgumentParser()
    parser.add_argument("--path", "-path",
                        default="/data/confidential/kvstreamer/sftp-3spost-30spost-30spulse/output",
                        type=str)
    args = parser.parse_args()
    df = create_sorted_df(args.path)
    print_gaps(df)


if __name__ == '__main__':
    main()
