#%% Matplotlib utilities for plotting with a consistent style.
import matplotlib.pyplot as plt
import warnings
from types import TracebackType
from typing import Any, Dict, Optional, Tuple, Type

from matplotlib.axes import Axes
from matplotlib.figure import Figure

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

def _show_legend_if_needed(ax: Axes) -> None:
    """Show the legend if the axes contain labelled artists.

    Parameters:
    ax : matplotlib.axes.Axes
        Axes to check for legend entries.
    """
    handles, labels = ax.get_legend_handles_labels()
    if any(label for label in labels):
        ax.legend()

def _show_and_close(fig: Figure, show: bool = True) -> None:
    """Display open figures and close the supplied figure when requested.

    Parameters:
    fig : matplotlib.figure.Figure
        Figure to close after displaying.
    show : bool, optional
        Whether to display figures and close this figure. Defaults to True.
    """
    if show:
        plt.show()
        plt.close(fig)

def _quick_plot(
    method: str, *args: Any, fig_ax: Optional[Tuple[Figure, Axes]] = None,
    figsize: Optional[Tuple[float, float]] = None, show: bool = True,
    set: Optional[Dict[str, Any]] = None, **kwargs: Any,
) -> None:
    """Call an axes plotting method using the default style.

    Parameters:
    method : str
        Name of the plotting method on the axes.
    *args : Any
        Positional arguments passed to the plotting method.
    fig_ax : tuple of (Figure, Axes), optional
        Figure and axes to use. Defaults to the current axes, or new axes
        if no figure is open.
    figsize : tuple of float, optional
        Width and height in inches when creating a figure. Defaults to
        opts["figure.figsize"]. Ignored when reusing a figure.
    show : bool, optional
        Whether to display open figures and close the plotted figure.
        Defaults to True.
    set : dict of str to Any, optional
        Axes properties passed to ax.set(), such as xlabel or title.
    **kwargs : Any
        Keyword arguments passed to the plotting method.
    """
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

def plot(
    *args: Any, fig_ax: Optional[Tuple[Figure, Axes]] = None,
    figsize: Optional[Tuple[float, float]] = None, show: bool = True,
    set: Optional[Dict[str, Any]] = None, **kwargs: Any,
) -> None:
    """Plot lines or markers using the default style.

    Parameters:
    *args : Any
        Coordinates and optional format strings passed to Axes.plot().
    fig_ax : tuple of (Figure, Axes), optional
        Figure and axes to use. Defaults to the current axes, or new axes
        if no figure is open.
    figsize : tuple of float, optional
        Width and height in inches when creating a figure. Defaults to
        opts["figure.figsize"]. Ignored when reusing a figure.
    show : bool, optional
        Whether to display open figures and close the plotted figure.
        Defaults to True. Use False to keep the figure open for further edits.
    set : dict of str to Any, optional
        Axes properties passed to ax.set(), such as xlabel or title.
    **kwargs : Any
        Keyword arguments passed to Axes.plot().
    """
    return _quick_plot("plot", *args, fig_ax=fig_ax, figsize=figsize, show=show, set=set, **kwargs)

def scatter(
    *args: Any, fig_ax: Optional[Tuple[Figure, Axes]] = None,
    figsize: Optional[Tuple[float, float]] = None, show: bool = True,
    set: Optional[Dict[str, Any]] = None, **kwargs: Any,
) -> None:
    """Create a scatter plot using the default style.

    Parameters:
    *args : Any
        Point coordinates passed to Axes.scatter().
    fig_ax : tuple of (Figure, Axes), optional
        Figure and axes to use. Defaults to the current axes, or new axes
        if no figure is open.
    figsize : tuple of float, optional
        Width and height in inches when creating a figure. Defaults to
        opts["figure.figsize"]. Ignored when reusing a figure.
    show : bool, optional
        Whether to display open figures and close the plotted figure.
        Defaults to True. Use False to keep the figure open for further edits.
    set : dict of str to Any, optional
        Axes properties passed to ax.set(), such as xlabel or title.
    **kwargs : Any
        Keyword arguments passed to Axes.scatter().
    """
    return _quick_plot("scatter", *args, fig_ax=fig_ax, figsize=figsize, show=show, set=set, **kwargs)

def errorbar(
    *args: Any, fig_ax: Optional[Tuple[Figure, Axes]] = None,
    figsize: Optional[Tuple[float, float]] = None, show: bool = True,
    set: Optional[Dict[str, Any]] = None, **kwargs: Any,
) -> None:
    """Create an error-bar plot using the default style.

    Parameters:
    *args : Any
        Coordinates and optional errors passed to Axes.errorbar().
    fig_ax : tuple of (Figure, Axes), optional
        Figure and axes to use. Defaults to the current axes, or new axes
        if no figure is open.
    figsize : tuple of float, optional
        Width and height in inches when creating a figure. Defaults to
        opts["figure.figsize"]. Ignored when reusing a figure.
    show : bool, optional
        Whether to display open figures and close the plotted figure.
        Defaults to True. Use False to keep the figure open for further edits.
    set : dict of str to Any, optional
        Axes properties passed to ax.set(), such as xlabel or title.
    **kwargs : Any
        Keyword arguments passed to Axes.errorbar().
    """
    return _quick_plot("errorbar", *args, fig_ax=fig_ax, figsize=figsize, show=show, set=set, **kwargs)

