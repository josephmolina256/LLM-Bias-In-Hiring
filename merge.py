import pandas as pd

# merge all /results/*_final.csv files into one dataframe
import glob
def merge_results():
    all_files = glob.glob("results/*_final.csv")
    df_list = []
    for file in all_files:
        df = pd.read_csv(file)
        df_list.append(df)
    merged_df = pd.concat(df_list, ignore_index=True)
    merged_df.to_csv("results/merged_results_final.csv", index=False)
    print(f"Merged {len(all_files)} files into results/merged_results_final.csv with {len(merged_df)} rows.")

if __name__ == "__main__":
    merge_results()