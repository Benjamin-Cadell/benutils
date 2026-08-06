#%% Matplotlib utilities for plotting with a consistent style.
import matplotlib.pyplot as plt
import warnings

latex_opts = {
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

fallback_opts = {
    "figure.figsize": (10, 6),
    "axes.labelsize": 14,
    "font.size": 14,
    "legend.fontsize": 14,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "axes.titlesize": 16,
}

# Try and initialise LaTeX rendering, otherwise go to fallback, either way,
# "opts" is generated and can be modified by the user.
fig = None
try:
    with plt.rc_context(latex_opts):
        fig, ax = plt.subplots()
        ax.set_xlabel(r"$\alpha + \beta$")
        fig.canvas.draw()
except Exception as exc:
    warnings.warn(
        f"Failed to initialize LaTeX rendering: {exc}. "
        "Falling back to Matplotlib's default text rendering.",
        RuntimeWarning,
        stacklevel=2,
    )
    opts = fallback_opts
else:
    opts = latex_opts
finally:
    if fig is not None:
        plt.close(fig)

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
