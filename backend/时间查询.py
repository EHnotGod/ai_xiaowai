from datetime import datetime
import pytz

def get_beijing_time():
    """
    获取当前北京时间，并返回格式化后的时间字符串和星期几
    :return: 包含北京时间和星期几的字典
    """
    # 获取当前UTC时间
    utc_now = datetime.utcnow()
    # 将UTC时间转换为北京时间
    beijing_tz = pytz.timezone('Asia/Shanghai')
    beijing_time = utc_now.replace(tzinfo=pytz.utc).astimezone(beijing_tz)
    # 格式化时间为字符串
    beijing_time_str = beijing_time.strftime('%Y-%m-%d %H:%M:%S')
    # 计算星期几
    weekday_num = beijing_time.weekday()
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    weekday_str = weekdays[weekday_num]
    # 返回结果
    return "现在是北京时间" + beijing_time_str + "，" + weekday_str
