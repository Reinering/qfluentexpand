#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from enum import Enum


class ExtendableEnumMeta(type(Enum)):
    def __new__(metacls, cls, bases, classdict):
        # 创建枚举类
        enum_class = super().__new__(metacls, cls, bases, classdict)
        # 保存原始的_member_names_
        enum_class._original_member_names_ = enum_class._member_names_.copy()
        return enum_class


class ExtendableEnum(Enum, metaclass=ExtendableEnumMeta):

    @classmethod
    def extend(cls, name, value, **kwargs):
        # 验证名称是否已存在
        if name in cls.__members__:
            raise ValueError(f'{name} already exists in {cls.__name__}')

        # 创建新的枚举成员
        member = cls._value2member_map_.get(value)
        if member is None:
            # 如果值不存在，创建新成员
            member = object.__new__(cls)
            member._name_ = name
            member._value_ = value
            for key, value in kwargs.items():
                setattr(member, key, value)
                # member.theme = theme  # 设定主题
            cls._value2member_map_[value] = member
            cls._member_names_.append(name)
            setattr(cls, name, member)
        return member

