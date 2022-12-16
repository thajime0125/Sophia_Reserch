import pandas as pd

TEST_CSV_PATH = "data/telop_info.csv"
# columns=["frame", "inning", "base", "count", "score"]


def define_highlight(df):

    highlight_point = pd.concat(
        [df['frame'], pd.Series([0] * len(df), name='point')], axis=1)

    now_score = df.iloc[0]["score"]
    now_base = df.iloc[0]["base"]
    for index, row in df.iterrows():
        if index == 46:
            continue

        # define get point scene
        if now_score != row["score"]:
            if now_score == "[0, 0]": # first point
                highlight_point.loc[index-1, "point"] += 3
            if row["base"] == "[0, 0, 0]": # homerun
                highlight_point.loc[index-1, "point"] += 3
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
        batter_change = False
        if eval(now_frame[3])[2] != eval(before_frame[3])[2]:
            batter_change = True
        elif now_frame[2] != before_frame[2]:
            batter_change = True
        elif now_frame[4] != before_frame[4]:
            batter_change = True
        if batter_change:
            before_frame = now_frame
            indexing_df = indexing_df.append(
                before_row, ignore_index=True, sort=False)
        before_row = row
    indexing_df = indexing_df.append(
        row, ignore_index=True, sort=False)

    return indexing_df


if __name__ == "__main__":
    df = indexing_frame(pd.read_csv(TEST_CSV_PATH))
    # print(df[30:50])
    # print(df[df["frame"] > 32000])
    # print(df["inning"].value_counts())
    point = define_highlight(df)
    print(point)
