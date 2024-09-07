import json
import requests
import random
import time
from urllib.parse import urlparse, parse_qs
import re
import os
from datetime import datetime, timedelta

API_URL = "https://api.weibo.cn/2/cardlist"
SIGN_URL = "https://api.weibo.cn/2/page/button"
# weibo_my_cookie = "https://api.weibo.cn/2/cardlist?gsid=_2A25L3cd1DeRxGeNN4lIT9S3KyzWIHXVmy129rDV6PUJbkdANLUPjkWpNSZIzhy-1vEAWvOTW2OzRlH3i1i83YEvz&wm=3333_2001&launchid=10000365--x&b=0&from=10D1093010&c=iphone&networktype=wifi&v_p=90&skin=default&v_f=1&s=6adc3325&lang=zh_CN&sflag=1&ua=iPhone12,1__weibo__13.1.0__iphone__os16.4.1&ft=0&aid=01A_H3R1DJltBVOq43_YwyFz-i-tgKOfKgn-iJm1YlPbhl2kk.&lcardid=&sg_page_search=1&luicode=10000011&orifid=profile_me%24%24231093_-_chaohua&sg_card201_2_enable=1&containerid=232478_-_bottom_mine_followed&sourcetype=page&sg_one_checkin_enable=1&sgtotal_activity_enable=1&sg_cp_template_enable=1&need_head_cards=0&pd_redpacket2022_enable=1&sg_wish2_enable=1&sg_page_tab_wbox_enable=1&is_push_alert=1&sgpage_newprofile_enable=1&enable_card214_hot_discuss=1&need_new_pop=1&card210_grade_enable=1&profile_toolbar_refactor=1&is_auto_scroll=1&card199_realtime_enable=1&client_key=82933924bf998e81f9e3172ab92d3555&lfid=231093_-_chaohua&card199_match_info_enable=1&count=20&is_winter_olympics_enable=1&sg_diamond_skin_enable=1&sg_airborne_theme_enable=1&card182_schedule_enable=1&page=1&uicode=10001387&card204_enable=1&tz=Asia%2FShanghai&supergroup_album_v2=1&card196_videolive_enable=1&sys_notify_open=0&card211_enable=1&sg_wishing_well_enable=1&refresh_type=0&oriuicode=10000011_10000011&mix_media_enable=1&st_bottom_bar_new_style_enable=1&support_switch_sort_enable=1&fid=232478_-_bottom_mine_followed&sg_search_person_topic_card_c60_enable=1&image_type=heif&card159164_emoji_enable=1&sg_page_header_v2=1&moduleID=pagecard&ul_sid=7BA35572-C991-4658-A799-BF6C550072B8&ul_hid=8242FC08-D2D6-4967-8D4F-1F7E983831A4&ul_ctime=1725554049738"
weibo_my_cookie = "https://api.weibo.cn/2/cardlist?gsid=_2A25L2PvgDeRxGeFM7lER-C3Jzz6IHXVmzAgorDV6PUJbkdANLXP1kWpNQN6a0EXgp1rb6_s9X9Sc8d_1LBRl_lRz&wm=3333_2001&launchid=10000365--x&b=0&from=10D1093010&c=iphone&networktype=wifi&v_p=90&skin=default&v_f=1&s=9a8f945c&lang=zh_CN&sflag=1&ua=iPhone12,1__weibo__13.1.0__iphone__os16.4.1&ft=0&aid=01A_H3R1DJltBVOq43_YwyFz-i-tgKOfKgn-iJm1YlPbhl2kk.&lcardid=&luicode=10000011&orifid=profile_me%24%24231093_-_chaohua&sg_page_search=1&sg_card201_2_enable=1&page_interrupt_enable=1&containerid=232478_-_bottom_mine_usual_visit&sourcetype=page&sg_one_checkin_enable=1&sgtotal_activity_enable=1&sg_cp_template_enable=1&need_head_cards=0&pd_redpacket2022_enable=1&sg_wish2_enable=1&sg_page_tab_wbox_enable=1&is_push_alert=1&sgpage_newprofile_enable=1&enable_card214_hot_discuss=1&need_new_pop=1&card210_grade_enable=1&profile_toolbar_refactor=1&is_auto_scroll=1&card199_realtime_enable=1&client_key=82933924bf998e81f9e3172ab92d3555&lfid=231093_-_chaohua&card199_match_info_enable=1&count=20&is_winter_olympics_enable=1&sg_diamond_skin_enable=1&sg_airborne_theme_enable=1&card182_schedule_enable=1&page=1&uicode=10001387&card204_enable=1&tz=Asia%2FShanghai&supergroup_album_v2=1&card196_videolive_enable=1&sys_notify_open=0&card211_enable=1&sg_wishing_well_enable=1&refresh_type=0&oriuicode=10000011_10000011&mix_media_enable=1&st_bottom_bar_new_style_enable=1&support_switch_sort_enable=1&fid=232478_-_bottom_mine_usual_visit&sg_search_person_topic_card_c60_enable=1&image_type=heif&card159164_emoji_enable=1&sg_page_header_v2=1&moduleID=pagecard&ul_sid=D026B342-AB6C-4829-B68B-4D14975A1BE7&ul_hid=D026B342-AB6C-4829-B68B-4D14975A1BE7&ul_ctime=1725729914618"

