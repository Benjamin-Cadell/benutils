benutils
========

The description says it all, this is a utiliy function package to be used mainly for myself, but opened for public use if you'd like.

This package has only been tested on MacBook with Python 3.14 (latest as of 2026) and with Apple silicon architecture, but the functions are fairly standard and should be universval.

Installation
============

Assuming you already have an environment setup with pip you want to add this package to, see below.

Clone, change directory into the repo and pip install with something like:

    git clone https://github.com/Benjamin-Cadell/benutils.git

    cd benutils

    pip install -e .

Otherwise, set up an environment first with conda like:

    conda create -n benutils python=3.14
    conda activate benutils

And then follow the steps above to install the package.

Tutorial and Usage
==================

Not a full tutorial, just a basic explanation on the main use.

Matplotlib functions
--------------------

The default matplotlib figure options are:

    opts = {
        "figure.figsize": (10, 6),
        "text.usetex": True,
        "text.latex.preamble": r"\usepackage{amsmath}",
        "font.family": "serif",
        "axes.labelsize": 14,
        "font.size": 14,
        "legend.fontsize": 14,
        "xtick.labelsize": 14,
        "ytick.labelsize": 14,
        "axes.titlesize": 16,
    }

On import, the code will try to initialise Matplotlib with these options.
If LaTeX rendering fails (for example, because LaTeX is not installed), the `text.usetex`, `text.latex.preamble`, and `font.family` entries are removed from `opts`.
The remaining plotting style is preserved and Matplotlib's default text rendering is used.

They are applied to matplotlib temporary for each plotting call, and then reverted to the state it was in before.

You can modify them simply by modifying the benutils.opts dictionary, for example:

    import benutils
    benutils.opts["axes.labelsize"] = 10

    # ... plotting code will now use the above default option ...

Plotting
--------

I've added simple quick plots as I use them so often to just run a quick diagnostic plot.

Simply quick plot with benutils.plot like so:

    import benutils
    import numpy as np

    x = np.arange(10)
    y = x**2

    # To do a standard plot with standard options. The plot is shown immediately.
    benutils.plot(x,y)

Keyword arguments for the underlying plotting method can be passed normally.
Axes properties can also be passed together using the `set` keyword; its contents are forwarded to `ax.set()` after plotting:

    benutils.plot(
        x,
        y,
        color="tab:blue",
        set={
            "xlabel": "x",
            "ylabel": "y",
            "title": "A quick plot",
            "xlim": (0, 10),
        },
    )

I've also added benutils.errorbar(), benutils.scatter(), benutils.hist(), and
benutils.imshow() as they are very common. For more complex calls, use the Plot
class:

    plot = benutils.Plot() # arguments to the init are passed to plt.subplots()

    plot.imshow(...) # accepts any function passed to ax. e.g. ax.plot, ax.axhline, etc.

    plot.show() # shows the plot, closes the figure, resets to previous matplotlib settings

Remember with that class, before plot.show() has been called, you can access any of the fig, ax or plt objects with any of:

    ax = plot.ax
    fig = plot.fig
    plt = benutils.plt

    # For example
    ax.set_xlim(0,10)

    # And then for example you want to save it:
    plt.savefig("plot.png")

I will be adding more matplotlib and other functions in the future.

Let me know about any extra functions you want to add, otherwise feel free to fork and add them yourselves.
