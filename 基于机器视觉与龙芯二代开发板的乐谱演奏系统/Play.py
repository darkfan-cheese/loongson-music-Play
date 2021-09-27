import wave
import os
import data
import match

class Play:
    def __init__(self):
        self.path = './source'
        self.files = {}
        self.outpath = './output/output.wav'


    def get(self):
        for filename in os.listdir(self.path):
            file = str(os.path.join(self.path, filename))
            file = file.replace('\\', '/')  # 获取每个音频文件
            # print(filename)
            self.files[filename.split('.')[0]] = file

    def play(self, data):
        song_data = []
        for i in data:
            # print(i)
            if i == 'a0' or i == 'aa0':
                i = '0'
            if i == 'sa0' or i == 'saa0':
                i = 's0'
            if 'aaa' in i:
                # print('进行替换')
                i = i.replace('aaa', 'aa')
            w = wave.open(self.files[i], 'rb')
            song_data.append([w.getparams(), w.readframes(w.getnframes())])
            w.close()
        output = wave.open(self.outpath, 'wb')
        output.setparams(song_data[0][0])
        for j in range(len(song_data)):
            output.writeframes(song_data[j][1])
        output.close()
        return True


if __name__ == '__main__':
    match1 = match.Match()
    # data = data.Music()
    song = match1.run('./image/hsgddj1.jpg')
    match2 = match.Match()
    song2 = match2.run('./image/hsgddj2.jpg')
    play = Play()
    play.get()
    # print(song.extend(song2))
    play.play(song+song2)
