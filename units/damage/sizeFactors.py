""""
program to display size Factors in S1914
actual formula also adds damage by single unit incrementation
"""

import matplotlib.pyplot as plt
import numpy as np

# retrieved data damage * sizefactors * terrain * mode
NameToSizeFactor = {0: {'Infantry': {0: 1.2, 5: 0.36, 15: 0.12, 40: 0.0}, 'Infantry airdamage': {0: 0.12, 5: 0.036, 15: 0.012000000000000002, 40: 0.0}, 'Infantry buildingdamage': {0: 0.8999999999999999, 5: 0.26999999999999996, 15: 0.09000000000000001, 40: 0.0}}, 1: {'Artillery attack': {0: 1.5, 50: 0.0}, 'Artillery defence': {0: 0.5, 50: 0.0}, 'Artillery airdamage': {0: 0.050000005, 50: 0.0}}, 2: {'Balloon air': {0: 1.5, 50: 0.0}, 'Balloon land': {0: 0.5000000099999999, 50: 0.0}, 'Balloon buildingdamage': {0: 0.5000000099999999, 50: 0.0}}, 3: {'Submarine': {0: 4.0, 50: 0.0}, 'Submarine airdamage': {0: 0.4, 50: 0.0}}, 4: {'Tank': {0: 4.0, 5: 2.4, 10: 1.2, 25: 0.0}, 'Tank airdamage': {0: 0.4, 5: 0.24, 10: 0.12, 25: 0.0}}, 5: {'Railgun attack': {0: 3.0, 50: 0.0}, 'Railgun defence': {0: 1.0, 50: 0.0}, 'Railgun airdamage': {0: 0.1, 50: 0.0}}, 6: {'Battleship': {0: 6.0, 50: 0.0}, 'Battleship airdamage': {0: 1.2000000000000002, 50: 0.0}}, 7: {'Airplane air': {0: 4.0, 15: 3.2, 25: 2.4, 35: 1.6, 50: 0.0}, 'Airplane land': {0: 1.0, 15: 0.8, 25: 0.6, 35: 0.4, 50: 0.0}, 'Airplane buildingdamage': {0: 1.0, 15: 0.8, 25: 0.6, 35: 0.4, 50: 0.0}}, 8: {'Car attack': {0: 1.2, 6: 0.72, 15: 0.24, 25: 0.12, 40: 0.0}, 'Car defence': {0: 2.4, 6: 1.44, 15: 0.48, 25: 0.24, 40: 0.0}, 'Car airdamage': {0: 1.59999984, 6: 0.9599999039999999, 15: 0.319999968, 25: 0.159999984, 40: 0.0}}, 9: {'Cruiser': {0: 2.0, 50: 0.0}, 'Cruiser airdamage': {0: 1.5, 50: 0.0}}, 10: {'Bomber': {0: 5.0, 15: 4.0, 25: 3.0, 35: 2.0, 50: 0.0}, 'Bomber airdamage': {0: 0.497999975, 15: 0.39839998, 25: 0.298799985, 35: 0.19919999, 50: 0.0}}, 11: {'MkIV_tank': {0: 6.0, 5: 3.0, 10: 1.2000000000000002, 25: 0.0}, 'MkIV_tank airdamage': {0: 0.6000000000000001, 5: 0.30000000000000004, 10: 0.12000000000000002, 25: 0.0}}, 12: {'Cavalry attack': {0: 2.6, 6: 1.56, 15: 0.52, 25: 0.26, 40: 0.0}, 'Cavalry defence': {0: 1.2, 6: 0.72, 15: 0.24, 25: 0.12, 40: 0.0}, 'Cavalry airdamage': {0: 0.12000001199999999, 6: 0.0720000072, 15: 0.0240000024, 25: 0.0120000012, 40: 0.0}}}


def getDamage(index, name):

    order = sorted(NameToSizeFactor[index][name].items())
    order += [(60, order[-1][1])]
    damage, j = [0], 0
    for i in range(59):
        damage.append(damage[-1] + order[j][1])
        if i+1 == order[j+1][0]:
            j += 1

    return damage


