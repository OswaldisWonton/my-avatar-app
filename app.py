import streamlit as st
import cv2
import numpy as np
import random
from utils.face_utils import FaceComparison
from utils.video_display import video_display, get_video_list

try:
    from utils.face_utils import FaceComparison
    print("FaceComparison 导入成功！")
except Exception as e:
    print("导入失败，错误信息：", e)

# 初始化人脸识别模型
face_model = FaceComparison(device="cpu")  # 确保创建实例

# Streamlit 界面
st.title("AIGC盲盒:定制属于你的动物形象🎁 AIGC Blind Box: Customize Your Own Animal Avatar🐾")

# 上传图像文件
uploaded_file = st.file_uploader("请上传您的个人照片（注意脸部不要有遮挡） Please upload your photo, thanks!🩵", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 将上传的文件读取为 OpenCV 图像格式
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # 显示上传的图像
    st.image(frame, channels="BGR", caption="上传的图像", use_column_width=True)

    # 检测是否有有效的人脸
    if not face_model.has_face(frame):  # 使用 has_face 方法
        st.error("未检测到人脸，请上传包含清晰人脸的图片。")
    else:
        # 正常处理逻辑
        result = []
        face_model.comparison(frame, result)

        # 检查 result 是否为空
        if not result:  # 如果 result 为空
            st.error("无法识别您的脸型，请尝试上传另一张图片。")
        else:
            st.success(f"检测成功！您的脸型被识别为：{result[0]}")

    # 初始化人脸模型
    face_model = FaceComparison("cpu")

    # 开始人脸对比
    result = []
    face_model.comparison(frame, result)

    if result[0]:
        face_label = result[0]
        st.write(f"🌈 您的AIGC盲盒已开启, {face_label} 形象如下, 请签收! 注意看, 还有植物元素融入其中, 你能猜到是什么植物吗？🎨 ")

        # 选择对应的视频和音乐文件
        video_dict = get_video_list("videos")
        video_path = random.choice(video_dict[face_label])

        # 播放视频
        st.video(video_path)
