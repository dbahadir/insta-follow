#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, database, datetime, time
from InstagramAPI import InstagramAPI
from database import db_session
from models import InstaUser
import config
import constant

def checkDailyCount(count) :
    if count :
        if count < config.FOLLOW_DAILY_COUNT :
            return count
    else :
        today =  time.strftime('%Y-%m-%d 00:00:00', time.localtime())
        dailyCount = InstaUser.query.filter(InstaUser.following_date >= today)
        if dailyCount.count() < config.FOLLOW_DAILY_COUNT :
            return dailyCount.count()
    print("Daily follow limit exceedeed")
    return -1

def follow(api) :
    daily = checkDailyCount(0)
    followUsers = InstaUser.query.filter_by(is_related=False, status=constant.USER_STATUS_NEW)
    if followUsers.count() and daily > -1:
        for followUser in followUsers :
            followUser.status = constant.USER_STATUS_PROCESSING
            db_session.commit()
            res = api.follow(followUser.insta_id)
            if res:
                followUser.following_status = constant.FOLLOWER_STATUS_YES
                followUser.following_date = datetime.datetime.now()
                print("User follow was succeed; {0}".format(followUser.user_name))
                daily += 1
                if checkDailyCount(daily) == -1 :
                    break;
            else :
                followUser.status = constant.USER_STATUS_NEW
                print("User follow was failed; {0}".format(followUser.user_name))
            db_session.commit()
            time.sleep(1)
    else :
        print("There is no new User for follow")

def unfollow(api) :
    now = time.time()
    before = now - config.UNFOLLOW_DELAY
    theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(before))
    unfollowUsers = InstaUser.query.filter_by(is_related=False, status=constant.USER_STATUS_PROCESSING).filter(InstaUser.following_date <= theTime)
    if unfollowUsers.count() :
        for unfollowUser in unfollowUsers :
            res = api.unfollow(unfollowUser.insta_id)
            if res:
                unfollowUser.status = constant.USER_STATUS_PROCESSED
                unfollowUser.following_status = constant.FOLLOWER_STATUS_OLD
                unfollowUser.unfollowing_date = datetime.datetime.now()
                print("User unfollow was succeed; {0}".format(unfollowUser.user_name))
                db_session.commit()
            else :
                print("User unfollow was failed; {0}".format(unfollowUser.user_name))
            time.sleep(1)
    else :
        print("There is no User for unfollow")

api = InstagramAPI(config.INSTA_USER, config.INSTA_PASS)
api.login()
follow(api)
unfollow(api)

sys.exit(0)
