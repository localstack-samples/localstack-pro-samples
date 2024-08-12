from pyspark.sql import SparkSession
from pyspark.sql.functions import col

class SparkRun:

    def __init__(self) -> None:
        self.spark = SparkSession.builder.appName("ExtremeWeather").getOrCreate()

    def run(self) -> None:
        df = self.spark.createDataFrame(
            [
                ("sue", 32),
                ("li", 3),
                ("bob", 75),
                ("heo", 13),
            ],
            ["first_name", "age"],
        )
        print(df.select(col("first_name"), col("age")).first())

    def stop(self):
        self.spark.stop()