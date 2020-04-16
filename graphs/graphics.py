from statistics import lateness_dict_average_seconds
import seaborn as sns
import pandas as pd

lateness_dict_average_seconds_graphics = {"hour": [], "delay": []}

for key in lateness_dict_average_seconds:
    lateness_dict_average_seconds_graphics["hour"].append(key)
    lateness_dict_average_seconds_graphics["delay"].append(lateness_dict_average_seconds[key])

pandas_list = pd.DataFrame(data=lateness_dict_average_seconds_graphics)

sns_plot = sns.barplot(x="hour", y="delay", data=pandas_list)

fig = sns_plot.get_figure()
fig.savefig("delay.png")
