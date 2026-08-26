#%% Matplotlib utilities for plotting with a consistent style.
import matplotlib.pyplot as plt
import warnings
import functools

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


def more_ax_kwargs(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        figsize = kwargs.pop("figsize", opts["figure.figsize"])

        # Explicit fig_ax takes precedence.
        if kwargs.get("fig_ax") is None:
            if plt.get_fignums():
                # Reuse the currently active figure/axes.
                fig = plt.gcf()
                ax = plt.gca()
            else:
                # Nothing open: make a new figure.
                fig, ax = plt.subplots(figsize=figsize)

            kwargs["fig_ax"] = (fig, ax)

        fig, ax = kwargs["fig_ax"]

        # Pull out kwargs intended for ax.set_* methods.
        set_kwargs = {
            key[4:]: kwargs.pop(key)
            for key in list(kwargs)
            if key.startswith("set_")
        }

        for name, value in set_kwargs.items():
            setter = getattr(ax, f"set_{name}")
            if isinstance(value, dict):
                setter(**value)
            elif isinstance(value, tuple):
                setter(*value)
            else:
                setter(value)

        return method(*args, **kwargs)

    return wrapper

@more_ax_kwargs
def plot(*args, fig_ax=None, show=True, **kwargs):
    """Plot data using the default style and display the figure."""
    with plt.rc_context(opts):
        fig, ax = fig_ax
        ax.plot(*args, **kwargs)
        _show_legend_if_needed(ax)
        if show:
            plt.show()
            plt.close(fig)

@more_ax_kwargs
def scatter(*args, fig_ax=None, show=True, **kwargs):
    """Create a scatter plot using the default style."""
    with plt.rc_context(opts):
        fig, ax = fig_ax
        ax.scatter(*args, **kwargs)
        _show_legend_if_needed(ax)
        if show:
            plt.show()
            plt.close(fig)

@more_ax_kwargs
def errorbar(*args, fig_ax=None, show=True, **kwargs):
    """Create an error-bar plot using the default style."""
    with plt.rc_context(opts):
        fig, ax = fig_ax
        ax.errorbar(*args, **kwargs)
        _show_legend_if_needed(ax)
        if show:
            plt.show()
            plt.close(fig)

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
