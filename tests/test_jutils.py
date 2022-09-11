#!/usr/bin/env python

"""Tests for `jutils` package."""

import unittest
from time import sleep

import pandas as pd
import numpy as np

from jutils.visual import Plot


def paciencia(funcion, tiempo=10):
    """Paciencia"""
    def _wrapper(self, **kwargs):
        funcion(self, **kwargs)
        sleep(tiempo)
    return _wrapper


class TestJutils(unittest.TestCase):
    """Tests for `jutils` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        category1 = ['F', 'M']
        category2 = ['A', 'B', 'C']
        category3 = ['1', '2', '3', '4']
        cant = 5000
        self.df = pd.DataFrame({
            'category1': np.random.choice(category1, cant),
            'category2': np.random.choice(category2, cant),
            'category3': np.random.choice(category3, cant),
            'value1': np.random.randint(-1200, 4000, cant),
            'value2': np.random.randint(4000, 11000, cant)
        })
        self.plot = Plot()

    def tearDown(self):
        """Tear down test fixtures, if any."""

    @paciencia
    def test_heat_map(self):
        """Test something."""
        self.plot.heatmap(self.df, x='category2', y='category3', aggfunc=len, fill_value=0).show()

    @paciencia
    def test_box(self):
        """"""
        self.plot.box(self.df, x='category2', y='value1').show()

    def test_box_numeric_numeric(self):
        """"""
        self.plot.box(self.df, x='value1', y='value2').show()

    @paciencia
    def test_histogram(self):
        """"""
        self.plot.histogram(self.df, x='value1').show()
        self.plot.histogram(self.df, x='category2').show()

    @paciencia
    def test_histogram_with_bins(self):
        """"""
        self.plot.histogram(self.df, x='value1', nbins=5).show()
        self.plot.histogram(self.df, x='category2', nbins=5).show()


    @paciencia
    def test_scatter(self):
        """"""
        self.plot.scatter(self.df, x='value1', y='value2', color='category2').show()

    @paciencia
    def test_pyramid(self):
        """"""
        self.plot.pyramid(
            self.df,
            x='value1',
            nbins=6,
            cat_col='category1',
            cat1='F',
            cat1name='Femenino',
            cat1color=self.plot.colors['femenine'],
            cat2='M',
            cat2name='Masculino',
            cat2color=self.plot.colors['masculine']
        ).show()

    @paciencia
    def test_pyramid_defaults(self):
        """"""
        self.plot.pyramid(self.df, x='value1', nbins=6, cat_col='category1', cat1='F', cat2='M').show()
