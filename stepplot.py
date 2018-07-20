# Copyright (c) 2018 Andrew Johnson
# See LICENSE for full license
# Permission is granted to copy this file with modifications so long as
# the above copyright notice is retained
"""
Function for some better step plotting

Y-data is assumed to be constant within some bin
"""

# TODO
# *. Put a proper error-bar marker for the legend. Currently same marker as normal plot
# *. Support for passing 2D matrices as y and yerr
# *. Testing
# *. Setup script, maybe?

from numpy import hstack, array, ndarray, divide, subtract, add
from matplotlib.pyplot import gca


def stepplot(x, y, yerr=None, ax=None, **kwargs):
    """
    Step-plotter for values that are constant within a bin

    Parameters
    ----------
    x: iterable
        Boundaries of bins. Must be of length N+1, where N is the
        number of elements in y
    y: iterable
        Data obtained in each bin of x
    yerr: None or iterable
        If given, plot error-bars in the center of the bin positions
    ax: None or axes argument
        Plot on which to draw the points. If not given, construct a new plot or
        obtain the current axes argument with :func:`matplotlib.pyplot.gca`.
    kwargs:
        Additional arguments to pass to :func:`matplotlib.pyplot.plot` and to
        func:`matplotlib.pyplot.errobar` if ``yerr`` is not ``None``.

    Returns
    -------
    object
        Ax on which the figure was drawn.
    """
    if not isinstance(x, ndarray):
        x = array(x)
    if not isinstance(y, ndarray):
        y = array(y)
    sortedIndices = x.argsort()
    sx = x[sortedIndices]
    sy = y[sortedIndices[:-1, ...]]
    stackedy = hstack((sy, sy[-1, ...]))
    drawstyle = 'steps-post'
    ax = ax or gca()
    lines2D = ax.plot(sx, stackedy, drawstyle=drawstyle, **kwargs)[0]

    if yerr is None:
        return ax
    if not isinstance(yerr, ndarray):
        yerr = array(yerr)

    syerr = yerr[sortedIndices[:-1, ...]]

    if 'label' in kwargs:
        kwargs.pop('label')
    if 'color' in kwargs:
        color = kwargs.pop('color')
    else:
        color = lines2D.get_color()

    errLoc = divide(subtract(sx[1:], sx[:-1]), 2)
    errLoc = add(sx[:-1], errLoc)
    ax.errorbar(errLoc, sy, yerr=syerr, color=color, fmt='none',
                **kwargs)

    return ax
