import pandas as pd
import glob
from pathlib import Path
import re
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np


def get_id(dispositif="ceinture"):
    """return a list of the ids of the patients"""

    path = rf'C:\ecg\rr_{dispositif}'
    id = []
    files = Path(path).glob('*.csv')  # .rglob to get subdirectories
    for f in files:
        m = re.search("([0-9]+)", str(f))
        id.append(m.group(0))
    tab = pd.DataFrame(columns=['id'])
    a = tab['id'] = id
    return a


def create_df_ceinture():
    """return a DF with ceinture datas for all patients"""

    path = r'C:\ecg\rr_ceinture'  # Get data file names
    filenames = glob.glob(path + "/*.csv")
    id = get_id("ceinture")

    dfs = []  # Read the files
    j = 0
    for filename in filenames:
        data = pd.read_csv(filename)
        data.sort_values(by=["timestamp_machine"], inplace=True)
        # print(data["timestamp_machine"])
        data["timestamp_machine"] -= data["timestamp_machine"].min()  # on fait démarrer les ts à zero
        i = [id[j]] * len(data)
        data['id'] = i
        j += 1
        dfs.append(data)

    df = pd.concat(dfs, ignore_index=True)  # Concatenate all datas into one DataFrame
    df.rename(columns={"timestamp_machine": "ts_machine", "timestamp_google": "ts_google" }, inplace = True)
    print("DataFrame ceinture créé")
    return df


def create_df_garmin():
    """return a DF with garmin datas for all patients (rr repetition has been removed)"""

    path = r'C:\ecg\rr_garmin'  # Get data file names
    filenames = glob.glob(path + "/*.csv")
    id = get_id("garmin")

    dfs = []  # Read the files
    j = 0
    for filename in filenames:
        data = pd.read_csv(filename)
        i = [id[j]] * len(data)
        data['id'] = i
        j += 1
        dfs.append(data)

    df = pd.concat(dfs, ignore_index=True)  # Concatenate all data into one DataFrame
    print("DataFrame garmin créé")

    result = df[df.rr.shift() != df.rr]  # remove rr repetitions
    return result


