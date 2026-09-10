#%% Matplotlib utilities for plotting with a consistent style.
import matplotlib.pyplot as plt
import warnings

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

# Try to initialise LaTeX rendering. If it fails, remove the LaTeX-specific
# options while preserving the rest of the plotting style.
fig = None
try:
    with plt.rc_context(opts):
        fig, ax = plt.subplots()
        ax.set_xlabel(r"$\alpha + \beta$")
        fig.canvas.draw()
except Exception as exc:
    warnings.warn(
        f"Failed to initialize/import LaTeX rendering: {exc}. "
        "Falling back to Matplotlib's default text rendering.",
        RuntimeWarning,
        stacklevel=2,
    )
    for key in ("text.usetex", "text.latex.preamble", "font.family"):
        opts.pop(key)
finally:
    if fig is not None:
        plt.close(fig)

def _show_legend_if_needed(ax):
    """Show the legend if any of the lines have labels."""
    handles, labels = ax.get_legend_handles_labels()
    if any(label for label in labels):
        ax.legend()

def _show_and_close(fig, show=True):
    if show:
        plt.show()
        plt.close(fig)

def _quick_plot(method, *args, fig_ax=None, figsize=None, show=True, set=None, **kwargs):
    if fig_ax is None:
        if plt.get_fignums():
            fig = plt.gcf()
            ax = plt.gca()
        else:
            fig, ax = plt.subplots(figsize=figsize or opts["figure.figsize"])
    else:
        fig, ax = fig_ax

    with plt.rc_context(opts):
        getattr(ax, method)(*args, **kwargs)
        ax.set(**(set or {}))
        _show_legend_if_needed(ax)
        _show_and_close(fig, show=show)

def plot(*args, fig_ax=None, figsize=None, show=True, set=None, **kwargs):
    """Plot data using the default style and display the figure."""
    return _quick_plot("plot", *args, fig_ax=fig_ax, figsize=figsize, show=show, set=set, **kwargs)

def scatter(*args, fig_ax=None, figsize=None, show=True, set=None, **kwargs):
    """Create a scatter plot using the default style."""
    return _quick_plot("scatter", *args, fig_ax=fig_ax, figsize=figsize, show=show, set=set, **kwargs)

def errorbar(*args, fig_ax=None, figsize=None, show=True, set=None, **kwargs):
    """Create an error-bar plot using the default style."""
    return _quick_plot("errorbar", *args, fig_ax=fig_ax, figsize=figsize, show=show, set=set, **kwargs)

def hist(*args, fig_ax=None, figsize=None, show=True, set=None, **kwargs):
    """Create a histogram using the default style."""
    return _quick_plot("hist", *args, fig_ax=fig_ax, figsize=figsize, show=show, set=set, **kwargs)

def imshow(*args, fig_ax=None, figsize=None, show=True, set=None, **kwargs):
    """Display data as an image using the default style."""
    return _quick_plot("imshow", *args, fig_ax=fig_ax, figsize=figsize, show=show, set=set, **kwargs)

class Plot:
    """
    A class for multiple plots with a style and use similar to that of pyplot.
    All unknown methods are directly passed to the axes object.
    """

    def __init__(self, *args, **kwargs):
        self._context = plt.rc_context(opts)
        self._context.__enter__()
        self._closed = False

        try:
            self.fig, self.ax = plt.subplots(*args, **kwargs)
        except Exception:
            self._context.__exit__(None, None, None)
            raise

    def __getattr__(self, name):
        """Forward unknown attributes to the underlying Axes object."""
        return getattr(self.ax, name)

    def show(self, *, close=True):
        """Display the figure and optionally close it afterwards."""
        _show_legend_if_needed(self.ax)
        plt.show()

        if close:
            self.close()

    def close(self):
        """Close the figure and restore the previous Matplotlib settings."""
        if not self._closed:
            plt.close(self.fig)
            self._context.__exit__(None, None, None)
            self._closed = True

    # Use the same enter/exit interface as plt.rc_context to allow usage with the 'with' statement.
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
