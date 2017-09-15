#!/usr/bin/env python

import os
import sys
import json 
import argparse

HEADER='''
# Generated palette file
# Colorbrewer palette: %s %s
# %d colours
# 
'''

def write_palette(base_name,palette,modifier='',dest='.'):
  suffix = ''
  if modifier:
    suffix = '_%s'%modifier[:3]

  fn = os.path.join(dest,'%s_%d%s.pal'%(base_name,len(palette),suffix))
  f = open(fn,'w')
  f.write(HEADER%(base_name,modifier,len(palette)))
  for col in palette:
    col = col[4:-1].split(',')
    f.write("%s %s %s\n"%tuple(col))
  f.close()

def write_palettes(dest): 
  if not os.path.exists(dest):
    os.makedirs(dest)

  brewer = json.load(open('colorbrewer.json'))

  for palette_name,palettes in brewer.items():
    for count,palette in palettes.items():
      try:
        count = int(count)
        write_palette(palette_name,palette,dest=dest)
        write_palette(palette_name,palette[::-1],'reversed',dest=dest)
      except:
        continue

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Generate colour palette files for THREDDS/ncWMS based on the colorbrewer2 color advice.')
  parser.add_argument('dest',help='destination directory')
  args = parser.parse_args()

  write_palettes(args.dest)

