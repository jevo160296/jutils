#!/usr/bin/env python

"""Tests for `jutils` package."""

import random
import unittest
from time import sleep

import pandas as pd

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
        rnd_gen = random.Random(x=0)
        x = ['A', 'B', 'C']
        y = ['1', '2', '3', '4']
        z = ['F', 'M']
        rows = range(5000)
        self.df = pd.DataFrame({
            'x': [x[rnd_gen.randint(0, 2)] for _ in rows],
            'y': [y[rnd_gen.randint(0, 3)] for _ in rows],
            'z': [z[rnd_gen.randint(0, 1)] for _ in rows],
            'value1': [(rnd_gen.random() - 0.5) * 2000 for _ in rows],
            'value2': [(rnd_gen.random() - 0.2) * 5500 for _ in rows]
        })
        self.plot = Plot()

    def tearDown(self):
        """Tear down test fixtures, if any."""

    @paciencia
    def test_heat_map(self):
        """Test something."""
        self.plot.heatmap(self.df, x='x', y='y', aggfunc=len, fill_value=0).show()

    @paciencia
    def test_box(self):
        """"""
        self.plot.box(self.df, x='x', y='value1').show()

    @paciencia
    def test_histogram(self):
        """"""
        self.plot.histogram(self.df, x='value1').show()
        self.plot.histogram(self.df, x='x').show()

    @paciencia
    def test_histogram_with_bins(self):
        """"""
        self.plot.histogram(self.df, x='value1', nbins=5).show()
        self.plot.histogram(self.df, x='x', nbins=5).show()

    @paciencia
    def test_scatter(self):
        """"""
        self.plot.scatter(self.df, x='value1', y='value2', color='x').show()

    @paciencia
    def test_pyramid(self):
        """"""
        self.plot.pyramid(
            self.df,
            x='value1',
            nbins=6,
            cat_col='z',
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
        self.plot.pyramid(self.df, x='value1', nbins=6, cat_col='z', cat1='F', cat2='M')
