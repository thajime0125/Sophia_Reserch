import pandas as pd

TEST_CSV_PATH = "data/telop_info.csv"
# columns=["frame", "inning", "base", "count", "score"]

def define_highlight(df):

    now_score = df.iloc[0]["score"]
    for row in df.iterrows():

        # define get point scene
        if now_score != row[1]["score"]:
            print(row[1][["frame", "score"]])
            now_score = row[1]["score"]
        
        
    
    return


def indexing_frame(df):
    
    before_frame = df.iloc[0].to_list()
    indexing_df = pd.DataFrame()
    for _, row in df.iterrows():
        now_frame = row.to_list()
        if now_frame[1:] != before_frame[1:]:
            before_frame = now_frame
            indexing_df = indexing_df.append(row, ignore_index=True, sort=False)
    return indexing_df


if __name__ == "__main__":
    df = indexing_frame(pd.read_csv(TEST_CSV_PATH))
    print(df)
    # print(df["inning"].value_counts())
    # define_highlight(df)
