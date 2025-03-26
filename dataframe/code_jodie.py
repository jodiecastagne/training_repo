"""
Code développé par : Jodie Castagné
Dans le cadre de la TX Traitement et analyse de signaux RR pour la collecte de données
Encadrement : Baptiste Chevallier
Semestre : A22

Catalogue des fonctions de traitement des données RR, calculs de statistiques, filtrage et visualisation.
"""


import pandas as pd
import glob
from pathlib import Path
import re
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np


def get_id(dispositif="ceinture"):
    """return a list of the ids of the subjects"""

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
    """return a DF with ceinture datas for all subjects"""

    path = r'C:\ecg\rr_ceinture'  # Get data file names
    filenames = glob.glob(path + "/*.csv")
    id = get_id("ceinture")

    dfs = []  # Read the files
    j = 0
    for filename in filenames:
        data = pd.read_csv(filename)
        data.sort_values(by=["timestamp_machine"], inplace=True)
        # print(data["timestamp_machine"])
        data["timestamp_machine"] -= data["timestamp_machine"].min()  # ts starts at zero
        i = [id[j]] * len(data)
        data['id'] = i
        j += 1
        dfs.append(data)

    df = pd.concat(dfs, ignore_index=True)  # Concatenate all datas into one DataFrame
    df.rename(columns={"timestamp_machine": "ts_machine", "timestamp_google": "ts_google"}, inplace = True)
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
        data.sort_values(by=["ts_machine"], inplace=True)
        data["ts_machine"] -= data["ts_machine"].min()  # ts starts at zero
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
    """Create big DF with statistical parameters calculated on ECG and Garmin data"""

    id = get_id("ceinture")  # create first column (id)
    tab = pd.DataFrame(columns=['id'])
    tab['id'] = id
    
    # Create tab stats ceinture
    for i in range(0, len(id)):
        df = df_c
        normal = df.loc[df['id'] == id[i]]
        a = df['rr'].loc[df['id'] == id[i]]
        tab.loc[tab['id'] == id[i], 'somme RR (s)'] = a.sum() / 1000
        b = df['ts_machine'].loc[df['id'] == id[i]]
        tab.loc[tab['id'] == id[i], 'durée enregistrement (s)'] = (b.max() - b.min()) / 1000
        tab.loc[tab['id'] == id[i], 'moyenne RR (ms)'] = a.mean()
        tab["Données manquantes (%)"] = (tab["durée enregistrement (s)"] - tab["somme RR (s)"]) / tab["durée enregistrement (s)"] * 100
        if len(a) != 0:
            tab.loc[tab['id'] == id[i], 'valeurs anormales (%)'] = 100-((len(normal_to_normal(normal).rr)/len(a))*100)
            #print(len(normal_to_normal(normal).rr), len(a))
     #print(tab.head())

    # Create tab stats garmin
    tab2 = pd.DataFrame()
    tab2['id2'] = id

    for i in range(0, len(id)):
        df = df_g
        c = df['rr'].loc[df['id'] == id[i]]
        normal = df.loc[df['id'] == id[i]]
        tab2.loc[tab2['id2'] == id[i], 'somme RR (s)2'] = c.sum() / 1000
        d = df['ts_machine'].loc[df['id'] == id[i]]
        tab2.loc[tab2['id2'] == id[i], 'durée enregistrement (s)2'] = ((d.max() - d.min()) / 1000)
        tab2.loc[tab2['id2'] == id[i], 'moyenne RR (ms)2'] = c.mean()
        tab2["Données manquantes (%)2"] = (tab2["durée enregistrement (s)2"] - tab2["somme RR (s)2"])/tab2["durée enregistrement (s)2"]*100
        if len(c) != 0:
            tab2.loc[tab2['id2'] == id[i], 'valeurs anormales (%)2'] = 100-((len(normal_to_normal(normal).rr)/len(c))*100)
    # concatenate both df
    return pd.concat([tab, tab2], axis=1)


