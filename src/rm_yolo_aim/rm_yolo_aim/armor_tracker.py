import math
from loguru import logger

# 定义常量, 弧度转角度
RAD2DEG = 180 / math.pi
DEG2RAD = math.pi / 180

def select_tracking_armor(armors_dict, color):

    # 筛选垂直方向的长度大于20像素的装甲板
    filtered_height_data = {k: v for k, v in armors_dict.items() if v["height"] > 20}

    # 根据颜色筛选 0: 蓝色, 1: 红色
    if color == 0:
        filtered_color_data = {k: v for k, v in filtered_height_data.items() if v["class_id"] < 6}
    elif color == 1:
        filtered_color_data = {k: v for k, v in filtered_height_data.items() if v["class_id"] > 5}

    # 最终筛选
    if not filtered_color_data:
        tracking_armor = {}
    else:
        # 找到 center 中 x 绝对值最小的条目
        # min_abs_center_key = min(filtered_color_data.items(), key=lambda k: abs(filtered_color_data[k]["center"][0]))
        # min_abs_center_value = filtered_color_data[min_abs_center_key]

        # 在剩余选项中找出 height 最大的条目
        tracking_armor = max(filtered_color_data.items(), key=lambda item: item[1]["height"])[1]

    # logger.info(f"tracking_armor: {tracking_armor}")

    return tracking_armor

def pixel_to_angle_and_deep(tracking_armor, vfov, pic_width):
    if not tracking_armor:  # 检查 tracking_armor 是否为空
        logger.info("tracking_armor is empty, returning default values.")
        return [0, 0, 0]

    try:
        height = tracking_armor["height"]
        center = tracking_armor["center"]
        
        # 估计距离
        deep = height

        # 确保 vfov 是以弧度为单位
        vfov_radians = vfov * DEG2RAD

        # 相机 x, y 坐标系下投影面的 Z 轴距离(单位: 像素)
        focal_pixel_distance = (pic_width / 2) / math.tan(vfov_radians / 2)

        # 确保 focal_pixel_distance 不为零
        if focal_pixel_distance == 0:
            logger.warning("focal_pixel_distance is zero, returning default angles.")
            return [0, 0, deep]

        # 计算角度
        yaw   = math.atan(center[0] / focal_pixel_distance) * RAD2DEG
        pitch = math.atan(center[1] / focal_pixel_distance) * RAD2DEG

        return yaw, pitch, deep

    except Exception as e:
        logger.error(f"Error in pixel_to_angle_and_deep: {e}")
        return [0, 0, 0]


if __name__ == "__main__":

    armors_dict = {
        "179":  {"class_id": 7, "height": 290, "center": [ 1,  333]},
        "-143": {"class_id": 3, "height": 288, "center": [-143, -35]},
        "149":  {"class_id": 3, "height": 191, "center": [ 149,  36]},
        "-113": {"class_id": 2, "height": 300, "center": [ 91, -35]},
    }

    result = select_tracking_armor(armors_dict, 0)

    yaw, pitch, deep = pixel_to_angle_and_deep(result, 72)
    
    logger.info(f"yaw: {yaw:.2f}, pitch: {pitch:.2f}, deep: {deep:.2f}")