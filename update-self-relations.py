#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, database, datetime
from InstagramAPI import InstagramAPI
from database import db_session
from models import InstaUser
import config
import constant

def updateSelfData(api) :
    api.getSelfUsernameInfo()
    selfInfo = api.LastJson

    if selfInfo['status'] == 'ok' :
        instaId = selfInfo['user']['pk']
        userName = selfInfo['user']['username']
        fullName = selfInfo['user']['full_name']
        isPrivate = selfInfo['user']['is_private']
        isNew = False
        selfUser = InstaUser.query.get(1)
        if not selfUser :
            selfUser = InstaUser()
            isNew = True
        selfUser.insta_id = instaId
        selfUser.user_name = userName
        selfUser.full_name = fullName
        selfUser.is_private = isPrivate
        selfUser.status = constant.USER_STATUS_PROCESSED
        if isNew :
            db_session.add(selfUser)
        db_session.commit()
        print("api.getSelfUsernameInfo() self data updated.")
    else :
        print("api.getSelfUsernameInfo() status is not OK. Status is %s" % selfInfo['status'])
        sys.exit(1)
    return instaId

def updateFollower(user) :
    instaId = user['pk']
    userName = user['username']
    fullName = user['full_name']
    isPrivate = user['is_private']
    isNew = False
    print ("USER: %s" % user)
    dbUser = InstaUser.query.filter_by(insta_id=instaId).first()
    if dbUser :
        if dbUser.status != constant.USER_STATUS_PROCESSED :
            return False
        dbUser.follower_status = constant.FOLLOWER_STATUS_YES
    else :
        isNew = True
        dbUser = InstaUser()
        dbUser.insta_id = instaId
        dbUser.status = constant.USER_STATUS_PROCESSED
        dbUser.follower_status = constant.FOLLOWER_STATUS_NEW
        dbUser.follower_date = datetime.datetime.now()
    dbUser.user_id = 1
    dbUser.user_name = userName
    dbUser.full_name = fullName
    dbUser.is_private = isPrivate
    if isNew :
        db_session.add(dbUser)
    db_session.commit()
    return True

def updateFollowers(api, instaId) :
    next_max_id = ''
    while 1:
        api.getUserFollowers(instaId, next_max_id)
        res = api.LastJson
        for user in res["users"]:
            updateFollower(user)
        if res["big_list"] is False :
            break
        next_max_id = res["next_max_id"]

def updateFollowing(user) :
    instaId = user['pk']
    userName = user['username']
    fullName = user['full_name']
    isPrivate = user['is_private']
    isNew = False
    print ("USER: %s" % user)
    dbUser = InstaUser.query.filter_by(insta_id=instaId).first()
    if dbUser :
        dbUser.following_status = constant.FOLLOWING_STATUS_YES
    else :
        isNew = True
        dbUser = InstaUser()
        dbUser.insta_id = instaId
        dbUser.user_id = 1
        dbUser.status = constant.USER_STATUS_PROCESSED
        dbUser.following_status = constant.FOLLOWING_STATUS_NEW
        dbUser.following_date = datetime.datetime.now()
    dbUser.user_name = userName
    dbUser.full_name = fullName
    dbUser.is_private = isPrivate
    if isNew :
        db_session.add(dbUser)
    db_session.commit()
    return True

def updateFollowings(api, instaId) :
    next_max_id = ''
    while 1:
        api.getUserFollowings(instaId, next_max_id)
        res = api.LastJson
        for user in res["users"]:
            updateFollowing(user)
        if res["big_list"] is False :
            break
        next_max_id = res["next_max_id"]


api = InstagramAPI(config.INSTA_USER, config.INSTA_PASS)
api.login()

instaId = updateSelfData(api)
updateFollowers(api, instaId)
updateFollowings(api, instaId)

sys.exit(0)
