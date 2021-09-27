# 模板匹配
import cv2 as cv
import numpy as np
import copy


class Match:
    def __init__(self):
        self.w_list_open = []
        self.h_list_open = []
        self.size = []
        self.image = []
        self.all = []  # 存放所有的音符坐标和音符的列表，格式为[[横坐标， 纵坐标， 音符], []]坐标为像素坐标
        self.point = []
        self.d_point = []
        self.underline = []
        self.output = []
        self.h = 16

    def match(self, img, match, thre=0.80):
        res = cv.matchTemplate(img, match, cv.TM_CCOEFF_NORMED)
        # res_open存放置信度
        loc = np.where(res >= thre)
        # loc_open 存放左上角坐标
        return loc

    def screen_(self, loc, delt=5):
        w_list = []
        h_list = []
        inside = False
        for pt in zip(*loc[::-1]):
            # print('*******************************')
            for i in self.h_list_open:
                if pt[1] > i-15 and pt[1] < i+35:
                    inside = True
            if len(w_list) == 0 and inside:
                w_list.append(pt[0])
                h_list.append(pt[1])
                continue
            count = len(w_list)
            for i, j in zip(w_list, h_list):
                # print(i, j, pt[0], pt[1])
                if abs(pt[0] - i) < delt and abs(pt[1] - j) < delt:
                    count -= 1
                    continue

            if count == len(w_list) and inside:
                w_list.append(pt[0])
                h_list.append(pt[1])
            inside = False
        # print(w_list, h_list)
        return w_list, h_list

    def screen(self, loc, delt=5):
        w_list = []
        h_list = []
        for pt in zip(*loc[::-1]):
            # print('*******************************')
            if len(w_list) == 0:
                w_list.append(pt[0])
                h_list.append(pt[1])
                continue
            count = len(w_list)
            for i, j in zip(w_list, h_list):
                # print(i, j, pt[0], pt[1])
                if abs(pt[0] - i) < delt and abs(pt[1] - j) < delt:
                    count -= 1
                    continue
            if count == len(w_list):
                w_list.append(pt[0])
                h_list.append(pt[1])
        return w_list, h_list

    def draw(self, img, loc, w, h, color=(0, 0, 255)):
        loc_ = copy.deepcopy(loc)
        count = 0
        for w_l, h_l in loc_:
            # print(w_l, h_l)
            count += 1
            bottom_right = (w_l + w, h_l + h)
            cv.rectangle(img, (w_l, h_l), bottom_right, color, 2)
        print(count)

    def pack(self, loc, count, save):
        for i in loc:
            save.append([i[0], i[1], str(count)])

    def get_underline(self, img, z):
        """
        :param img: 图像
        :param z: 输入的横坐标和纵坐标，一个字宽15左右，高22
        h: 输入字的高度，大概高26
        :return: 是否有下滑线  布尔值
        """
        h = self.h - 2
        exist = False
        for i in range(5):
            if img[z[1]+h+2+i][z[0]+8] == 0:
                exist = True
        return exist

    def run(self, path):
        img = cv.imread(path, cv.IMREAD_GRAYSCALE)
        self.size = img.shape
        _, img = cv.threshold(img, 100, 255, 0)
        match_0 = cv.imread('./image/1/0.jpg', 0)
        _, match_0 = cv.threshold(match_0, 100, 255, 0)
        match_1 = cv.imread('./image/1/1.jpg', 0)
        _, match_1 = cv.threshold(match_1, 100, 255, 0)
        match_2 = cv.imread('./image/1/2.jpg', 0)
        _, match_2 = cv.threshold(match_2, 100, 255, 0)
        match_3 = cv.imread('./image/1/3.jpg', 0)
        _, match_3 = cv.threshold(match_3, 100, 255, 0)
        match_4 = cv.imread('./image/1/4.jpg', 0)
        _, match_4 = cv.threshold(match_4, 100, 255, 0)
        match_5 = cv.imread('./image/1/5.jpg', 0)
        _, match_5 = cv.threshold(match_5, 100, 255, 0)
        match_6 = cv.imread('./image/1/6.jpg', 0)
        _, match_6 = cv.threshold(match_6, 100, 255, 0)
        match_7 = cv.imread('./image/1/7.jpg', 0)
        _, match_7 = cv.threshold(match_7, 100, 255, 0)
        match_open = cv.imread('./image/1/open.jpg', 0)
        _, match_open = cv.threshold(match_open, 100, 255, 0)
        match_point = cv.imread('./image/1/point.jpg', 0)
        _, match_point = cv.threshold(match_point, 100, 255, 0)
        match_d_point = cv.imread('./image/1/double_point.jpg', 0)
        _, match_d_point = cv.threshold(match_d_point, 100, 255, 0)
        self.h = match_7.shape[0]
        # print(self.h)
        loc_open = self.match(img, match_open, 0.7)
        loc_point = self.match(img, match_point, 0.75)
        loc_d_point = self.match(img, match_d_point)
        loc_0 = self.match(img, match_0)
        loc_1 = self.match(img, match_1)
        loc_2 = self.match(img, match_2)
        loc_3 = self.match(img, match_3)
        loc_4 = self.match(img, match_4)
        loc_5 = self.match(img, match_5)
        loc_6 = self.match(img, match_6)
        loc_7 = self.match(img, match_7)
        # w为横坐标（横着的⬇）， h为纵坐标（竖着的→）
        self.w_list_open, self.h_list_open = self.screen(loc_open, 20)
        w_list, h_list = self.screen_(loc_0, 15)
        loc_0 = zip(w_list, h_list)
        w_list, h_list = self.screen_(loc_1, 15)
        loc_1 = zip(w_list, h_list)
        w_list, h_list = self.screen_(loc_2, 15)
        loc_2 = zip(w_list, h_list)
        w_list, h_list = self.screen_(loc_3, 15)
        loc_3 = zip(w_list, h_list)
        w_list, h_list = self.screen_(loc_4, 15)
        loc_4 = zip(w_list, h_list)
        w_list, h_list = self.screen_(loc_5, 15)
        loc_5 = zip(w_list, h_list)
        w_list, h_list = self.screen_(loc_6, 15)
        loc_6 = zip(w_list, h_list)
        w_list, h_list = self.screen_(loc_7, 15)
        loc_7 = zip(w_list, h_list)
        w_list, h_list = self.screen_(loc_point, 15)
        loc_point = zip(w_list, h_list)
        w_list, h_list = self.screen_(loc_d_point, 15)
        loc_d_point = zip(w_list, h_list)

        self.pack(loc_0, 0, self.all)
        self.pack(loc_1, 1, self.all)
        self.pack(loc_2, 2, self.all)
        self.pack(loc_3, 3, self.all)
        self.pack(loc_4, 4, self.all)
        self.pack(loc_5, 5, self.all)
        self.pack(loc_6, 6, self.all)
        self.pack(loc_7, 7, self.all)
        self.pack(loc_point, 'a', self.point)
        self.pack(loc_d_point, 'aa', self.d_point)

        # 排序
        self.all = sorted(self.all, key=lambda x: x[1])
        comp = self.all[0][1]
        all_2 = [[]]
        count = 0
        for i in self.all:
            if i[1]-150 > comp:
                all_2[count-1] = sorted(all_2[count-1])
                all_2.append([])
                comp = i[1]
                count += 1
                all_2[count].append(i)
            else:
                all_2[count].append(i)
        all_2[count-1] = sorted(all_2[count-1])
        all_2[count] = sorted(all_2[count])

        for i in all_2:
            for kk in i:
                for n in self.point:
                    if n[0] > kk[0] > n[0]-20 and n[1] < kk[1] < n[1] + 35:
                        kk[2] = n[2] + kk[2]
                for nn in self.d_point:
                    if nn[0] > kk[0] > nn[0]-20 and nn[1] < kk[1] < nn[1] + 45:
                        kk[2] = nn[2] + kk[2]
        # 判断是否有下划线
        for i in all_2:
            for kk in i:
                if self.get_underline(img, kk[:2]):
                    kk[2] = 's' + kk[2]
        self.all = all_2
        for i in all_2:
            for kk in i:
                if "7" in kk[2]:
                    cv.putText(img, kk[2], (kk[0], kk[1]-30), cv.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
                self.output.append(kk[2])
        print(self.output)
        return self.output
        # img = cv.resize(img, (900, 1000))
        # cv.imshow('img', img)
        # cv.waitKey(0)


if __name__ == '__main__':
    match = Match()
    a = match.run(path='./image/hsgddj1.jpg')
    print(a)