def send_request(url, params, headers):
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            return None
    return None


def extract_params(url):
    parsed_url = urlparse(url)
    params_from_url = parse_qs(parsed_url.query)
    params_from_url = {k: v[0] for k, v in params_from_url.items()}
    return params_from_url

def qqemail(subject, email, text):
    # QQ 邮箱 SMTP 服务器授权码
    key = 'czpwtypwvsxebcba'  # 换成你的 QQ 邮箱 SMTP 授权码
    EMAIL_ADDRESS = '760985953@qq.com'  # 换成你的 QQ 邮箱地址
    EMAIL_PASSWORD = key

    import smtplib
    from email.message import EmailMessage
    import ssl

    # 配置 SSL 上下文
    context = ssl.create_default_context()

    # 设置发件人和收件人
    sender = EMAIL_ADDRESS  # 发件邮箱
    receiver = email  # 收件邮箱，可以是 QQ 邮箱或其他邮箱

    # 构建邮件内容
    msg = EmailMessage()
    msg['Subject'] = subject  # 邮件主题
    msg['From'] = sender  # 发件人
    msg['To'] = receiver  # 收件人
    msg.set_content(text)  # 邮件正文内容

    # 使用 SSL 连接 QQ 邮箱的 SMTP 服务器并发送邮件
    try:
        with smtplib.SMTP_SSL("smtp.qq.com", 465, context=context) as smtp:  # 使用 SSL 加密连接
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # 登录 QQ 邮箱
            smtp.send_message(msg)  # 发送邮件
        print(f"邮件发送成功，已发送至 {receiver}")
    except Exception as e:
        print(f"邮件发送失败，错误信息：{e}")


def get_card_type_11(params, headers):
    data = send_request(API_URL, params, headers)
    if data is None:
        return []
    cards = data.get("cards", [])
    card_type_11_info = []
    for card in cards:
        if card.get("card_type") == 11:
            card_group = card.get("card_group", [])
            for item in card_group:
                if item.get("card_type") == 8:
                    info = {
                        "scheme": item.get("scheme"),
                        "title_sub": item.get("title_sub")
                    }
                    card_type_11_info.append(info)
    return card_type_11_info


def sign_in(headers, base_params, scheme):
    params = extract_params(scheme)
    request_url = f"http://i.huati.weibo.com/mobile/super/active_fcheckin?cardid=bottom_one_checkin&container_id={params['containerid']}&pageid={params['containerid']}&scheme_type=1"
    sign_in_params = {
        "aid": base_params.get("aid"),
        "b": base_params.get("b"),
        "c": base_params.get("c"),
        "from": base_params.get("from"),
        "ft": base_params.get("ft"),
        "gsid": base_params.get("gsid"),
        "lang": base_params.get("lang"),
        "launchid": base_params.get("launchid"),
        "networktype": base_params.get("networktype"),
        "s": base_params.get("s"),
        "sflag": base_params.get("sflag"),
        "skin": base_params.get("skin"),
        "ua": base_params.get("ua"),
        "v_f": base_params.get("v_f"),
        "v_p": base_params.get("v_p"),
        "wm": base_params.get("wm"),
        "fid": "232478_-_one_checkin",
        "lfid": base_params.get("lfid"),
        "luicode": base_params.get("luicode"),
        "moduleID": base_params.get("moduleID"),
        "orifid": base_params.get("orifid"),
        "oriuicode": base_params.get("oriuicode"),
        "request_url": request_url,
        "source_code": base_params.get("source_code"),
        "sourcetype": "page",
        "uicode": base_params.get("uicode"),
        "ul_sid": base_params.get("ul_sid"),
        "ul_hid": base_params.get("ul_hid"),
        "ul_ctime": base_params.get("ul_ctime"),
    }
    data = send_request(SIGN_URL, sign_in_params, headers)
    return data

