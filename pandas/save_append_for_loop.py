import time
from datetime import datetime

import pandas as pd


csv_loc = "record.csv"


df = pd.DataFrame(columns=["column1", "column2"])
df.to_csv(csv_loc, index=False)
for i in range(30):
    _df = []
    _df.append(
        {
            "column1": datetime.now().strftime("%H:%M:%S.%f"),
            "column2": datetime.now().strftime("%H:%M:%S.%f"),
        }
    )
    _df = pd.DataFrame(_df)
    _df.to_csv(csv_loc, mode="a", index=False, header=False)


df_record = pd.read_csv(csv_loc)
df_record.head(10)
#   column1       column2
# 0	02:51:59.382818	02:51:59.382849
# 1	02:51:59.384701	02:51:59.384726
# 2	02:51:59.386448	02:51:59.386471
# 3	02:51:59.387895	02:51:59.387918
# 4	02:51:59.389248	02:51:59.389270
# 5	02:51:59.391366	02:51:59.391384
# 6	02:51:59.392329	02:51:59.392356
# 7	02:51:59.393255	02:51:59.393271
# 8	02:51:59.394153	02:51:59.394169
# 9	02:51:59.395051	02:51:59.395067
