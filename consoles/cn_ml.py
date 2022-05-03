import pandas as pd
from f_ds import u_df
from f_ds import u_rfr


repo = 'D:\\Temp\\write\\220228\\Bi\\'
csv_train = repo + 'train.csv'
csv_test = repo + 'test.csv'
csv_pred = repo + 'pred.csv'

df_train = pd.read_csv(csv_train)
df_test = pd.read_csv(csv_test)

x_train, y_train = u_df.split_to_x_y(df_train, col_label='label')

model = u_rfr.create_model(x_train, y_train, verbose=True)
y_pred = u_rfr.predict(model, df_test)

df_pred = pd.DataFrame(y_pred)
df_pred.to_csv(csv_pred)



