# Copyright (c) 2018 Andrew Johnson
# See LICENSE for full license
# Permission is granted to copy this file with modifications so long as
# the above copyright notice is retained
"""
Function for some better step plotting

Y-data is assumed to be constant within some bin
"""

# TODO
# *. Put a proper error-bar marker for the legend.
#    Currently same marker as normal plot
# *. Support for passing 2D matrices as y and yerr
# *. Testing
# *. Setup script, maybe?

from numpy import hstack, array, ndarray, divide, subtract, add
from matplotlib.pyplot import gca


def stepplot(x, y, yerr=None, ax=None, stackon='right', loglog=False,
             logx=False, logy=False, **kwargs):
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
    stackon: {'right', 'left'}
        Append the last or first column to ydata and yerr.
    loglog: bool
        Apply a log scale to both axis if this evaluates to true
    logx: bool
        Apply a logscale to x-axis if this evaluates to true
    logy: bool
        Apply a logscale to y-axis if this evaluates to true
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
    if stackon == 'right':
        sy = y[sortedIndices[:-1, ...]]
        stackedy = hstack((sy, sy[-1, ...]))
        drawstyle = 'steps-post'
    elif stackon == 'left':
        sy = y[sortedIndices[1:, ...]]
        stackedy = hstack((sy[0, ...], sy))
        drawstyle = 'steps-pre'
    else:
        raise KeyError("stackon must be either left or right, not {}"
                       .format(stackon))
    ax = ax or gca()
    lines2D = ax.plot(sx, stackedy, drawstyle=drawstyle, **kwargs)[0]

    if loglog or logy:
        ax.set_yscale('log')
    if loglog or logx:
        ax.set_xscale('log')

    if yerr is None:
        return ax
    if not isinstance(yerr, ndarray):
        yerr = array(yerr)

    if stackon == 'right':
        syerr = yerr[sortedIndices[:-1, ...]]
        stackedyerr = hstack((syerr, syerr[-1, ...]))
    else:
        syerr = yerr[sortedIndices[1:, ...]]
        stackedyerr = hstack((syerr[0, ...], syerr))

    if 'label' in kwargs:
        kwargs.pop('label')
    if 'color' in kwargs:
        color = kwargs.pop('color')
    else:
        color = lines2D.get_color()

    errLoc = divide(subtract(sx[1:], sx[:-1]), 2)
    errLoc = add(sx[:-1], errLoc)
    ax.errorbar(errLoc, sy, yerr=stackedyerr, color=color, fmt='none',
                **kwargs)

    return ax
