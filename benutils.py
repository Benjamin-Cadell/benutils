import matplotlib.pyplot as plt

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

def _show_legend_if_needed(ax):
    """Show the legend if any of the lines have labels."""
    handles, labels = ax.get_legend_handles_labels()
    if any(label for label in labels):
        ax.legend()

def plot(*args, **kwargs):
    """Plot data using the default style and display the figure."""
    with plt.rc_context(opts):
        plt.plot(*args, **kwargs)
        _show_legend_if_needed(plt.gca())
        plt.show()


def scatter(*args, **kwargs):
    """Create a scatter plot using the default style."""
    with plt.rc_context(opts):
        plt.scatter(*args, **kwargs)
        _show_legend_if_needed(plt.gca())
        plt.show()

def errorbar(*args, **kwargs):
    """Create an error-bar plot using the default style."""
    with plt.rc_context(opts):
        plt.errorbar(*args, **kwargs)
        _show_legend_if_needed(plt.gca())
        plt.show()

class Plot:
    """A small wrapper around a Matplotlib figure and axes."""

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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()