def hist(
    *args: Any, fig_ax: Optional[Tuple[Figure, Axes]] = None,
    figsize: Optional[Tuple[float, float]] = None, show: bool = True,
    set: Optional[Dict[str, Any]] = None, **kwargs: Any,
) -> None:
    """Create a histogram using the default style.

    Parameters:
    *args : Any
        Data and optional bin settings passed to Axes.hist().
    fig_ax : tuple of (Figure, Axes), optional
        Figure and axes to use. Defaults to the current axes, or new axes
        if no figure is open.
    figsize : tuple of float, optional
        Width and height in inches when creating a figure. Defaults to
        opts["figure.figsize"]. Ignored when reusing a figure.
    show : bool, optional
        Whether to display open figures and close the plotted figure.
        Defaults to True. Use False to keep the figure open for further edits.
    set : dict of str to Any, optional
        Axes properties passed to ax.set(), such as xlabel or title.
    **kwargs : Any
        Keyword arguments passed to Axes.hist().
    """
    return _quick_plot("hist", *args, fig_ax=fig_ax, figsize=figsize, show=show, set=set, **kwargs)

def imshow(
    *args: Any, fig_ax: Optional[Tuple[Figure, Axes]] = None,
    figsize: Optional[Tuple[float, float]] = None, show: bool = True,
    set: Optional[Dict[str, Any]] = None, **kwargs: Any,
) -> None:
    """Display data as an image using the default style.

    Parameters:
    *args : Any
        Image data and optional settings passed to Axes.imshow().
    fig_ax : tuple of (Figure, Axes), optional
        Figure and axes to use. Defaults to the current axes, or new axes
        if no figure is open.
    figsize : tuple of float, optional
        Width and height in inches when creating a figure. Defaults to
        opts["figure.figsize"]. Ignored when reusing a figure.
    show : bool, optional
        Whether to display open figures and close the plotted figure.
        Defaults to True. Use False to keep the figure open for further edits.
    set : dict of str to Any, optional
        Axes properties passed to ax.set(), such as xlabel or title.
    **kwargs : Any
        Keyword arguments passed to Axes.imshow().
    """
    return _quick_plot("imshow", *args, fig_ax=fig_ax, figsize=figsize, show=show, set=set, **kwargs)

class Plot:
    """
    A class for multiple plots with a style and use similar to that of pyplot.
    All unknown methods are directly passed to the axes object.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Create a figure and axes with the default style until closed.

        Parameters:
        *args : Any
            Positional arguments passed to plt.subplots(), such as nrows
            and ncols. Multiple subplots produce an array of axes in self.ax.
        **kwargs : Any
            Keyword arguments passed to plt.subplots(), such as figsize
            or sharex.
        """
        self._context = plt.rc_context(opts)
        self._context.__enter__()
        self._closed = False

        try:
            self.fig, self.ax = plt.subplots(*args, **kwargs)
        except Exception:
            self._context.__exit__(None, None, None)
            raise

    def __getattr__(self, name: str) -> Any:
        """Forward unknown attributes to the underlying axes object.

        Parameters:
        name : str
            Name of the attribute or method to retrieve from self.ax.

        Returns:
        Any
            The requested attribute or bound method.
        """
        return getattr(self.ax, name)

    def show(self, *, legend: bool = True, close: bool = True) -> None:
        """Display the figure and optionally close it afterwards.

        Parameters:
        legend : bool, optional
            Whether to show the legend if needed. Defaults to True.
        close : bool, optional
            Whether to close the figure and restore the previous Matplotlib
            settings after displaying it. Defaults to True.
        """
        if legend:
            _show_legend_if_needed(self.ax)
        plt.show()

        if close:
            self.close()

    def close(self) -> None:
        """Close the figure and restore the previous Matplotlib settings.

        Calling this method again after closing has no effect.
        """
        if not self._closed:
            plt.close(self.fig)
            self._context.__exit__(None, None, None)
            self._closed = True

    # Use the same enter/exit interface as plt.rc_context to allow usage with the 'with' statement.
    def __enter__(self) -> "Plot":
        """Return this plot when entering a with statement.

        Returns:
        Plot
            This plot, with its figure and axes available for use.
        """
        return self

    def __exit__(
        self, exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException], traceback: Optional[TracebackType],
    ) -> None:
        """Close the figure on leaving a with statement, propagating exceptions.

        Parameters:
        exc_type : type of BaseException, optional
            Type of the exception raised in the block, or None.
        exc_value : BaseException, optional
            Exception raised in the block, or None.
        traceback : types.TracebackType, optional
            Traceback for the exception, or None.
        """
        self.close()