def circular_plot(df_stat):
    """Create a circular plot showing the % of subjects with specific amounts of anomalous values"""
    stats = df_stat  # set of statistical values
    size1 = len(stats[stats['valeurs anormales (%)'] < 10.])
    size2 = len(stats[(stats['valeurs anormales (%)'] >= 10.) & (stats["valeurs anormales (%)"] < 15.)])
    size3 = len(stats[stats['valeurs anormales (%)'] >= 15.])

    labels = '[0-10%]', '[10-15%]', '[+15%]'
    sizes = [size1, size2, size3]
    colors = ["yellowgreen", "orange", "red"]

    plt.subplot(121)
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=False, startangle=90)
    plt.title("Valeurs anormales Ceinture")
    plt.axis('equal')

    size4 = len(stats[stats['valeurs anormales (%)2'] < 10.])
    size5 = len(stats[(stats['valeurs anormales (%)2'] >= 10.) & (stats["valeurs anormales (%)2"] < 15.)])
    size6 = len(stats[stats['valeurs anormales (%)2'] >= 15.])

    labels2 = '[0-10%]   ', '               [10-15%]', '[+15%]'
    sizes2 = [size4, size5, size6]

    plt.subplot(122)
    plt.pie(sizes2, labels=labels2, colors=colors, autopct='%1.1f%%', shadow=False, startangle=90)
    plt.title("Valeurs anormales Garmin")
    plt.axis('equal')

    plt.show()


def missing_values(df_stat):
    """Create a circular plot showing if the device under- or overestimates the RR values based on % patients
    in each category"""
    stats = df_stat  # set of statistical values
    size1 = len(stats[stats['Données manquantes (%)'] < 0])
    size2 = len(stats[stats['Données manquantes (%)'] >= 0])

    labels = 'surestime RR', 'sousestime RR'
    sizes = [size1, size2]
    colors = ["gold", "lemonchiffon"]

    plt.subplot(121)
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=False, startangle=90)
    plt.title("Ceinture")
    plt.axis('equal')

    size3 = len(stats[stats['Données manquantes (%)2'] < 0])
    size4 = len(stats[stats['Données manquantes (%)2'] >= 0])

    labels2 = 'surestime RR', 'sous-estime RR'
    sizes2 = [size3, size4]
    plt.subplot(122)
    plt.pie(sizes2, labels=labels2, colors=colors, autopct='%1.1f%%', shadow=False, startangle=90)
    plt.title("Garmin")
    plt.axis('equal')

    plt.show()


def visualize_plotly(dataframe, id : int):
    """visualize RR signal for one subject with plotly
    parameter 1 : df_ceinture or df_garmin
    parameter 2 : id of subject (int)"""

    df_sort = dataframe.sort_values("ts_machine")
    df = df_sort[['rr', 'ts_machine']].loc[df_sort['id'] == id]
    fig = px.line(df, x="ts_machine", y="rr", title="RR de l'ID " + str(id))
    fig.show()


def visualize_two_subjects(df, id1 : int, id2 : int):
    """visualize RR signals of 2 subjects from 1 device"""
    df1 = df[["rr", "ts_machine"]].loc[df["id"] == id1]
    df2 = df[["rr", "ts_machine"]].loc[df["id"] == id2]

    x1 = df1["ts_machine"]/1000
    x2 = df2["ts_machine"]/1000
    y1 = df1["rr"]
    y2 = df2["rr"]

    fig, ax = plt.subplots(2, 1)

    ax[0].plot(x1, y1)
    ax[1].plot(x2, y2)
    ax[0].set_title(f"patient {id1}")
    ax[1].set_title(f"patient {id2}")
    ax[0].set_xlim(0, max(df1["ts_machine"].max(), df2["ts_machine"].max())/1000)
    ax[0].set_ylim(0, max(df1["rr"].max(), df2["rr"].max()))

    ax[0].set_ylim(0, 1500)
    ax[1].set_xlim(0, max(df1["ts_machine"].max(), df2["ts_machine"].max())/1000)
    ax[1].set_ylim(0, max(df1["rr"].max(), df2["rr"].max()))
    ax[1].set_ylim(0, 1500)
    ax[0].set_xlabel("time (s)")
    ax[0].set_ylabel("rr (ms)")
    ax[1].set_xlabel("time (s)")
    ax[1].set_ylabel("rr (ms)")
    fig.tight_layout()

    plt.show()


