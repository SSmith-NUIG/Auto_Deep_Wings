import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
# Get list of the pairwise files outputted by poolfstat script
list_of_auto_deep_wings = os.listdir("/home/stephen/Documents/deep_wings/deep_wings_output/auto")
len(list_of_auto_deep_wings)
df_list = []
i = 0
for file_name in list_of_auto_deep_wings:
    df1 = pd.read_excel(f"/home/stephen/Documents/deep_wings/deep_wings_output/auto/{file_name}", engine='openpyxl')
    sample_name = os.path.splitext(df1["File name"][0])[0].split("_", 1)[0]
    df1 = df1[df1["File name"].str.contains("AVERAGE")==False]
    new_column = sample_name
    df1["Sample name"] = new_column
    df1.drop(columns=["File name"], inplace=True)
    df_list.append(df1)

combined_success_df = pd.concat(df_list, axis=0)
combined_success_df["Success"].value_counts()
combined_success_df = combined_success_df.sort_values(['Sample name']).reset_index(drop=True)
combined_success_df.to_csv("/home/stephen/Documents/deep_wings/deep_wings_output/combined_auto.csv")

df_melted = pd.melt(combined_success_df, id_vars=['Sample name'], value_vars=['Success'])

sns.countplot(x="Sample name", hue="value", data=df_melted)
plt.xticks(rotation=90, ha="center")
plt.title("Auto crop upload success data")
plt.xlabel("Sample Name")
plt.legend(bbox_to_anchor=(1.01, 1.05), labels=["Fail", "Success"], loc="upper left")
plt.text(x=25, y=12.2, s="Total: 459 Success: 425 Fail: 34 Success% = 92.6%")


df_list = []
i = 0
for file_name in list_of_auto_deep_wings:
    df1 = pd.read_excel(f"/home/stephen/Documents/deep_wings/deep_wings_output/auto/{file_name}", engine='openpyxl')
    sample_name = os.path.splitext(df1["File name"][0])[0].split("_", 1)[0]
    df1= df1[df1["File name"].str.contains("AVERAGE")==True]
    df1["Sample name"] = sample_name
    df2 = df1[["Sample name", "Subspecies Top #1", "Subspecies Probability Top #1",
               "Subspecies Top #2", "Subspecies Probability Top #2",
               "Subspecies Top #3", "Subspecies Probability Top #3"]]
    df_list.append(df2)


combined_subspecies_df = pd.concat(df_list, axis=0)
combined_subspecies_df = combined_subspecies_df.sort_values(['Sample name']).reset_index(drop=True)
combined_subspecies_df.to_csv("/home/stephen/Documents/deep_wings/deep_wings_output/combined_subspecies_auto.csv")

sns.barplot(data=combined_subspecies_df, x="Sample name", y="Subspecies Probability Top #1", hue="Subspecies Top #1",
            dodge=False)
plt.xticks(rotation=90, ha="center")
plt.title("Auto crop lineage assignment")
plt.legend(bbox_to_anchor=(1.13, 1.15), loc='upper right', borderaxespad=0)
plt.xlabel("Sample Name")
