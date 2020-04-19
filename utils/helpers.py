import pandas as pd


def append_score(s_df, score):
    if s_df is None:
        s_df = pd.DataFrame(columns=list(score))
    return s_df.append(score, ignore_index=True)
