import time

import pandas as pd

from server.config import config
from utils.evaluation import evaluation

score_df = None
for features_index in range(len(config.FEATURE_SELECTION)):
    for threshold in range(12, 24):
        for neighbours in range(1, 6):
            print(
                f"Feature group: {features_index}\nThreshold: {threshold}\nK neighbours: {neighbours}\n-------------------------------------")
            result = evaluation(features=features_index, threshold=threshold, neighbours=neighbours, processes=15)
            print(f"{result.mean()}\n=====================================")
            if score_df is not None:
                score_df = score_df.append(result.mean(), ignore_index=True)
            else:
                score_df = pd.DataFrame(result.mean()).transpose()

score_df.to_csv(rf'cv_evaluation_{time.strftime("%Y%m%d-%H%M%S")}.csv', index=False)
print(score_df.mean().rename('Mean'))
