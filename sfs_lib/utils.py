import pandas as pd

def clean_execution_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and formats the execution report DataFrame.
    
    Returns a new cleaned DataFrame.
    """

    df = df.copy()  # important: avoid mutating original df

    # Drop unwanted columns
    df.drop(
        columns=[
            "CreatedBy",
            "ModifiedBy",
            "CreatedDate",
            "ModifiedDate",
        ],
        errors="ignore",
        inplace=True,
    )

    # Convert datetime columns
    df["StartTime"] = pd.to_datetime(
        df["StartTime"], format="%d-%m-%Y %H:%M", errors="coerce"
    )
    df["EndTime"] = pd.to_datetime(
        df["EndTime"], format="%d-%m-%Y %H:%M", errors="coerce"
    )

    # Convert elapsed time (seconds → HH:MM:SS)
    df["ElapsedTime"] = pd.to_timedelta(
        pd.to_numeric(df["ElapsedTime"], errors="coerce"), unit="s"
    )
    df["ElapsedTime"] = (
        df["ElapsedTime"]
        .astype(str)
        .str.split(".").str[0]
        .str.split(" ").str[-1]
    )

    # Extract execution date from Title
    df["Execution Date"] = (
        df["Title"]
        .str.split(" - ").str[1]
        .str.rsplit(" ", n=1).str[0]
    )

    # Drop Title column
    df.drop(columns=["Title"], errors="ignore", inplace=True)

    # Rename columns
    df.rename(
        columns={
            "StartingProcessName": "Process Name",
            "StartTime": "Start Time",
            "EndTime": "End Time",
            "ElapsedTime": "Elapsed Time",
        },
        inplace=True,
    )

    # Format time columns
    df["Start Time"] = df["Start Time"].dt.strftime("%H:%M:%S")
    df["End Time"] = df["End Time"].dt.strftime("%H:%M:%S")

    return df

def duplicate_tcs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract the dataframe which has more than once duplicate Process Name

    """
    df = df.copy()

    duplicates=df[df.duplicated(subset=['Process Name'], keep=False)]

    return duplicates


from typing import List, Dict, Tuple

def get_duplicate_summary(df: pd.DataFrame, group_col: str = 'Process Name') -> Tuple[Dict[int, pd.DataFrame], pd.DataFrame]:
    """
    Computes duplicates for a DataFrame based on a grouping column.

    Returns:
    1. dup_dict: dictionary where key = number of duplicates, value = DataFrame of rows with that many duplicates
    2. summary_df: DataFrame summarizing count of test cases for each duplicate count

    Example usage:
        dup_dict, summary_df = get_duplicate_summary_generic(df)
        dup_dict[5]  # all rows executed 5 times
        summary_df  # summary of all duplicate counts
    """

    df = df.copy()

    # Add a column with duplicate count
    df['dup_counts'] = df.groupby(group_col)[group_col].transform('size')

    # Get all unique duplicate counts
    unique_counts = sorted(df['dup_counts'].unique(), reverse=True)

    # Create dictionary for all duplicate counts
    dup_dict = {count: df[df['dup_counts'] == count] for count in unique_counts}

    # Optional: print summary
    print("Duplicate summary:")
    for count, subset in dup_dict.items():
        print(f"Test cases executed {count} times = {subset.shape[0]}")

    # Create a summary DataFrame
    summary_df = pd.DataFrame({
        'Duplicate Count': list(dup_dict.keys()),
        'Number of Test Cases': [subset.shape[0] for subset in dup_dict.values()]
    }).sort_values(by='Duplicate Count', ascending=False).reset_index(drop=True)

    return dup_dict, summary_df


