"""
Demo-script to generate plot figures
"""

from matplotlib import pyplot
from stepplot import stepplot

x = [0, 1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]
yerr = [0.1, 0.4, 0.2, 0.6, 0.10]

fig1 = pyplot.figure()
stepplot(x, y, yerr=yerr, label='stepplot')
pyplot.legend()


if __name__ == '__main__':
    pyplot.show()
    resp = input('Save figure? [yN] ')
    if resp.lower()[0].lower() == 'y':
        fig1.savefig('demo1')
