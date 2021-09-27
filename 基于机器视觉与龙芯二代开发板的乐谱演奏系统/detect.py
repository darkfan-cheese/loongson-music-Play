import cv2
import numpy as np
import time

def detect(image_loc=''):
    #start = time.time()
    with open('./data/custom/classes.names','r') as file:
        LABELS = file.read().splitlines() #变为列表形式['person', 'bicycle', 'car']

    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

    args = {
        "video": "./VID_20201111_161423.mp4",
        "confidence": 0.5,              # minimum bounding box confidence
        "threshold": 0.1,               # NMS threshold
    }
    weightsPath = './yuepu.weights'
    configPath = './config/yolov3-custom.cfg'

    # cap = cv2.VideoCapture(0)
    # while cap.isOpened():
    #     (fram,image)=cap.read()
    #
    #     #cv2.imwrite('./figures/'+str(1)+'JPG', image)
    #
    #     #image = cv2.imread('./figures/'+str(1)+'JPG')
    image = cv2.imread(image_loc)

    (H, W) = image.shape[:2]

    #将图像转化为输入的标准格式
    #对原图像进行像素归一化1/255.0，缩放尺寸 (416, 416),，对应训练模型时cfg的文件 交换了R与G通道
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (288, 288),swapRB=True, crop=False)
    net = cv2.dnn.readNetFromDarknet(configPath,weightsPath) #加载模型权重文件
    net.setInput(blob) #将blob设为输入
    ln = net.getUnconnectedOutLayersNames()  #找到输出层 draknet中有三个输出层‘yolo_82’, ‘yolo_94’, ‘yolo_106’
    layerOutputs = net.forward(ln) # ln此时为输出层名称，向前传播，得到检测结果


    boxes, confidences, classIDs = [], [], []
    for output in layerOutputs:  #对三个输出层 循环
        for detection in output: #对每个输出层中的每个检测框循环
        # [5:] 代表从第6个开始分割

            confidence = detection[4] #得到置信度的值

        #根据置信度筛选
            if confidence > args['confidence']:
                scores = detection[5:]  # detection=[x,y,h,w,c,class1,class2,class3，class4。。。。。。]
                classID = np.argmax(scores)  # 找出最大值的索引，即哪一类是最大值
            # 得到box框的（x,y,h,w）
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
            # 把预测框中心坐标转换成框的左上角坐标(x,y)
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    # 提取出来的框有重复，所以要进行非极大值抑制处理
    #[1.需要操作的各矩形框  2.矩形框对应的置信度  3.置信度的阈值，低于这个阈值的框直接删除  4.NMS的阈值]
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],args["threshold"])
    #print('idxs形状为：',idxs.shape)

    # if len(idxs) > 0 :
    #     for i in idxs.flatten():# indxs是二维的，第0维是输出层，所以这里把它展平成1维
    #         (x, y) = (boxes[i][0], boxes[i][1])
    #         (w, h) = (boxes[i][2], boxes[i][3])


            #color = [int(c) for c in COLORS[classIDs[i]]]
            #cv2.rectangle(image,(x,y),(x+w,y+h),color,2)
            #text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
            #cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)

    #print('程序运行时间：', time.time() - start,'秒')
    #image = cv2.resize(image,(500,700))
    #cv2.imshow('Image',image)
    #cv2.waitKey(0)
    return boxes, len(idxs)