def read_streak():
    # 从 GitHub Actions 环境变量读取 streak
    STREAK_HISTORY = os.getenv('STREAK_HISTORY', 'None')
    if STREAK_HISTORY != 'None':
        if ',' in STREAK_HISTORY:
            last_date_str, streak_count = STREAK_HISTORY.split(',')
            last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
            return last_date, int(streak_count)
        else:
            # 如果 STREAK_HISTORY 格式不正确，抛出错误
            raise ValueError(f"Invalid STREAK_HISTORY format: {STREAK_HISTORY}")
    return None, 0  # 没有签到历史时返回默认值


def update_streak(today, streak_count):
    # 更新 GitHub Actions 环境变量
    with open(os.getenv('GITHUB_ENV'), 'a') as f:
        f.write(f"STREAK_HISTORY={today.strftime('%Y-%m-%d')},{streak_count}\n")


user_agents = [
    "Weibo/81434 (iPhone; iOS 16.0; Scale/3.00)",
    "Weibo/81435 (iPhone; iOS 17.0; Scale/2.00)",
    "Weibo/81436 (iPhone; iOS 17.1; Scale/3.00)"
]

headers = {"Accept": "*/*", "SNRT": "normal", "X-Sessionid": "8B83D45D-A5A4-4006-A9C2-1AB5452AB4FD",
           "Accept-Encoding": "gzip, deflate", "X-Validator": "nsYeah7o/zOlMt4Lhnz6YCNBJ4v1Kh1eT2Pr3Bh0tRo=",
           "Host": "api.weibo.cn", "x-engine-type": "cronet-98.0.4758.87", "Connection": "keep-alive",
           "Accept-Language": "en-US,en", "cronet_rid": "6524001", "Authorization": "", "X-Log-Uid": "7253083542",
           "User-Agent": random.choice(user_agents)}

if __name__ == "__main__":
    # weibo_my_cookie = ''
    params = extract_params(weibo_my_cookie)

    # 获取超话列表
    card_type_11_info = get_card_type_11(params, headers)

    # 读取签到历史
    last_sign_in_date, streak_count = read_streak()
    today = datetime.today().date()

    # 判断是否是连续签到
    if last_sign_in_date is not None:
        if (today - last_sign_in_date) == timedelta(days=1):
            streak_count += 1  # 连续签到
        elif (today - last_sign_in_date) > timedelta(days=1):
            streak_count = 1  # 中断，重新开始
    else:
        streak_count = 1  # 第一次签到

    # 打印获取的超话列表信息
    super_topic_list = "\n".join([f"    {info['title_sub']}" for info in card_type_11_info])
    print("超话列表：")
    print(super_topic_list)

    # 依次进行签到
    result_message = f"\n签到结果 (连续签到天数: {streak_count} 天)：\n"
    for info in card_type_11_info:
        result = sign_in(headers, params, info['scheme'])
        # 判断签到结果
        if result and result.get('msg') == '已签到':
            status = '成功'
        else:
            status = '失败'
        result_message += f"    {info['title_sub']}超话：{status}\n"
        time.sleep(random.randint(5, 10))  # 避免请求过于频繁

    # 更新签到历史
    update_streak(today, streak_count)

    # 所有签到完成后，发送邮件汇总结果
    qqemail("超话签到汇总结果", "760985953@qq.com", result_message)

    print(result_message)
