#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : RandSekai
@File    : data_moe.py
@Author  : moriwx
@Date    : 2026-04-01 19:49:52
'''

import re
import pandas as pd

INPUT_PATH = 'database/'

def link_extract(text):
    match = re.search(r'\[\[(.*?)\]\]', text)
    if match:
        return match.group(1)
    else:
        return text

def maapd_extract(text):
    match_ma = re.search(r'{{color\|#884499\|(\d{1,4})}}', text.replace("'", ''))
    match_apd = re.search(r'{{color\|#FF77DD\|(\d{1,4})}}', text)
    if match_apd:
        return (match_ma.group(1), match_apd.group(1))
    return (match_ma.group(1),) if match_ma else text
    
data = []
after_marker = False
orig_marker_line = '<!-- embed-end:originaloth -->'
with open(INPUT_PATH+'プロセカ曲.txt', 'r', encoding='utf-8') as file:
    for line in file:
        if line.strip() == orig_marker_line:
            after_marker = True
        if len(line)>=5 and line.startswith('|'):
            datai = line.lstrip('|').rstrip('\n').split('||')
            if len(datai)==17:
                orig_tag = 0 if after_marker else 1
                datai.append(orig_tag)
                data.append(datai)
            else: print(datai)
columns = ['id', 'date', 'title', 'vocal', 'bpm', 'duration', 'ez', 'nr', 'hd', 'ex',
          'maapd', 'ezn', 'nrn', 'hdn', 'exn', 'maapdn', 'info', 'orig_tag']
df = pd.DataFrame(data, columns=columns)
df.title = df.title.apply(link_extract)
df.vocal = df.vocal.apply(link_extract)
df.maapd = df.maapd.apply(maapd_extract)
df.maapdn = df.maapdn.apply(maapd_extract)

def apd_date_cal(row):
    if len(row.maapd)==2:
        apddatel = re.findall(r'\d{4}/\d{2}/\d{2}', row['info'])
        if len(apddatel)==1:
            return apddatel[0]
#         elif len(apddatel)>1: print(row)
        else:
            return row['date']
    return ''
df['appdate'] = df.apply(apd_date_cal, axis=1)

def band_genre(text):
    if text.startswith('Leo/need'):
        return 'ln'
    if text.startswith('MORE MORE JUMP!'):
        return 'mmj'
    if text.startswith('Vivid BAD SQUAD'):
        return 'vbs'
    if text.startswith('Wonderlands×Showtime'):
        return 'ws'
    if text.startswith('25点，Nightcord见。'):
        return '25'
    if text.startswith('世界计划虚拟歌手') or text.startswith('世界计划其他服务器'):
        return 'v'
    if text.startswith('世界计划其他歌曲'): # 待细分
        return 'other'
    return ''
df['band'] = df.title.apply(band_genre)
df['genre'] = df.title.str.extract(r'^(.*?)\d{0,1}#', expand=True)
df.loc[df.id.isin(['76', '77', '141', '235', '336', '366', '489', '502', '579', '585', '624', '648',
                   '726', '709',
                   '739', '743', '742'] + \
                  list(map(str, range(685, 690)))), 'band'] = 'v'
df.loc[df.id.isin(('302', '232', '233')), 'band'] = 'ln'
df.loc[df.id.isin(('400',)), 'band'] = 'mmj'
df.loc[df.id.isin(('83', '84', '150', '177', '179', '311', # ビビバスアーカイブv
    '230', '536', '555', '703')), 'band'] = 'vbs'
df.loc[df.id.isin(('234', '623')), 'band'] = 'ws'
df.loc[df.id.isin(('231', '501', '723')), 'band'] = '25'

def title_extract(text):
    match = re.search(r'\|(.*?)$', text)
    if match:
        match1 = re.search(r'^{{lj\|(.*?)}}$', match.group(1))
        if match1:
            return match1.group(1)
        return match.group(1)
    return text
df.title = df.title.apply(title_extract)

utaeru_str = '''
63 64 97 132 130 173 159 207 196 257 236 259 310 351 375 383 423 424 442 524 546 605 646 570 695 642 574 681
57 99 89 112 144 140 193 209 211 264 252 295 287 308 374 429 405 422 457 474 498 575 582 539 635 659 610 683 756
54 55 101 126 156 180 182 239 244 217 280 267 316 373 356 421 398 404 497 471 478 508 576 634 583 684 716 679 740
51 52 103 105 127 166 178 224 212 282 333 324 386 397 452 411 450 472 548 577 538 560 649 600 660 735 760
60 61 62 90 116 149 142 187 203 189 248 237 304 300 353 345 409 492 507 549 500 564 596 540 572 597 630 662 384 754
82 128 151 165 161 176 185 192 197 227 254 274 292 314 315 326 338 332 359 364 370 380 382 381 368 512 460 516 532 543 488 545 569 573 565 578 587 588 633 638 655 656 671 732 379
76 77 141 231 232 233 234 230 235 302 336 400 366 489 579 555 585 717 739 743 742

2 3 6 18 93 75 8 96 135 148 184 155 226 243 289 255 323 339 395 407 396 458
10 13 71 73 11 70 87 123 121 154 157 172 147 169 213 320 258 361 355 413 417 431 482 495 511 530 544 554 521 607 621 693 682
102 195 365 410 513 490 580 672 643
41 36 88 138 174 201 198 240 298 306 432 436 434 480 493 475 499 557 603
67 92 74 125 139 129 111 204 181 194 272 277 358 402 455 491 644 551
1 47 50 48 44 83 45 118 110 124 152 190 104 206 216 222 223 296 313 327 202 263 301 319 401 341 439 430 463 470 466 485 525 518 593 619 627 628 552 654 666 658 612 278 265
501 623 689 733

163 514 599
241 290
''' # 另：君恋クエスト