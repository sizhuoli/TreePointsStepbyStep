#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 14:19:53 2021

@author: sizhuo
"""


from config import Preprocessing
from core2.preprocessing import processor

config = Preprocessing.Configuration()

prep = processor(config,boundary = 1, aux = 1)
prep.extract_normal(boundary = 1, aux = 1)

