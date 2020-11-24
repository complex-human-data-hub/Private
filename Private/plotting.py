import logging
import threading
from enum import Enum, auto
import seaborn as sns
import matplotlib.pyplot as plt
import io
import pandas as pd
from Private.graph_constants import data_columns
from Private.config import config_logger

# worked when I added config code here, rather than a function call (was writing to a file)
config_logger()
logger = logging.getLogger("plotting")
lock = threading.Lock()

# helper Variable
keyword_labels = 'labels'
keyword_title = 'title'


class GraphType(Enum):
    JOINTPLOT = auto()
    PAIRPLOT = auto()
    DISTPLOT = auto()
    KDEPLOT = auto()
    RUGPLOT = auto()
    RELPLOT = auto()
    CATPLOT = auto()
    LMPLOT = auto()
    REGPLOT = auto()
    RESIDPLOT = auto()
    HEATMAP = auto()
    CLUSTERMAP = auto()
    POINTPLOT = auto()


class PrivatePlottingException(Exception):
    """
    Allows us to separate private exceptions from more generic exceptions
    """
    pass


# plotting helper methods
def create_data_frame(argument_names, kw_argument_names, *args, **kwargs):
    """
    Creates a pandas data frame from given set of lists and column names. Each list will be taken as a column.
    It's a must to keep the same order in column names as well as the data lists.

    :param argument_names: String list of argument names. Should be in the same order as data lists
    :param kw_argument_names: String list of key word arg names. Should be in the same order as data lists
    :param args: data lists
    :return: pandas data frame
    """
    labels = {}
    args = [arg for arg in args if arg is not None]
    for kw_argument in kw_argument_names:
        kw = kw_argument.split(' = ')[0]
        kwarg_name = kw_argument.split(' = ')[1]
        if kw in data_columns and kwarg_name not in argument_names:
            argument_names.append(kwarg_name)
            args.append(kwargs[kw])
        if kw == keyword_labels:
            labels = kwargs[kw]
    if len(argument_names) != len(args):
        raise PrivatePlottingException("Expected exactly " + str(len(args)) + " column names")
    zipped_list = list(zip(*args))
    if labels:
        for n, argument_name in enumerate(argument_names):
            if argument_name in labels:
                argument_names[n] = labels[argument_name]

    df = pd.DataFrame(zipped_list, columns=argument_names)
    return df


def set_plot_title(g, title):
    """
    Sets the title and adjust to a seaborn plot
    :param g: plot
    :param title: title as string
    """
    if title:
        g.fig.subplots_adjust(top=0.9)
        g.fig.suptitle(title)


def modify_plot_kwargs(kw_arguments, kwargs):
    """
    This replace the values of the data lists in the keyword parameters with the string variable (column) name

    :param kw_arguments: String list of key word arg names. Should be in the same order as data lists
    :param kwargs: key word arg
    :return: kwarg
    """
    for kw_argument in kw_arguments:
        kw = kw_argument.split(' = ')[0]
        if kw in data_columns:
            kwargs[kw] = kw_argument.split(' = ')[1]
    if keyword_labels in kwargs:
        for kw_argument in kw_arguments:
            kw = kw_argument.split(' = ')[0]
            kw_var = kw_argument.split(' = ')[1]
            if kw in data_columns and kw_var in kwargs[keyword_labels]:
                kwargs[kw] = kwargs[keyword_labels][kw_var]
        del kwargs[keyword_labels]
    return kwargs


def generate_plot_data(argument_names, kw_argument_names, *args, **kwargs):
    """
    Uses other support functions to generate plot data
    :param argument_names: String list of argument names. Should be in the same order as data lists
    :param kw_argument_names: String list of key word arg names. Should be in the same order as data lists
    :param args: data lists
    :return: pandas data frame
    :return: data frame, title, modified kwargs
    """
    df = create_data_frame(argument_names, kw_argument_names, *args, **kwargs)
    title = ""
    if keyword_labels in kwargs and keyword_title in kwargs[keyword_labels]:
        title = kwargs[keyword_labels][keyword_title]
    kwargs = modify_plot_kwargs(kw_argument_names, kwargs)
    return df, title, kwargs


