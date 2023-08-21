from src.util.exception_and_logging.handle_exception import ExceptionHandler


def check_input_csv(df_csv, columns):
    """ This function checks if the input csv file has data and has all the required columns """
    # check if the input csv has data
    with ExceptionHandler("Empty input csv file"):
        if df_csv.shape[0] < 1:
            raise ValueError("Empty input csv file")

    # check if all required columns are in the csv file
    with ExceptionHandler("Missing column name(s) in the csv files"):
        for key in columns:
            if key not in df_csv.columns:
                raise ValueError(f"Input csv file missing column {key}")
