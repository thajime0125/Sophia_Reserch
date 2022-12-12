import pandas as pd

TEST_CSV_PATH = "data/telop_info.csv"
# columns=["frame", "inning", "base", "count", "score"]


def define_highlight(df):

    highlight_point = pd.concat(
        [df['frame'], pd.Series([0] * len(df), name='point')], axis=1)

    now_score = df.iloc[0]["score"]
    now_base = df.iloc[0]["base"]
    for index, row in df.iterrows():

        # define get point scene
        if now_score != row["score"]:
            if now_score == "[0, 0]": # first point
                highlight_point.loc[index-1, "point"] += 3
            if row["base"] == "[0, 0, 0]": # homerun
                highlight_point.loc[index-1, "point"] += 2
            now_score = row["score"]
            highlight_point.loc[index-1, "point"] += 1

        # define get base scene
        if now_base != row["base"]:
            now_base = row["base"]
            if sum(eval(row["base"])) > 1: # chance
                highlight_point.loc[index, "point"] += 1
            # highlight_point.loc[index-1, "point"] += 1

    # define end of game scene
    highlight_point.loc[index, "point"] += 10

    return highlight_point[highlight_point["point"] > 0].sort_values("point", ascending=False)


def indexing_frame(df):

    before_frame = df.iloc[0].to_list()
    indexing_df = pd.DataFrame()
    for _, row in df.iterrows():
        now_frame = row.to_list()
        if now_frame[1:] != before_frame[1:]:
            before_frame = now_frame
            indexing_df = indexing_df.append(
                row, ignore_index=True, sort=False)
    indexing_df = indexing_df.append(
        row, ignore_index=True, sort=False)

    return indexing_df


if __name__ == "__main__":
    df = indexing_frame(pd.read_csv(TEST_CSV_PATH))
    # print(df[df["frame"] > 32000])
    # print(df["inning"].value_counts())
    point = define_highlight(df)
    print(point)
