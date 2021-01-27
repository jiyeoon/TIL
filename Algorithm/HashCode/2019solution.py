

import random
import collections
import numpy as np
from tqdm import tqdm

random.seed(42)

REARRANGE_FOR_MERGE = True
MERGE_WINDOW = 10000
ARRANGE_WINDOW = 10000

def read_file(file_path):
    with open(file_path) as f:
        pictures = [row.strip().split() for row in f.readlines()[1:]]
    
    pic_tags = {}
    horizontal_photos = [] # horizontal photos only
    vertical_photos = [] # vertical photos only
    
    for i, pictures in enumerate(pictures):
        pic_tags[i] = set(pictures[2:]) # 태그들 넣음
        if pictures[0] == "H":
            horizontal_photos.append(i)
        elif pictures[0] == "V":
            vertical_photos.append(i)
    
    return pic_tags, horizontal_photos, vertical_photos

file_path = './input/'
pic_tags, horizontal_photos, vertical_photos = read_file(file_path)

# 태그들이 주어질 때 점수 산정 방법입니다. 
def calc_tags_pair_score(tags1, tags2):
    return min(len(tags1 & tags2), len(tags1 - tags2), len(tags2 - tags1))

# idx가 의미하는게 무엇일까??? 
def calc_idxs_pair_score(idxs1, idxs2):
    # given two tuples of indices, calculate the score
    return calc_tags_pair_score(
        set.union(*[pic_tags[idx] for idx in idxs1]),
        set.union(*[pic_tags[idx] for idx in idxs2]))

def calc_idxs_pair_score_max(idxs1, idxs2):
    # given two tuples of indices, calculate the maximum possible score by tag length
    return min(len(set.union(*[pic_tags[idx] for idx in idxs1])),
               len(set.union(*[pic_tags[idx] for idx in idxs2])))//2

# 점수 산정 방법. 슬라이드들의 순서가 주어지면 점수를 계산한다. 
def calc_sequence(idxs_lst):
    # given the sequence of indices, calculate the score
    check_validity(idxs_lst)
    score = 0
    for before, after in zip(idxs_lst[:-1], idxs_lst[1:]):
        score += calc_idxs_pair_score(before, after)            
    return score

def calc_sequence_max(idxs_lst):
    # given the sequence of indices, calculate the score
    check_validity(idxs_lst)
    score = 0
    for before, after in zip(idxs_lst[:-1], idxs_lst[1:]):
        score += calc_idxs_pair_score_max(before, after)            
    return score

def check_validity(idxs_lst):
    all_pics = [idx for idxs in idxs_lst for idx in idxs]
    if len(all_pics) != len(set(all_pics)):
        print("Duplicates found")
    all_verts = [idx for idxs in idxs_lst for idx in idxs if len(idxs) == 2]
    if (set(all_verts) - set(vertical_photos)):
        print("Horizontal photos found in vertical combinations")
    all_horis = [idx for idxs in idxs_lst for idx in idxs if len(idxs) == 1]
    if (set(all_horis) - set(horizontal_photos)):
        print("Vertical photos found in horizontal arrangement")