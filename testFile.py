#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 10:13:00 2018

@author: qlayerspc
"""

from subprocess import check_output

#string = check_output(['htop' ], shell=True).decode("utf-8")
#print9string)

pids = check_output(['pgrep', 'sprayFoam']).decode("utf-8").split()

print(pids)