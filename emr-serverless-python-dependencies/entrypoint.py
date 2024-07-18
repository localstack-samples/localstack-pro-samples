from jobs.spark_run import SparkRun

# importing typer to validate it is in the environment
import typer

if __name__ == "__main__":
    spark_runner = SparkRun()
    spark_runner.run()
    spark_runner.stop()
