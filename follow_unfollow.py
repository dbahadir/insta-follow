#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, database, datetime, time
from InstagramAPI import InstagramAPI
from database import db_session
from models import InstaUser
import config
import constant

def login():
    api = InstagramAPI(config.INSTA_USER, config.INSTA_PASS)
    api.login()
    return api

def checkDailyCount(count) :
    if count :
        if count < config.FOLLOW_DAILY_COUNT :
            return count
    else :
        today =  time.strftime('%Y-%m-%d 00:00:00', time.localtime())
        dailyCount = InstaUser.query.filter_by(status=constant.USER_STATUS_PROCESSING).filter(InstaUser.following_date >= today)
        if dailyCount.count() < config.FOLLOW_DAILY_COUNT :
            return dailyCount.count()
    print("Daily follow limit exceedeed")
    return -1

def follow() :
    api = login()
    daily = checkDailyCount(0)
    followUsers = InstaUser.query.filter_by(is_related=False, status=constant.USER_STATUS_NEW)
    if followUsers.count() and daily > -1:
        i = 1
        for followUser in followUsers :
            followUser.status = constant.USER_STATUS_PROCESSING
            db_session.commit()
            res = api.follow(followUser.insta_id)
            if res:
                followUser.following_status = constant.FOLLOWER_STATUS_YES
                followUser.following_date = datetime.datetime.now()
                db_session.commit()
                print("User follow was succeed; {0}".format(followUser.user_name))
                i = 1
                daily += 1
                if checkDailyCount(daily) == -1 :
                    break;
            else :
                followUser.status = constant.USER_STATUS_NEW
                db_session.commit()
                print("User follow was failed; {0}".format(followUser.user_name))
                if i > 10 :
                    print ("Follow action is failed 10 times, so exit the action.");
                    break;
                else :
                    sec = 60 * i
                    print("sleeping {0} seconds...".format(sec));
                    time.sleep(sec)
                    api = login()
                    i += 1
            time.sleep(1)
    else :
        print("There is no new User for follow")

def unfollow() :
    api = login()
    now = time.time()
    before = now - config.UNFOLLOW_DELAY
    theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(before))
    unfollowUsers = InstaUser.query.filter_by(is_related=False, status=constant.USER_STATUS_PROCESSING).filter(InstaUser.following_date <= theTime)
    if unfollowUsers.count() :
        i = 1
        for unfollowUser in unfollowUsers :
            res = api.unfollow(unfollowUser.insta_id)
            if res:
                unfollowUser.status = constant.USER_STATUS_PROCESSED
                unfollowUser.following_status = constant.FOLLOWER_STATUS_OLD
                unfollowUser.unfollowing_date = datetime.datetime.now()
                db_session.commit()
                print("User unfollow was succeed; {0}".format(unfollowUser.user_name))
                i = 1
            else :
                print("User unfollow was failed; {0}".format(unfollowUser.user_name))
                if i > 10 :
                    print ("Unfollow action is failed 10 times, so exit the action.");
                    break;
                else :
                    sec = 60 * i
                    print("sleeping {0} seconds...".format(sec));
                    time.sleep(sec)
                    api = login()
                    i += 1
            time.sleep(1)
    else :
        print("There is no User for unfollow")

follow(api)
unfollow(api)

sys.exit(0)
