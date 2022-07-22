import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from collections import defaultdict

class UnionFind:

    def __init__(self, size):

        if size <= 0:
            raise ValueError('Value should be larger than zero')
        self.size = size
        self.numComponents = size

        # initializing arrays with [None]*size is slightly faster
        self.ID = [i for i in range(size)]
        self.SZ = [1 for _ in range(size)]

    def find(self, p):

        root = p
        while root != self.ID[root]:
            root = self.ID[root]

        while p != root:
            next = self.ID[p]
            self.ID[p] = root
            p = next

        return root

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def componentSize(self, p):
        return self.sz[self.find(p)]

    def size(self):
        return self.size

    def components(self):
        return self.numberComponents

    def unify(self, p, q):

        if self.connected(p,q):
            return

        root1 = self.find(p)
        root2 = self.find(q)

        if self.SZ[root1] < self.SZ[root2]:
            self.SZ[root2] += self.SZ[root1]
            self.ID[root1] = root2
            self.SZ[root1] = 0
        else:
            self.SZ[root1] += self.SZ[root2]
            self.ID[root2] = root1
            self.SZ[root2] = 0

        self.numComponents -= 1

units = {'Artillery': (345600, 1.0), 'Balloon': (86400, 1.0), 'Submarine': (518400, 2.0), 'Tank': (518400, 2.0), 'Railgun': (1036800, 3.0), 'Battleship': (1036800, 3.0), 'Fighter': (518400, 2.0), 'Car': (86400, 0.25), 'Cruiser': (345600, 1.0), 'Bomber': (864000, 3.0), 'Heavy Tank': (691200, 3.0), 'Cavalry': (86400, 0.25)}

productiontimeFactory = lambda buildingtime, factoryHitpoints: 4 * buildingtime / factoryHitpoints

productiontimeWorkshop = lambda buildingtime, factoryHitpoints: 4 * buildingtime/(factoryHitpoints * 3600)

productiontimeHours = lambda buildingtime, factoryHitpoints: 4 * buildingtime / (max(factoryHitpoints-4,4) * 3600)


def groupUnits():

    unitnames = sorted(units)
    values = []
    for name in unitnames:
        values.append(units[name])

    u = UnionFind(len(units))
    for i,el1 in enumerate(values):
        for j,el2 in enumerate(values):
            if el1 == el2:
                u.unify(u.ID[i],u.ID[j])

    groups = defaultdict(list)
    for i, groupid in enumerate(u.ID):
        groups[groupid].append(unitnames[i])

    return groups


def plot():

    fig, ax = plt.subplots(facecolor='white',figsize= (14,8))
    fig.suptitle('production times'.upper(), fontsize=25, y=0.93)

    colors = ['red','gold','blue','orange','black','green','purple']
    color = iter(colors)

    for group, names in groups.items():

        buildingtime, buildinglevel = units[names[0]]
        y = []
        domain = ((int(buildinglevel)*4+4), 21)
        c = next(color)

        for hitpoint in range(*domain):
            for _ in range(2):
                y.append(productiontimeHours(buildingtime, hitpoint))

        x = [el for el in range(*domain) for _ in range(2)]
        x = x[1::] + [x[-1]+1]

        # balloon overlaps with car-group
        if 'Car' not in names:
            for i in range(0, len(x)-2, 2):
                ax.plot( [x[i],x[i+2]],[y[i],y[i]],'-o', linewidth=4, color=c)

            for i in range(len(x)-4):
                if x[i] == x[i+1] and y[i] != y[i+1]:
                    ax.plot([x[i]],[y[i]], 'o', color='white')
        else:
            for i in range(0, len(x) - 2, 2):
                ax.plot([x[i], x[i + 2]], [y[i], y[i]], '--o', linewidth=3, color=c)

            for i in range(len(x) - 4):
                if x[i] == x[i + 1] and y[i] != y[i + 1]:
                    ax.plot([x[i]], [y[i]], 'o', color='white')

        #messy extend to workshop
        if 'Car' in names:
            y = []
            for hitpoint in range(2,5):
                for _ in range(2):
                    y.append(productiontimeWorkshop(buildingtime,hitpoint))

            x = [el for el in range(2,5) for _ in range(2)]
            for i in range(0, len(x) - 2, 2):
                ax.plot([x[i], x[i + 2]], [y[i], y[i]], '-o',dashes = [4,1], linewidth=4, color=c)

            for i in range(len(x) - 1):
                if x[i] == x[i - 1]:
                    ax.plot([x[i+1]], [y[i]], 'o', color='white')


    ax.set_xticks(np.arange(21))
    xlabels = [el for el in range(5)] + [h if (h % 4 != 0 or h < 1) else f'factory lvl{(h)//4}' for h in range(1,17)]
    xlabels[2] = 'workshop(1)'
    xlabels[4] = 'workshop(2)'
    ax.set_xticklabels(xlabels)

    ax.set_xlabel('HITPOINTS', fontsize=14)
    ax.set_ylabel('HOURS', fontsize=14)
    ax.set_yticks(np.arange(0,101,5))
    ax.set_xlim(0,20.1)
    ax.grid(color='black', zorder=0)

    color = iter(colors)
    labels = iter([", ".join(names) for groupid, names in groups.items()])
    legend_elements = []
    for _ in range(len(colors)):
        legend_elements.append(Patch(facecolor=next(color), label=next(labels)))

    ax.legend(title='petruz', handles=legend_elements, loc=2, fancybox=True, edgecolor= 'black')

    plt.savefig("buildingtimeChart.png", dpi=300)


if __name__ == "__main__":
    groups = groupUnits()
    plot()