# Plotting Function Definitions
#   Distribution plots
def jointplot(argument_names, kw_argument_names, *args, **kwargs):
    """
    Can be used to plot  two variables with bivariate and univariate graphs.

    :param argument_names: String list of argument names. Should be in the same order as data lists
    :param kw_argument_names: String list of key word arg names. Should be in the same order as data lists
    :param args: data lists
    :param kwargs: Other arguments that can be passed to seaborn
    :return: Data URL
    """
    return private_plot(GraphType.JOINTPLOT, argument_names, kw_argument_names, *args, **kwargs)


def _jointplot(args, argument_names, df, kwargs):
    g = sns.jointplot(x=argument_names[0], y=argument_names[1], data=df, **kwargs)
    return g


def pairplot(argument_names, kw_argument_names, *args, **kwargs):
    """
    Plot pairwise relationships in a dataset.

    :param argument_names: String list of argument names. Should be in the same order as data lists
    :param kw_argument_names: String list of key word arg names. Should be in the same order as data lists
    :param args: data lists
    :param kwargs: Other arguments that can be passed to seaborn
    :return: Data URL
    """
    return private_plot(GraphType.PAIRPLOT, argument_names, kw_argument_names, *args, **kwargs)


def _pairplot(args, argument_names, df, kwargs):
    g = sns.pairplot(df, **kwargs)
    return g


def distplot(argument_names, kw_argument_names, *args, **kwargs):
    return private_plot(GraphType.DISTPLOT, argument_names, kw_argument_names, *args, **kwargs)


def _distplot(args, argument_names, df, kwargs):
    g = sns.displot(data=df, x=argument_names[0], **kwargs)
    return g


def kdeplot(argument_names, kw_argument_names, *args, **kwargs):
    """
    Fit and plot a univariate or bivariate kernel density estimate.

    :param argument_names: String list of argument names. Should be in the same order as data lists
    :param kw_argument_names: String list of key word arg names. Should be in the same order as data lists
    :param x, y: data lists
    :param kwargs: Other arguments that can be passed to seaborn
    :return: Data URL
    """
    return private_plot(GraphType.KDEPLOT, argument_names, kw_argument_names, *args, **kwargs)


def _kdeplot(args, argument_names, df, kwargs):
    if len(args) > 1:
        g = sns.kdeplot(x=argument_names[0], y=argument_names[1], data=df, **kwargs)
    else:
        g = sns.kdeplot(x=argument_names[0], data=df, **kwargs)
    return g


def rugplot(argument_names, kw_argument_names, *args, **kwargs):
    """
    Plot datapoints in an array as sticks on an axis.

    :param a: vector
    :param kwargs: Other arguments that can be passed to seaborn
    :return: Data URL
    """
    return private_plot(GraphType.RUGPLOT, argument_names, kw_argument_names, *args, **kwargs)


def _rugplot(args, argument_names, df, kwargs):
    if len(args) > 1:
        sns.scatterplot(data=df, x=argument_names[0], y=argument_names[1], **kwargs)
        g = sns.rugplot(data=df, x=argument_names[0], y=argument_names[1], **kwargs)
    else:
        sns.scatterplot(data=df, x=argument_names[0], **kwargs)
        g = sns.rugplot(data=df, x=argument_names[0], **kwargs)
    return g


#   Relational plots
def relplot(argument_names, kw_argument_names, *args, **kwargs):
    """
    Can be used to draw all seaborn relational plots. The kind parameter selects between different relational plots:
    scatterplot (with kind="scatter"; the default)
    lineplot (with kind="line")

    :param argument_names: String list of argument names. Should be in the same order as data lists
    :param kw_argument_names: String list of key word arg names. Should be in the same order as data lists
    :param args: data lists
    :param kwargs: Other arguments that can be passed to seaborn
    :return: Data URL
    """
    return private_plot(GraphType.RELPLOT, argument_names, kw_argument_names, *args, **kwargs)