def createPlot():

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize= (15,10), facecolor='lightgrey')
    fig.suptitle('damage chart'.upper(), fontsize=25, y = 0.93)

    a = plt.cm.nipy_spectral(np.linspace(0, 1, len(NameToSizeFactor)))
    a[6] = np.array([0,0,0,1])
    a[-1] = np.array([0.5, 0.7, 0.8, 1])
    color1 = iter(a)

    colorDict = {}
    for key in NameToSizeFactor.keys():
        colorDict[key] = next(color1)

    names1, names2, names3, names4 = [],[],[],[]
    x = np.arange(60)
    for index, dicts in NameToSizeFactor.items():

        for name, values in dicts.items():

            y = getDamage(index, name)

            if index in [0,4,8,11,12] and 'air' not in name:

                if 'defence' in name:
                    ax1.plot(x, y, linewidth=1.75, color=colorDict[index], dashes = [4,2], zorder=20)
                    names1.append(name)
                elif 'building' in name:
                    ax1.plot(x, y, linewidth=2, color=colorDict[index], zorder=30, dashes= [1,1])
                    names1.append(name)
                else:
                    ax1.plot(x, y, linewidth=2, color=colorDict[index], zorder=3)
                    names1.append(name)

            if index in [1,3,9,6,5] and 'air' not in name:
                if 'def' in name:
                    ax2.plot(x, y, linewidth=2.5, color=colorDict[index], dashes = [2,2], zorder=20)
                    names2.append(name)
                elif 'building' in name:
                    ax2.plot(x, y, linewidth=2, color=colorDict[index], zorder=30, dashes= [1,1])
                    names2.append(name)
                else:
                    ax2.plot(x, y, linewidth=2, color=colorDict[index], zorder=10)
                    names2.append(name)

            if index in [7,2,10] and 'building' not in name:
                if 'air' in name:
                    ax4.plot(x, y, linewidth=2, color=colorDict[index], dashes = [4,2], zorder=20)
                    names4.append(name)

                elif 'def' in name:
                    ax4.plot(x, y, linewidth=1.75, color=colorDict[index], dashes = [4,2], zorder=20)
                    names4.append(name)
                else:
                    ax4.plot(x, y, linewidth=2, color=colorDict[index], zorder=10)
                    names4.append(name)

            if 'air' in name:

                if 'Balloon' in name:
                    ax3.plot(x, y, linewidth=2.5, color=colorDict[index], dashes = [4,2], zorder = 11)
                else:
                    ax3.plot(x, y, linewidth=2, color=colorDict[index], zorder= 10)
                names3.append(name)


    ax1.grid(zorder=2.5)
    ax2.grid(zorder=2.5)
    ax3.grid(zorder=2.5)
    ax4.grid(zorder=2.5)

    ax1.set_xticks(np.arange(0, 66, 5))
    ax2.set_xticks(np.arange(0, 66, 5))
    ax3.set_xticks(np.arange(0, 66, 5))
    ax4.set_xticks(np.arange(0, 66, 5))

    ax1.set_yticks(np.arange(0, 66, 5))
    ax2.set_yticks(np.arange(0,311,10))
    ax3.set_yticks(np.arange(0, 311, 10))
    ax4.set_yticks(np.arange(0, 311, 10))

    ax1.set_title('melee landunits'.upper())
    ax2.set_title('sea and ranged landunits'.upper())
    ax3.set_title('air damage'.upper())
    ax4.set_title('airunits (+balloon)'.upper())

    ax1.set_xlabel('number of units'.upper())
    ax2.set_xlabel('number of units'.upper())
    ax3.set_xlabel('number of units'.upper())
    ax4.set_xlabel('number of units'.upper())

    ax1.set_ylabel('total damage'.upper())
    ax3.set_ylabel('total damage'.upper())
    ax2.set_ylabel('total damage'.upper())
    ax4.set_ylabel('total damage'.upper())

    ax1.set_xlim(0,53)
    ax2.set_xlim(0, 53)
    ax3.set_xlim(0, 53)
    ax4.set_xlim(0, 53)

    ax1.set_ylim(0,64)
    ax2.set_ylim(0,302)
    ax3.set_ylim(0,141)
    ax4.set_ylim(0,178)

    ax1.legend(names1, edgecolor = 'black')
    ax2.legend(names2, edgecolor = 'black')
    ax3.legend(names3, edgecolor='black')
    ax4.legend(names4, title='petruz', edgecolor='black')

    plt.savefig("damageChart.png", dpi=300)


createPlot()