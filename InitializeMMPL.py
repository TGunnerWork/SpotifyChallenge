import json
import pandas as pd
import os
import sqlite3
from tqdm import tqdm

columns = ["pl_pid",
           "pl_name",
           "pos",
           "track_name",
           "artist_name",
           "track_uri",
           "artist_uri"]

meta = ["name",
        "pid"]

dtypes = {"pl_pid": int,
          "pl_name": str,
          "pos": int,
          "track_name": str,
          "artist_name": str,
          "track_uri": str,
          "artist_uri": str}

cwd = os.getcwd()

with sqlite3.connect("Spotify.db") as conn:

    # Create tables
    print("Creating Database Tables...")
    with open("Queries/CreateTables.sql", "r") as script_file:
        conn.cursor().executescript(script_file.read())

    # Change directory for processing
    os.chdir("SourceData/spotify_million_playlist_dataset/data")

    # Import data into DB
    for json_file in tqdm(
            os.listdir(),
            desc="Importing JSONs...",
            unit="JSON file"):

        with open(json_file, "r") as file:
            pd.json_normalize(
                json.load(file)["playlists"],
                record_path="tracks",
                meta=meta,
                meta_prefix="pl_",
                errors="ignore"
            )[columns].to_sql(
                "RawData",
                conn,
                if_exists="append",
                index=False)

            conn.commit()

    # Go back to working directory
    os.chdir(cwd)

    # Normalize and index database tables
    with open("Queries/Normalize.sql", "r") as script_file:
        print("Normalizing and Indexing Database...")
        conn.cursor().executescript(script_file.read())