def _relplot(args, argument_names, df, kwargs):
    if len(args) == 3:
        g = sns.relplot(x=argument_names[0], y=argument_names[1], hue=argument_names[2], data=df, **kwargs)
    elif len(args) == 2:
        g = sns.relplot(x=argument_names[0], y=argument_names[1], data=df, **kwargs)
    else:
        raise PrivatePlottingException("At least 2 parameters expected for the relplot")
    return g


#   Categorical plots
def catplot(argument_names, kw_argument_names, *args, **kwargs):
    """
    Can be used to draw all seaborn categorical plots. The kind parameter selects between different categorical plots:

    Categorical scatterplots:

    stripplot (with kind="strip"; the default)
    swarmplot (with kind="swarm")

    Categorical distribution plots:

    boxplot (with kind="box")
    violinplot (with kind="violin")
    boxenplot (with kind="boxen")

    Categorical estimate plots:

    pointplot (with kind="point")
    barplot (with kind="bar")
    countplot (with kind="count")


    :param argument_names: String list of argument names. Should be in the same order as data lists
    :param kw_argument_names: String list of key word arg names. Should be in the same order as data lists
    :param args: data lists
    :param kwargs: Other arguments that can be passed to seaborn
    :return: Data URL
    """
    return private_plot(GraphType.CATPLOT, argument_names, kw_argument_names, *args, **kwargs)


def _catplot(args, argument_names, df, kwargs):
    if len(args) == 3:
        g = sns.catplot(x=argument_names[0], y=argument_names[1], hue=argument_names[2], data=df, **kwargs)
    elif len(args) == 2:
        g = sns.catplot(x=argument_names[0], y=argument_names[1], data=df, **kwargs)
    else:
        g = sns.catplot(x=argument_names[0], data=df, **kwargs)
    return g


# Regression plots
def lmplot(argument_names, kw_argument_names, *args, **kwargs):
    """
    Plot data and regression model fits across a FacetGrid.

    :param argument_names: String list of argument names. Should be in the same order as data lists
    :param kw_argument_names: String list of key word arg names. Should be in the same order as data lists
    :param kwargs: Other arguments that can be passed to seaborn
    :return: Data URL
    """
    return private_plot(GraphType.LMPLOT, argument_names, kw_argument_names, *args, **kwargs)


def _lmplot(args, argument_names, df, kwargs):
    if len(args) == 3:
        g = sns.lmplot(x=argument_names[0], y=argument_names[1], hue=argument_names[2], data=df, **kwargs)
    else:
        g = sns.lmplot(x=argument_names[0], y=argument_names[1], data=df, **kwargs)
    return g


def regplot(argument_names, kw_argument_names, *args, **kwargs):
    """
    Can be used to plot data and a linear regression model fit.

    :param argument_names: String list of argument names. Should be in the same order as data lists
    :param kw_argument_names: String list of key word arg names. Should be in the same order as data lists
    :param x, y: data lists
    :param kwargs: Other arguments that can be passed to seaborn
    :return: Data URL
    """
    return private_plot(GraphType.REGPLOT, argument_names, kw_argument_names, *args, **kwargs)


def _regplot(args, argument_names, df, kwargs):
    g = sns.regplot(x=argument_names[0], y=argument_names[1], data=df, **kwargs)
    return g


def residplot(argument_names, kw_argument_names, *args, **kwargs):
    """
    Plot the residuals of a linear regression.

    :param argument_names: String list of argument names. Should be in the same order as data lists
    :param kw_argument_names: String list of key word arg names. Should be in the same order as data lists
    :param x, y: data lists
    :param kwargs: Other arguments that can be passed to seaborn
    :return: Data URL
    """
    return private_plot(GraphType.RESIDPLOT, argument_names, kw_argument_names, *args, **kwargs)


