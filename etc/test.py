#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import numpy as np
import csv


if __name__ == '__main__':
    dirpath = os.path.dirname(__file__)
    print(dirpath)

    nfnet_data = './nfnet_book_catalog_k100_th9_0729.tsv'
    resnet_data = './resnet_sim_img_result_20210803.tsv'
    gt_data = './true_catalog_data_.tsv'

    # data loading and dict
    nfnet_dict = dict()
    resnet_dict = dict()
    gt_dict = dict()

    with open(gt_data, mode='r', encoding='utf-8') as gfo:
        f_reader = csv.reader(gfo, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)

        for counter, row in enumerate(f_reader):
            ctlg_no = row[0]
            prd_no = row[3]

            if ctlg_no in gt_dict:
                gt_dict[ctlg_no].append(prd_no)
            else:
                gt_dict[ctlg_no] = [prd_no]


    print('gt_dict done')


    resnet_ctlg_list = list()
    with open(resnet_data, mode='r', encoding='utf-8') as gfo:
        f_reader = csv.reader(gfo, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)

        match_ctlg_cnt = 0
        for counter, row in enumerate(f_reader):
            ctlg_no = row[0]
            prd_list = row[1].split(',')

            if ctlg_no in gt_dict:
                match_ctlg_cnt += 1
                resnet_ctlg_list.append(ctlg_no)
                resnet_dict[ctlg_no] = prd_list

        print('[resnet] match_ctlg_cnt', match_ctlg_cnt)

    nfnet_ctlg_list = list()
    with open(nfnet_data, mode='r', encoding='utf-8') as gfo:
        f_reader = csv.reader(gfo, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)

        match_ctlg_cnt = 0
        for counter, row in enumerate(f_reader):
            ctlg_no = row[0]
            prd_list = row[1].split(',')

            if ctlg_no in gt_dict:
                match_ctlg_cnt += 1
                nfnet_ctlg_list.append(ctlg_no)
                nfnet_dict[ctlg_no] = prd_list

        print('[nfnet] match_ctlg_cnt', match_ctlg_cnt)


    # 각 결과 비교
    diff_nfnet = list(set(nfnet_ctlg_list) - set(resnet_ctlg_list))
    diff_resnet = list(set(resnet_ctlg_list) - set(nfnet_ctlg_list))

    print(len(diff_nfnet))
    print(diff_resnet)

    # nfnet, resnet 모두 있는 ctlg_no는 8326개
    # 일단 해당 데이터에 대해서만이라도 정답셋과 비교한다면?
    # 해당 카탈로그번호에 대한 정답셋 데이터 추출
    # 해당 번호에 대한 유사도 그룹핑 결과 추출

    match_ctlg_list = nfnet_ctlg_list

    match_gt_dict = dict()
    match_resnet_dict = dict()
    match_nfnet_dict = dict()

    for ctlg_no in match_ctlg_list:
        if ctlg_no in gt_dict:
            match_gt_dict[ctlg_no] = gt_dict[ctlg_no]

        if ctlg_no in resnet_dict:
            match_resnet_dict[ctlg_no] = resnet_dict[ctlg_no]

        if ctlg_no in nfnet_dict:
            match_nfnet_dict[ctlg_no] = nfnet_dict[ctlg_no]


    print(len(match_gt_dict))
    print(len(match_resnet_dict))
    print(len(match_nfnet_dict))

    # gt vs resnet
    gt_resnet_result_dict = dict()
    sum_precision = 0
    non_precision_cnt = 0
    for ctlg_no, prd_list in match_gt_dict.items():
        gt_resnet_list = list(set(prd_list) - set(match_resnet_dict[ctlg_no]))
        # false positive : resnet은 정답이라고 찾은 상품이 실제 gt 안에 없음
        resnet_gt_list = list(set(match_resnet_dict[ctlg_no]) - set(prd_list))

        tp_list = [i for i,j in zip(prd_list, match_resnet_dict[ctlg_no]) if i == j]

        len_gt_resnet = len(gt_resnet_list)
        len_resnet_gt = len(resnet_gt_list)
        len_tp_list = len(tp_list)

        if len_tp_list + len_resnet_gt != 0:
            precision = len_tp_list / (len_tp_list + len_resnet_gt)
            sum_precision += precision
        else:
            precision = None
            non_precision_cnt += 1

        gt_resnet_result_dict[ctlg_no] = gt_resnet_list, len_gt_resnet, resnet_gt_list, len_resnet_gt, tp_list, len_tp_list, precision


    print(len(gt_resnet_result_dict))
    print('[resnet] non_precision_cnt', non_precision_cnt)
    print('[resnet] average precision : ', sum_precision / (len(gt_resnet_result_dict) - non_precision_cnt) )

    # gt vs nfnet
    gt_nfnet_result_dict = dict()
    sum_precision = 0
    non_precision_cnt = 0
    for ctlg_no, prd_list in match_gt_dict.items():
        gt_nfnet_list = list(set(prd_list) - set(match_nfnet_dict[ctlg_no]))
        # false positive : nfnet은 정답이라고 찾은 상품이 실제 gt 안에 없음
        nfnet_gt_list = list(set(match_nfnet_dict[ctlg_no]) - set(prd_list))

        tp_list = [i for i, j in zip(prd_list, match_resnet_dict[ctlg_no]) if i == j]

        len_gt_nfnet = len(gt_nfnet_list)
        len_nfnet_gt = len(nfnet_gt_list)
        len_tp_list = len(tp_list)

        if len_tp_list + len_nfnet_gt != 0:
            precision = len_tp_list / (len_tp_list + len_nfnet_gt)
            sum_precision += precision
        else:
            precision = None
            non_precision_cnt += 1


        gt_nfnet_result_dict[ctlg_no] = gt_nfnet_list, len_gt_nfnet, nfnet_gt_list, len_nfnet_gt, tp_list, len_tp_list, precision

    print(len(gt_nfnet_result_dict))
    print('[nfnet] non_precision_cnt', non_precision_cnt)
    print('[nfnet] average precision : ', sum_precision / (len(gt_nfnet_result_dict) - non_precision_cnt))



    print('done')