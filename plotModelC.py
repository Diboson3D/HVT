#!/usr/bin/env python

import os, sys
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 100)

series = ["Zprime", "Wprime", "WprimeToWZ", "WprimeToWH", "ZprimeToWW", "ZprimeToZH", "Zprime3", "Wprime3"]

masses = range(800, 8000+1, 100)

data = {}

df = pd.DataFrame(columns=["M"]+series)

# Read Madgraph output files
for cat in series:
    mass = []
    xs = []
    pdfUp = []
    pdfDown= []
    for m in masses:
        with open("xs/HVTmodelC_" + cat + "_" + "%d.txt" % m, "r") as l:
            mass_, xs_, pdfUp_, pdfDown_ = m, 0., 0., 0.
            lines = l.read().splitlines()
            for l in lines:
                if "original cross-section" in l:
                    try:
                        xs_ = float(l.split(" ")[-1])
                    except:
                        print "xs not found in M", m
                if "scale variation:" in l:
                    try:
                        pdfDown_ = float(l.split(" ")[-1].replace("%", ""))
                        pdfUp_   = float(l.split(" ")[-2].replace("%", ""))
                    except:
                        print "pdf not found in M", m
                if "Cross-section" in l:
                    try:
                        xs_ = float(l.split(" ")[-4])
                    except:
                        print "xs not found in M", m
            mass.append(mass_)
            xs.append(xs_)
            pdfUp.append(pdfUp_)
            pdfDown.append(pdfDown_)
    df["M"] = mass
    df[cat] = xs
    if any([x for x in pdfUp if x != 0.]): df[cat+" Up"] = pdfUp
    if any([x for x in pdfDown if x != 0.]): df[cat+" Down"] = pdfDown
    

# Rename some columns
df.rename(columns={"Wprime" : "Wprime_cH1", "Zprime" : "Zprime_cH1", "Wprime3" : "Wprime_cH3", "Zprime3" : "Zprime_cH3"}, inplace=True)

df["BrWprimeToWZ"] = df["WprimeToWZ"] / df["Wprime_cH1"]
df["BrWprimeToWH"] = df["WprimeToWH"] / df["Wprime_cH1"]
df["BrZprimeToWW"] = df["ZprimeToWW"] / df["Zprime_cH1"]
df["BrZprimeToZH"] = df["ZprimeToZH"] / df["Zprime_cH1"]

# Export to CSV
df.to_csv("dataframe.csv")

# print
#print df

#for index, row in df.iterrows():
#    print row["M"], ": [", int(row["Zprime Up"]*10)/1000.+1., ",", int(row["Zprime Down"]*10)/1000.+1., "], ",
#    #print row["M"], ": [1., 1.], ",
#print


# Plot
fig1, ax1 = plt.subplots()

ax1.plot(df['M'], df['Wprime_cH1'], '-', color='tab:red', label="W', $c_H = 1$")
ax1.plot(df['M'], df['Zprime_cH1'], '-', color='tab:blue', label="Z', $c_H = 1$")
ax1.plot(df['M'], df['Wprime_cH3'], '--', color='tab:red', label="W', $c_H = 3$")
ax1.plot(df['M'], df['Zprime_cH3'], '--', color='tab:blue', label="Z', $c_H = 3$")

ax1.legend()
ax1.set_title("HVT model C")
ax1.set_xlabel("V' mass (GeV)")
ax1.set_ylabel('cross section (pb)')
ax1.set_yscale('log')

fig1.tight_layout()
plt.savefig("modelC_XS.pdf")
plt.savefig("modelC_XS.png")


fig2, ax2 = plt.subplots()

ax2.plot(df['M'], df['BrWprimeToWZ'], '-', color='tab:red', label="W' $\longrightarrow $ WZ")
ax2.plot(df['M'], df['BrWprimeToWH'], '-', color='tab:orange', label="W' $\longrightarrow$ WH")
ax2.plot(df['M'], df['BrZprimeToWW'], '-', color='tab:green', label="Z' $\longrightarrow$ WW")
ax2.plot(df['M'], df['BrZprimeToZH'], '-', color='tab:blue', label="Z' $\longrightarrow$ ZH")

ax2.set_ylim(top=1, bottom=0)
ax2.legend()
ax2.set_title("HVT model C, $c_H = 1$")
ax2.set_xlabel("V' mass (GeV)")
ax2.set_ylabel('Branching fraction')
#ax2.set_yscale('log')

fig2.tight_layout()
plt.savefig("modelC_BR.pdf")
plt.savefig("modelC_BR.png")
