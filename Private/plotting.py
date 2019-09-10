import seaborn as sns
import matplotlib.pyplot as plt
import io
import pandas as pd

# helper Variable
keyword_labels = "labels"
keyword_title = 'title'
data_columns = {"col", "row", "style", "hue", "size"}


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
        raise Exception("Expected exactly " + str(len(args)) + " column names")
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
    if keyword_labels in kwargs:
        if keyword_title in kwargs[keyword_labels]:
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
    df, title, kwargs = generate_plot_data(argument_names, kw_argument_names, *args, **kwargs)
    try:
        g = sns.jointplot(x=argument_names[0], y=argument_names[1], data=df, **kwargs)
        set_plot_title(g, title)
    except Exception as e:
        pass
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    return buf


def pairplot(argument_names, kw_argument_names, *args, **kwargs):
    """
    Plot pairwise relationships in a dataset.

    :param argument_names: String list of argument names. Should be in the same order as data lists
    :param kw_argument_names: String list of key word arg names. Should be in the same order as data lists
    :param args: data lists
    :param kwargs: Other arguments that can be passed to seaborn
    :return: Data URL
    """
    df, title, kwargs = generate_plot_data(argument_names, kw_argument_names, *args, **kwargs)
    try:
        g = sns.pairplot(df, **kwargs)
        set_plot_title(g, title)
    except Exception as e:
        pass
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    return buf


def distplot(argument_names, kw_argument_names, *args, **kwargs):
    df, title, kwargs = generate_plot_data(argument_names, kw_argument_names, *args, **kwargs)
    try:  # this is wrapped in a try because distplot throws a future warning that prevents execution
        sns.distplot(df[df.columns[0]], **kwargs)
        plt.title(title)
    except Exception as e:
        pass
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    return buf


def kdeplot(argument_names, kw_argument_names, *args, **kwargs):
    """
    Fit and plot a univariate or bivariate kernel density estimate.

    :param argument_names: String list of argument names. Should be in the same order as data lists
    :param kw_argument_names: String list of key word arg names. Should be in the same order as data lists
    :param x, y: data lists
    :param kwargs: Other arguments that can be passed to seaborn
    :return: Data URL
    """
    df, title, kwargs = generate_plot_data(argument_names, kw_argument_names, *args, **kwargs)
    try:
        if len(args) > 1 is None:
            sns.kdeplot(df.ix[:,0], **kwargs)
        else:
            sns.kdeplot(df.ix[:,0], df.ix[:,1], **kwargs)
        plt.title(title)
    except Exception as e:
        pass
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    return buf


def rugplot(argument_names, kw_argument_names, *args, **kwargs):
    """
    Plot datapoints in an array as sticks on an axis.

    :param a: vector
    :param kwargs: Other arguments that can be passed to seaborn
    :return: Data URL
    """
    df, title, kwargs = generate_plot_data(argument_names, kw_argument_names, *args, **kwargs)
    try:
        sns.rugplot(df.ix[:,0], **kwargs)
        plt.title(title)
    except Exception as e:
        pass
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    return buf


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
    df, title, kwargs = generate_plot_data(argument_names, kw_argument_names, *args, **kwargs)
    try:
        if len(args) == 3:
            g = sns.relplot(x=argument_names[0], y=argument_names[1], hue=argument_names[2], data=df, **kwargs)
        elif len(args) == 2:
            g = sns.relplot(x=argument_names[0], y=argument_names[1], data=df, **kwargs)
        else:
            raise Exception("At least 2 parameters expected for the relplot")
        set_plot_title(g, title)
    except Exception as e:
        pass
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    return buf


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
    df, title, kwargs = generate_plot_data(argument_names, kw_argument_names, *args, **kwargs)
    try:
        if len(args) == 3:
            g = sns.catplot(x=argument_names[0], y=argument_names[1], hue=argument_names[2], data=df, **kwargs)
        elif len(args) == 2:
            g = sns.catplot(x=argument_names[0], y=argument_names[1], data=df, **kwargs)
        else:
            g = sns.catplot(x=argument_names[0], data=df, **kwargs)
        set_plot_title(g, title)
    except Exception as e:
        pass
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    return buf


# Regression plots
def lmplot(argument_names, kw_argument_names, *args, **kwargs):
    """
    Plot data and regression model fits across a FacetGrid.

    :param argument_names: String list of argument names. Should be in the same order as data lists
    :param kw_argument_names: String list of key word arg names. Should be in the same order as data lists
    :param kwargs: Other arguments that can be passed to seaborn
    :return: Data URL
    """
    df, title, kwargs = generate_plot_data(argument_names, kw_argument_names, *args, **kwargs)
    try:
        if len(args) == 3:
            g = sns.lmplot(x=argument_names[0], y=argument_names[1], hue=argument_names[2], data=df, **kwargs)
        else:
            g = sns.lmplot(x=argument_names[0], y=argument_names[1], data=df, **kwargs)
        set_plot_title(g, title)
    except Exception as e:
        pass
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    return buf


def regplot(argument_names, kw_argument_names, *args, **kwargs):
    """
    Can be used to plot data and a linear regression model fit.

    :param argument_names: String list of argument names. Should be in the same order as data lists
    :param kw_argument_names: String list of key word arg names. Should be in the same order as data lists
    :param x, y: data lists
    :param kwargs: Other arguments that can be passed to seaborn
    :return: Data URL
    """
    df, title, kwargs = generate_plot_data(argument_names, kw_argument_names, *args, **kwargs)
    try:
        g = sns.regplot(x=argument_names[0], y=argument_names[1], data=df, **kwargs)
        set_plot_title(g, title)
    except Exception as e:
        pass
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    return buf


def residplot(argument_names, kw_argument_names, *args, **kwargs):
    """
    Plot the residuals of a linear regression.

    :param argument_names: String list of argument names. Should be in the same order as data lists
    :param kw_argument_names: String list of key word arg names. Should be in the same order as data lists
    :param x, y: data lists
    :param kwargs: Other arguments that can be passed to seaborn
    :return: Data URL
    """
    df, title, kwargs = generate_plot_data(argument_names, kw_argument_names, *args, **kwargs)
    try:
        g = sns.residplot(x=argument_names[0], y=argument_names[1], data=df, **kwargs)
        set_plot_title(g, title)
    except Exception as e:
        pass
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    return buf


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
    df, title, kwargs = generate_plot_data(argument_names, kw_argument_names, *args, **kwargs)
    try:
        g = sns.heatmap(df, **kwargs)
        set_plot_title(g, title)
    except Exception as e:
        pass
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    return buf


def clustermap(argument_names, kw_argument_names, *args, **kwargs):
    """
    Plot a matrix dataset as a hierarchically-clustered heatmap.

    :param argument_names: String list of argument names. Should be in the same order as data lists
    :param kw_argument_names: String list of key word arg names. Should be in the same order as data lists
    :param args: data lists, Rectangular data for clustering. Cannot contain NAs.
    :param kwargs: Other arguments that can be passed to seaborn
    :return: Data URL
    """
    df, title, kwargs = generate_plot_data(argument_names, kw_argument_names, *args, **kwargs)
    try:
        g = sns.clustermap(df, **kwargs)
        set_plot_title(g, title)
    except Exception as e:
        pass
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    return buf