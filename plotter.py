import matplotlib.pyplot as plt
import numpy as np
import sys
from py_expression_eval import Parser
import warnings

warnings.filterwarnings("ignore")


class Plotter():
    def __init__(self):
        self.parser = Parser()
        self.functions = {}
        self.fInfo = {}
        self.info = {"label": "function",
                     "data": False,
                     "color": "b",
                     "x": np.linspace(-5.0, 5.0, 501),
                     "y": None,
                     "xLabel": 'x label',
                     "yLabel": 'y label',
                     "xyLabelTrue": False,
                     "title": "Plotter result",
                     "legend": True
                     }

    def check(self, expr):
        try:
            e = self.parser.parse(expr)
        except Exception as e:
            print(e)
            return None
        return e

    def add(self, f, **exInfo):
        expression = self.check(f)
        if expression is not None:
            self.functions[f] = expression
        else:
            print("parser: can't add the function " + f)
            return
        if exInfo:
            self.fInfo[f] = exInfo
        else:
            info = self.info.copy()
            info['label'] = f
            self.fInfo[f] = info

    def delete(self, f):
        if f in self.functions:
            self.functions.pop(f)

    def clear(self):
        plt.cla()

    def setY(self, f, x):
        if x:
            y = []
            for i in self.fInfo[f]['x']:
                try:
                    y.append(self.functions[f].evaluate({x: i}))
                except ValueError as e:
                    y.append(np.nan)
            self.fInfo[f]['y'] = np.array(y)
        else:
            v = self.functions[f].evaluate({})
            self.fInfo[f]['y'] = np.array(len(self.fInfo[f]['x']) * [v])

    def findArg(self, d):
        count = 0
        j = 0
        for i in d:
            if len(i) == 1 and (i not in ['e', 'E']):
                count += 1
                j = i

        return {'count': count, 'x': False or j}

    def setText(self, F):
        if F["xyLabelTrue"]:
            plt.xlabel(F["xlabel"])
            plt.ylabel(F["ylabel"])
        plt.title(F["title"])

    def plotF(self, f):
        if f not in self.functions:
            return
        symbols = self.findArg(self.functions[f].symbols())
        if symbols['count'] > 1:
            raise Exception('too much arguments of function' + f)
        elif symbols['x'] == f and len(f) > 1:
            raise Exception("plotF: error input, the function " + f)
        F = self.fInfo[f]
        self.setText(F)
        try:
            self.setY(f, symbols['x'])
            if symbols['x']:
                F['y'][:-1][np.abs(np.diff(F['y'])) > 0.6] = np.nan
            plt.plot(F['x'], F['y'], label=F['label'])
        except Exception as e:
            print("evaluate: " + f + " doesn't evaluate")
            print(e)

    def plot(self, f=None, legend=False):
        if f in self.functions.keys():
            self.plotF(f)
        else:
            for f in self.functions:
                self.plotF(f)
        if legend:
            plt.legend()
        plt.ylim(-5, 5)
        plt.savefig('plot' + '.png')
        # plt.show()

    def deleteAll(self):
        self.clear()
        self.functions.clear()
        self.fInfo.clear()


p = Plotter()
p.add(sys.argv[1])
p.plot()