def visualize_two_devices(df_c, df_g, id: int):
    """visualize RR signals of 1 subjects from the 2 devices"""
    df1 = df_c[["rr", "ts_machine"]].loc[df_c["id"] == id]
    df2 = df_g[["rr", "ts_machine"]].loc[df_g["id"] == id]
    x1 = df1["ts_machine"] / 1000
    x2 = df2["ts_machine"] / 1000
    y1 = df1["rr"]
    y2 = df2["rr"]

    fig, ax = plt.subplots(2, 1)

    ax[0].plot(x1, y1)
    ax[1].plot(x2, y2)
    ax[0].set_title(f"Ceinture patient {id}")
    ax[1].set_title(f"Garmin patient {id}")
    ax[0].set_xlim(0, max(df1["ts_machine"].max(), df2["ts_machine"].max())/1000)
    ax[0].set_ylim(0, max(df1["rr"].max(), df2["rr"].max()))

    ax[0].set_ylim(0, 1500)
    ax[1].set_xlim(0, max(df1["ts_machine"].max(), df2["ts_machine"].max())/1000)
    ax[1].set_ylim(0, max(df1["rr"].max(), df2["rr"].max()))
    ax[1].set_ylim(0, 1500)
    ax[0].set_xlabel("time (s)")
    ax[0].set_ylabel("rr (ms)")
    ax[1].set_xlabel("time (s)")
    ax[1].set_ylabel("rr (ms)")
    fig.tight_layout()

    plt.show()


def normal_to_normal(dataframe):
    """drop the rows where rr < 300 or > 1300 ms and where rr is different from 20% of previous RR"""
    df = dataframe[(dataframe["rr"] > 300) & (dataframe["rr"] < 1300)]
    df = df[((df.shift().rr-df.rr)/df.shift().rr <= 0.2) & ((df.shift().rr-df.rr)/df.shift().rr >= -0.2)]
    return df

""" attempt to add the target column
def add_event(df_c, df_g):
    id = []
    event = pd.read_csv('C:/ecg/df_target_utc.csv')
    for i in range(0, len(event["id"])):
        m = re.search("([0-9]+)", str(event["id"][i]))
        id.append(m.group(0))
    event["id"] = id
    df_event = event[(abs(event.ts - event.ts.shift()) >= 4000)]  # remove rr repetitions
    df_c["event"] = [0] * len(df_c["id"])
    id_unique = np.unique(np.array(id))
    df = []
    for i in range(0, len(id_unique)):
        sub_event = df_event[df_event["id"] == id_unique[i]]
        sub_df_c = df_c[df_c["id"] == id_unique[i]]
        for j in range(0, len(sub_event["id"])):
            if not sub_df_c.empty:
                print("texte :", (sub_event.iloc[j, 2] + (sub_event.iloc[j, 0]*1000)))
                sub_df_c.loc[(sub_df_c['ts_machine'] <= (sub_event.iloc[j, 2] + sub_event.iloc[j, 0]*1000)) &
                             (sub_df_c['ts_machine'] >= sub_event.iloc[j, 2]), 'event'] = 1
        df.append(sub_df_c)
    print("colonne events ajoutés")
    return pd.concat(df)
"""


def main():
    id = get_id()
    print(get_id())
    df_c, df_g = create_df_ceinture(), create_df_garmin()
    export(df_c, "ceinture")
    export(df_g, "montre")
    export(create_df_stats(df_c,df_g), "today")
    #visualize_plotly(df_c, id[1])
    visualize_two_devices(df_c, df_g, id[2])
    visualize_two_subjects(df_c, id[2], id[3])
    df_stats = create_df_stats(normal_to_normal(df_c), normal_to_normal(df_g))
    circular_plot(df_stats)
    missing_values(df_stats)


if __name__ == '__main__':
    main()
