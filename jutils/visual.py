"""
Module with graph utilities.
"""
import plotly.express as px
import pandas as pd
from pandas import DataFrame
import numpy as np
import plotly.graph_objects as go


# noinspection GrazieInspection
class Plot:
    """
    Graficar contiene funciones para realizar gráficos predeterminados, tiene un sistema de colores semánticos
    útiles para
    """

    def __init__(self, colors=None):
        if colors is None:
            self.colors = {
                'femenine': '#ff69b4',
                'masculine': '#7858da',
                'correct': '#1CDB59',
                'incorrect': '#fa1e1e',
                'c1': '#79216d',
                'c2': '#ca1e3f',
                'c3': '#b26116',
                'c4': '#a0933a',
                'c5': '#a3f789'
            }
        else:
            self.colors = colors

        self.color_discrete_sequence = [self.colors[c] for c in ['c1', 'c2', 'c3', 'c4', 'c5']]
        self.color_continuous_scale = ["#fff", self.colors['c1']]

    def heatmap(self, df: DataFrame, x: str, y: str, aggfunc=len, fill_value=0, **kwargs) -> go.Figure:
        """
        Display a heatmap summarizing the columns x and y by aggfunc.

        :param df: Dataframe with the data.
        :param x: Column to display in the x-axis. (Categorical).
        :param y: Column to display in the y-axis. (Categorical).
        :param aggfunc: Function to summarize the data.
        :param fill_value: Value to replace nulls after the aggregation.
        :param kwargs: Aditional parameters to pass to plotly.express.imshow.
        :return: A Figure that can be displayed with the method show().
        """
        df_heatmap = df[[x, y]].pivot_table(index=y, columns=x, aggfunc=aggfunc, fill_value=fill_value)
        return px.imshow(df_heatmap, color_continuous_scale=self.color_continuous_scale, title=f'{x} vs {y}', **kwargs)

    def box(self, df: DataFrame, x: str = None, y: str = None, title: str = None, notched=True, **kwargs) -> go.Figure:
        """
        Boxplot

        :param df: Dataframe with the data.
        :param x: Column to display in the x-axis. (Categorical)
        :param y: Column to display in the y-axis. (Numerical)
        :param title: Plot title.
        :param notched: Set a notch in the plot.
        :param kwargs: Aditional parameters to pass to plotly.express.imshow.
        :return: A Figure that can be displayed with the method show().
        """
        if title is None:
            title = f'Boxplot {x} vs {y}' if x is not None else f'Boxplot {y}'
        return px.box(df, x=x, y=y, title=title, notched=notched,
                      color_discrete_sequence=self.color_discrete_sequence, **kwargs)

    def histogram(self, df=None, x=None, nbins: int = None, text_auto=True, **kwargs) -> go.Figure:
        """
        Histogram

        :param df: Dataframe with the data.
        :param x: Column to display in the x-axis. (Categorical | Numerical)
        :param nbins: Cant of bins to group the data (If x is categorical, ignores this parameter).
        :param text_auto: If False, doesn't show value labels.
        :param kwargs: Aditional parameters to pass to plotly.express.imshow.
        :return: A Figure that can be displayed with the method show().
        """
        return px.histogram(df, x=x, text_auto=text_auto,
                            color_discrete_sequence=self.color_discrete_sequence,
                            nbins=nbins,
                            **kwargs)

    def scatter(self, df: DataFrame, x: str, y: str, color: str = None, correct_incorrect_map=None,
                **kwargs) -> go.Figure:
        """
        Scatter plot

        :param df: Dataframe with the data.
        :param x: Column to display in the x-axis. (Numerical)
        :param y: Column to display in the y-axis. (Numerical)
        :param color: Column to separate points by color.
        :param correct_incorrect_map: A dictionary that maps the columns value to the assigned colors.
        :param kwargs: Aditional parameters to pass to plotly.express.imshow.
        :return: A Figure that can be displayed with the method show().
        """
        if correct_incorrect_map is None:
            color_discrete_sequence = self.color_discrete_sequence
            color_discrete_map = None
        else:
            color_discrete_sequence = None
            color_discrete_map = {
                correct_incorrect_map['correct']: self.colors['correct'],
                correct_incorrect_map['incorrect']: self.colors['incorrect']
            }
        return px.scatter(
            data_frame=df,
            x=x,
            y=y,
            color=color,
            color_discrete_sequence=color_discrete_sequence,
            color_discrete_map=color_discrete_map, **kwargs)

    def pyramid(self,
                df: DataFrame,
                x: str,
                nbins: int,
                cat_col: str,
                cat1,
                cat2,
                title: str = None,
                cat1name: str = None,
                cat2name: str = None,
                cat1color=None,
                cat2color=None
                ) -> go.Figure:
        """
        Pyramid plot

        :param df: Dataframe with the data.
        :param x: Column to display in the x-axis. (Numerical)
        :param nbins: Cant of bins to group the data.
        :param cat_col: Column containing the categories. (Categorical)
        :param cat1: Name of the first category.
        :param cat2: Name of the second category.
        :param title: Plot title.
        :param cat1name: Display name of the first category in the plot.
        :param cat2name: Display name of the second category in the plot.
        :param cat1color: Display color of the first category in the plot.
        :param cat2color: Display color of the second category in the plot.
        :return: A Figure that can be displayed with the method show().
        """
        cat1name = cat1 if cat1name is None else cat1name
        cat2name = cat2 if cat2name is None else cat2name
        cat1color = self.colors['femenine'] if cat1color is None else cat1color
        cat2color = self.colors['masculine'] if cat2color is None else cat2color
        title = f'Piramide de {cat_col} vs {x}.' if title is None else title

        minimo = df[x].min()
        maximo = df[x].max()
        limites = [round(x) for x in np.linspace(minimo, maximo, nbins)]
        labels = [f'[{lim_min}-{lim_max})'
                  for (lim_min, lim_max) in zip(limites[0:nbins - 1], limites[1:nbins])]

        bins_1 = pd.cut(df.loc[df[cat_col] == cat1][x], bins=limites, labels=labels, include_lowest=True)
        bins_2 = pd.cut(df.loc[df[cat_col] == cat2][x], bins=limites, labels=labels, include_lowest=True)

        bins_1.name = cat1name
        bins_2.name = cat2name

        grouped_1 = bins_1.groupby(bins_1).count()
        grouped_2 = bins_2.groupby(bins_2).count()

        data = pd.DataFrame([grouped_1, grouped_2]).transpose()

        y = data.index
        x_1 = data[cat1name]
        x_2 = data[cat2name] * (-1)
        meta = data[cat2name]

        fig = go.Figure()
        bar1 = go.Bar(y=y, x=x_1, name=cat1name, orientation='h',
                      texttemplate='%{x}', marker_color=cat1color)
        bar2 = go.Bar(y=y, x=x_2, name=cat2name, orientation='h',
                      texttemplate='%{meta}', marker_color=cat2color, meta=meta)
        fig.add_trace(bar1)
        fig.add_trace(bar2)
        fig.update_layout(title=title, barmode='relative', bargap=0.0,
                          bargroupgap=0)
        return fig
