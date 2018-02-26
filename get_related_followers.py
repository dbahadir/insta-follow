#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, database, datetime
from InstagramAPI import InstagramAPI
from database import db_session
from models import InstaUser
import config
import constant

def findUserData(api, relatedUser) :
    api.searchUsername(relatedUser.user_name)
    userInfo = api.LastJson
    if userInfo['status'] == 'ok' :
        instaId = userInfo['user']['pk']
        fullName = userInfo['user']['full_name']
        isPrivate = userInfo['user']['is_private']
        relatedUser.insta_id = instaId
        relatedUser.full_name = fullName
        relatedUser.is_private = isPrivate
        if isPrivate :
            relatedUser.status = constant.USER_STATUS_FAILED
            print("User profile is private!. We dont get followers.")
        else :
            relatedUser.status = constant.USER_STATUS_NEW
        db_session.commit()
        print("api.searchUsername() related user data updated.")
    else :
        print("api.searchUsername() status is not OK. Status is %s" % userInfo['status'])
        relatedUser.status = constant.USER_STATUS_FAILED
        db_session.commit()

def updateFollower(user, relatedUserId) :
    instaId = user['pk']
    userName = user['username']
    fullName = user['full_name']
    isPrivate = user['is_private']
    print ("USER: {0}".format(user))
    dbUser = InstaUser.query.filter_by(insta_id=instaId).first()
    if dbUser :
        print("User already processed, skip it.")
        return False
    else :
        dbUser = InstaUser()
        dbUser.insta_id = instaId
        dbUser.status = constant.USER_STATUS_NEW
        dbUser.user_id = relatedUserId
        dbUser.user_name = userName
        dbUser.full_name = fullName
        dbUser.is_private = isPrivate
        db_session.add(dbUser)
        db_session.commit()
    return True

def updateFollowers(api, relatedUser) :
    next_max_id = ''
    while 1:
        api.getUserFollowers(relatedUser.insta_id, next_max_id)
        res = api.LastJson
        for user in res["users"]:
            updateFollower(user, relatedUser.id)
        if res["big_list"] is False :
            break
        next_max_id = res["next_max_id"]

def getFollowers(api) :
    relatedUser = InstaUser.query.filter_by(is_related=True, status=constant.USER_STATUS_NEW).first()
    if relatedUser :
        relatedUser.status = constant.USER_STATUS_PROCESSING
        db_session.commit()
        if relatedUser.insta_id == 0 :
            findUserData(api, relatedUser)
            getFollowers(api)
        else :
            updateFollowers(api, relatedUser)
            relatedUser.status = constant.USER_STATUS_PROCESSED
            db_session.commit()
    else :
        print("There is no new related User!")

api = InstagramAPI(config.INSTA_USER, config.INSTA_PASS)
api.login()
getFollowers(api)

sys.exit(0)
