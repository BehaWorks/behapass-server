import faiss
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def remove_outliers(user_metrix):
    # user_metrix = list(db.get_all_metrix_by_user_id(user_id))
    df = pd.DataFrame(user_metrix)
    df = df.drop("user_id", axis="columns")
    try:
        df = df.drop("_id", axis="columns")
    except KeyError:
        pass
    df.dropna(inplace=True)
    session_ids = df.pop("session_id")
    index = faiss.IndexFlatL2(len(df.columns))
    scaler = StandardScaler()
    index.add(np.ascontiguousarray(scaler.fit_transform(df.to_numpy("float32"))))
    # for user_metric in user_metrix:
    distances, indices = index.search(np.ascontiguousarray(scaler.transform(df.to_numpy("float32"))), len(user_metrix))
    averages = [np.average(distance) for distance in distances]
    threshold = np.quantile(averages, 0.75) * 2
    outliers = []
    for id, value in enumerate(averages):
        if value > threshold:
            outliers.append(session_ids[id])

    df = df.join(session_ids)
    df = df[~df['session_id'].isin(outliers)]
    return df
