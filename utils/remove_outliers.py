import faiss
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from server.db import create_db

db = create_db()
for user_id in db.get_user_ids():
    print(user_id)
    user_metrix = list(db.get_all_metrix_by_user_id(user_id))
    df = pd.DataFrame(user_metrix)
    df = df.drop("user_id", axis="columns")
    try:
        df = df.drop("_id", axis="columns")
    except KeyError:
        pass
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
    db.remove_metrix_by_session_ids(outliers)
    print("Hotovo")
