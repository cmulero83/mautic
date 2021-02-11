#!/bin/bash
#-*- ENCODING: UTF-8 -*-

source Desktop/Mailshield/mautic/entorno/bin/activate
nohup python Desktop/Mailshield/mautic/vtiger_to_mautic.py
deactivate


