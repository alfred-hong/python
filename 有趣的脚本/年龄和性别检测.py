import cv2 as cv


def getFaceBox(net, frame, conf_threshold=0.7):
    # 获取位置
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    bboxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])
            cv.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn, bboxes


# 性别
genderProto = "gender_deploy.prototxt"
genderModel = "gender_net.caffemodel"
genderNet = cv.dnn.readNet(genderModel, genderProto)
# 性别参数
genderList = ['Male', 'Female']

# 年龄
ageProto = "age_deploy.prototxt"
ageModel = "age_net.caffemodel"
ageNet = cv.dnn.readNet(ageModel, ageProto)
# 年龄参数
ageList = ['(0 - 2)', '(4 - 6)', '(8 - 12)', '(15 - 20)', '(25 - 32)', '(38 - 43)', '(48 - 53)', '(60 - 100)']

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
padding = 20

# 人脸
faceProto = 'opencv_face_detector.pbtxt'
faceModel = 'opencv_face_detector_uint8.pb'
faceNet = cv.dnn.readNet(faceModel, faceProto)

# 读取图片
frame = cv.imread('image1.jpg')
frameFace, bboxes = getFaceBox(faceNet, frame)

for bbox in bboxes:
    face = frame[max(0, bbox[1] - padding):min(bbox[3] + padding, frame.shape[0] - 1),
           max(0, bbox[0] - padding):min(bbox[2] + padding, frame.shape[1] - 1)]
    blob = cv.dnn.blobFromImage(face, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
    genderNet.setInput(blob)
    genderPreds = genderNet.forward()
    gender = genderList[genderPreds[0].argmax()]
    print("Gender Output : {}".format(genderPreds))
    print("Gender : {}".format(gender))

    ageNet.setInput(blob)
    agePreds = ageNet.forward()
    age = ageList[agePreds[0].argmax()]
    print("Gender Output : {}".format(agePreds))
    print("Gender : {}".format(age))

    label = "{}, {}".format(gender, age)
    cv.namedWindow("Age Gender Demo", 0)
    cv.resizeWindow("Age Gender Demo", 900, 500)
    cv.putText(frameFace, label, (bbox[0], bbox[1] - 20), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 3, cv.LINE_AA)
    cv.imshow("Age Gender Demo", frameFace)
    cv.waitKey(0)