def export(df, title):
    """ Export DataFrame to CSV """

    filepath = Path(f'C:/ecg/to_csv/{title}.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, sep=',')


def create_df_stats(df_c, df_g):
    """Create big DF with statistical infos on ceinture and garmin"""

    id = get_id("ceinture")  # create first column (id)
    tab = pd.DataFrame(columns=['id'])
    tab['id'] = id

    for i in range(0, len(id)):
        a = df_c['rr'].loc[df_c['id'] == id[i]]
        tab.loc[tab['id'] == id[i], 'somme RR (s)'] = f'{a.sum() / 1000}'
        b = df_c['ts_machine'].loc[df_c['id'] == id[i]]
        tab.loc[tab['id'] == id[i], 'durée enregistrement (s)'] = f"{((b.max() - b.min()) / 1000)}"
        tab.loc[tab['id'] == id[i], 'moyenne RR (ms)'] = f"{a.mean()}"
    print(tab.head())

    # Create tab stats garmin
    tab2 = pd.DataFrame(columns=['id'])
    tab2['id'] = id

    for i in range(0, len(id)):
        c = df_g['rr'].loc[df_g['id'] == id[i]]
        tab2.loc[tab2['id'] == id[i], 'somme RR (s)'] = f'{c.sum() / 1000}'
        d = df_g['ts_machine'].loc[df_g['id'] == id[i]]
        tab2.loc[tab2['id'] == id[i], 'durée enregistrement (s)'] = f"{((d.max() - d.min()) / 1000)}"
        tab2.loc[tab2['id'] == id[i], 'moyenne RR (ms)'] = f"{c.mean()}"
    # concatenate both df
    return pd.concat([tab2, tab], axis=1)


def visualisation(dataframe, id : int):
    """visualize with plotly"""

    df_sort = dataframe.sort_values("ts_machine")
    df = df_sort[['rr', 'ts_machine']].loc[df_sort['id'] == id]
    fig = px.line(df, x="ts_machine", y="rr", title="RR de l'ID " + str(id))
    fig.show()


def multiple_matplot(df_c, n1 : int, n2 : int):
    """visualize rr_ceinture of two patients"""
    id = get_id("ceinture")
    print(id)
    df1 = df_c[["rr", "ts_machine"]].loc[df_c["id"] == id[n1]]
    df2 = df_c[["rr", "ts_machine"]].loc[df_c["id"] == id[n2]]

    # fig1
    x1 = df1["ts_machine"]/1000
    x2 = df2["ts_machine"]/1000
    y1 = df1["rr"]
    y2 = df2["rr"]

    fig, ax = plt.subplots(2, 1)

    ax[0].plot(x1, y1)
    ax[1].plot(x2, y2)
    ax[0].set_title(f"patient {id[n1]}")
    ax[1].set_title(f"patient {id[n2]}")
    ax[0].set_xlim(0, max(df1["ts_machine"].max(), df2["ts_machine"].max())/1000)
    #ax[0].set_ylim(0, max(df1["rr"].max(), df2["rr"].max()))
    ax[0].set_ylim(0, 1400)
    ax[1].set_xlim(0, max(df1["ts_machine"].max(), df2["ts_machine"].max())/1000)
    #ax[1].set_ylim(0, max(df1["rr"].max(), df2["rr"].max()))
    ax[1].set_ylim(0, 1400)
    ax[0].set_xlabel("time (ms)")
    ax[0].set_ylabel("rr (ms)")
    ax[1].set_xlabel("time (ms)")
    ax[1].set_ylabel("rr (ms)")
    fig.tight_layout()

    plt.show()


def matplot_c_g(dfceinture, dfgarmin, n: int):
    """visualize rr_ceinture and rr_garmin of one patient"""
    df_c = dfceinture.sort_values(by="ts_machine", ascending=True)
    df_g = dfgarmin.sort_values(by="ts_machine", ascending=True)
    id = get_id("ceinture")
    print(id)
    df1 = df_c[["rr", "ts_machine"]].loc[df_c["id"] == id[n]]
    df2 = df_g[["rr", "ts_machine"]].loc[df_g["id"] == id[n]]
    x1 = df1["ts_machine"] / 1000
    x2 = df2["ts_machine"] / 1000
    y1 = df1["rr"]
    y2 = df2["rr"]
    print(x1, y1)
    plt.figure(1)
    ax1 = plt.subplot(211)
    ax1.plot(x1, y1)
    plt.xlabel("ts (s)")
    plt.ylabel("rr (ms)")
    plt.title(f"patient {id[n]}, ceinture")
    plt.xlim(0, max(df1["ts_machine"].max(),
                    df2["ts_machine"].max())/1000)
    plt.ylim(0, max(df1["rr"].max(), df2["rr"].max()))
    ax2 = plt.subplot(212)
    ax2.plot(x2, y2)
    plt.xlabel("ts (s)")
    plt.ylabel("rr (ms)")
    plt.title(f"patient {id[n]}, garmin")
    plt.xlim(0, max(df1["ts_machine"].max(),
                    df2["ts_machine"].max())/1000)
    plt.ylim(0, max(df1["rr"].max(), df2["rr"].max()))
    plt.show()


def normal_to_normal(dataframe):
    """drop the rows where rr < 300 or > 1300 and where delta t """
    # 20%
    return dataframe[(dataframe["rr"] > 300) & (dataframe["rr"] < 1300)]

"""
def add_event(df_c, df_g):
    id = []
    df = pd.read_csv('C:/ecg/df_target_utc.csv')
    print(df)
    for i in range(0, len(df["id"])):
        m = re.search("([0-9]+)", str(df["id"][i]))
        id.append(m.group(0))
    df["id"] = id
    print(df)
    df = df[(abs(df.ts - df.ts.shift()) >= 4000)]  # remove rr repetitions
    print(df)
    df_c["event"] = [0] * len(df_c["id"])
    print(df_c)
    id_unique = np.unique(np.array(id))
    for i in range(0, len(id_unique)):
        sub_df = df[df["id"] == id_unique[i]]
        sub_df_c = df_c[df_c["id"] == id_unique[i]]

"""
def main():
    df_c, df_g = create_df_ceinture(), create_df_garmin()    # create dataframe ceinture and dataframe garmin
    # print(df_c)
    id = get_id()
    print(id)
    # print(normal_to_normal(df_c))
    #multiple_matplot(normal_to_normal(df_c), 1, 2)
    #matplot_c_g(df_c, df_g, 1)
    # add_event(df_c, df_g)
    data = pd.read_csv(rf'C:\ecg\rr_ceinture\ecg_10517002.csv')
    print(data.head())


if __name__ == '__main__':
    main()