def _residplot(args, argument_names, df, kwargs):
    g = sns.residplot(x=argument_names[0], y=argument_names[1], data=df, **kwargs)
    return g


# Matrix plots
def heatmap(argument_names, kw_argument_names, *args, **kwargs):
    """
    Plot rectangular data as a color-encoded matrix.

    :param argument_names: String list of argument names. Should be in the same order as data lists
    :param kw_argument_names: String list of key word arg names. Should be in the same order as data lists
    :param args: data lists, 2D dataset that can be coerced into an ndarray.
    :param kwargs: Other arguments that can be passed to seaborn
    :return: Data URL
    """
    return private_plot(GraphType.HEATMAP, argument_names, kw_argument_names, *args, **kwargs)


def _heatmap(args, argument_names, df, kwargs):
    g = sns.heatmap(df, **kwargs)
    return g


def clustermap(argument_names, kw_argument_names, *args, **kwargs):
    """
    Plot a matrix dataset as a hierarchically-clustered heatmap.

    :param argument_names: String list of argument names. Should be in the same order as data lists
    :param kw_argument_names: String list of key word arg names. Should be in the same order as data lists
    :param args: data lists, Rectangular data for clustering. Cannot contain NAs.
    :param kwargs: Other arguments that can be passed to seaborn
    :return: Data URL
    """
    return private_plot(GraphType.CLUSTERMAP, argument_names, kw_argument_names, *args, **kwargs)


def _clustermap(args, argument_names, df, kwargs):
    g = sns.clustermap(df, **kwargs)
    return g


def pointplot(argument_names, kw_argument_names, *args, **kwargs):
    """
    Plot a matrix dataset as a hierarchically-clustered heatmap.

    :param argument_names: String list of argument names. Should be in the same order as data lists
    :param kw_argument_names: String list of key word arg names. Should be in the same order as data lists
    :param args: data lists, Rectangular data for clustering. Cannot contain NAs.
    :param kwargs: Other arguments that can be passed to seaborn
    :return: Data URL
    """
    return private_plot(GraphType.POINTPLOT, argument_names, kw_argument_names, *args, **kwargs)


def _pointplot(args, argument_names, df, kwargs):
    if len(args) == 3:
        g = sns.pointplot(x=argument_names[0], y=argument_names[1], hue=argument_names[2], data=df, **kwargs)
    elif len(args) == 2:
        g = sns.pointplot(x=argument_names[0], y=argument_names[1], data=df, **kwargs)
    else:
        g = sns.pointplot(x=argument_names[0], data=df, **kwargs)
    return g


plot_types = {
    GraphType.JOINTPLOT: _jointplot,
    GraphType.PAIRPLOT: _pairplot,
    GraphType.DISTPLOT: _distplot,
    GraphType.KDEPLOT: _kdeplot,
    GraphType.RUGPLOT: _rugplot,
    GraphType.RELPLOT: _relplot,
    GraphType.CATPLOT: _catplot,
    GraphType.LMPLOT: _lmplot,
    GraphType.REGPLOT: _regplot,
    GraphType.RESIDPLOT: _residplot,
    GraphType.HEATMAP: _heatmap,
    GraphType.CLUSTERMAP: _clustermap,
    GraphType.POINTPLOT: _pointplot
}


def private_plot(plot_type, argument_names, kw_argument_names, *args, **kwargs):
    df, title, kwargs = generate_plot_data(argument_names, kw_argument_names, *args, **kwargs)
    lock.acquire()
    plt.figure()
    try:
        g = plot_types[plot_type](args, argument_names, df, kwargs)
        set_plot_title(g, title)
    except Exception:
        pass
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.clf()
    plt.close()
    lock.release()
    return buf
