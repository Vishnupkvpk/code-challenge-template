import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import logging
from typing import Optional
from datetime import datetime

load_dotenv()

class WeatherDataIngestor:
    """
    Class for ingesting weather data files into a database, checking for duplicates.
    """

    def __init__(self, db_url: str, table_name: str, file_extension: str = ".txt"):
        """
        :param db_url: Database connection URL
        :param table_name: Name of the database table
        :param file_extension: Extension of the weather data files
        """
        self.db_url = db_url
        self.table_name = table_name
        self.file_extension = file_extension
        self.engine = create_engine(db_url, pool_size=5, max_overflow=10)

        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    def read_weather_file(self, file_path: str) -> Optional[pd.DataFrame]:
        """
        :param file_path: Path to the weather data file
        :return: Cleaned DataFrame or None if an error occurs
        """
        try:
            self.logger.debug(f"Reading file: {file_path}")
            df = pd.read_csv(
                file_path,
                sep="\t",
                header=None,
                names=["date", "max_temp", "min_temp", "precipitation"],
            )
            df["date"] = pd.to_datetime(df["date"], format="%Y%m%d", errors="coerce")
            df["station_id"] = os.path.splitext(os.path.basename(file_path))[0]
            df = df.replace(-9999, pd.NA)

            # Drop rows with invalid dates
            df = df.dropna(subset=["date"])
            self.logger.info(f"Processed file: {file_path} with {len(df)} valid records.")
            return df
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {e}")
            return None

    def check_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Check for duplicates in the data based on station_id and date.
        :param df: DataFrame to check for duplicates
        :return: DataFrame with duplicates removed
        """
        with self.engine.connect() as conn:
            # Check for existing records in the database
            existing_records = pd.read_sql(
                f"SELECT station_id, date FROM {self.table_name}", conn
            )
            
            # Ensure 'date' columns are of the same type for both DataFrames
            existing_records['date'] = pd.to_datetime(existing_records['date'], errors='coerce')
            df['date'] = pd.to_datetime(df['date'], errors='coerce')

            # Merge and remove duplicates
            df = df.merge(existing_records, on=["station_id", "date"], how="left", indicator=True)
            df = df[df["_merge"] == "left_only"].drop(columns="_merge")
            return df


    def ingest_data_to_db(self, df: pd.DataFrame):
        """
        :param df: DataFrame to ingest
        """
        try:
            self.logger.info(f"Ingesting {len(df)} records into table {self.table_name}.")
            with self.engine.begin() as conn:
                df.to_sql(
                    self.table_name,
                    conn,
                    if_exists="append",
                    index=False,
                    method="multi",
                )
            self.logger.info(f"Successfully ingested {len(df)} records.")
        except SQLAlchemyError as e:
            self.logger.error(f"Database ingestion failed: {e}")

    def process_file(self, file_path: str):
        """
        :param file_path: Path to the file
        """
        df = self.read_weather_file(file_path)
        if df is not None and not df.empty:
            # Check for duplicates before ingesting
            df = self.check_duplicates(df)
            if not df.empty:
                self.ingest_data_to_db(df)
            else:
                self.logger.warning(f"No new data found in file: {file_path}")
        else:
            self.logger.warning(f"No valid data found in file: {file_path}")

    def process_directory(self, directory_path: str):
        """
        :param directory_path: Path to the directory
        """
        start_time = datetime.now()
        self.logger.info(f"Started processing directory at {start_time}.")
        self.logger.info(f"Processing directory: {directory_path}")

        if not os.path.isdir(directory_path):
            self.logger.error(f"Provided path is not a directory: {directory_path}")
            return

        files = [
            f for f in os.listdir(directory_path) if f.endswith(self.file_extension)
        ]
        if not files:
            self.logger.warning(f"No files with extension {self.file_extension} found.")
            return

        total_records_ingested = 0

        for file in files:
            file_path = os.path.join(directory_path, file)
            df = self.read_weather_file(file_path)
            if df is not None and not df.empty:
                # Check for duplicates before ingesting
                df = self.check_duplicates(df)
                if not df.empty:
                    self.ingest_data_to_db(df)
                    total_records_ingested += len(df)

        end_time = datetime.now()
        self.logger.info(f"Finished processing directory at {end_time}.")
        self.logger.info(f"Total records ingested: {total_records_ingested}")
        
if __name__ == "__main__":
    DB_URL = os.getenv(
        "DATABASE_URL", "postgresql+psycopg2://postgres:postgres123@localhost:5432/weather_analysis"
    )
    DATA_DIRECTORY = os.getenv("DATA_DIRECTORY", "/path/to/data")
    TABLE_NAME = "weather"

    ingestor = WeatherDataIngestor(db_url=DB_URL, table_name=TABLE_NAME)
    ingestor.process_directory(DATA_DIRECTORY)
