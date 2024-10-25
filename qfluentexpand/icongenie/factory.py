#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from enum import Enum
from typing import Dict, Any


class EnumFactory:
    @staticmethod
    def create_enum(name: str, initial_members: Dict[str, Any] = None):
        if initial_members is None:
            initial_members = {}

        # 创建新的枚举类
        return Enum(name, initial_members)

    @staticmethod
    def extend_enum(enum_class: type, name: str, value: Any):
        # 创建包含现有成员和新成员的字典
        members = {member.name: member.value for member in enum_class}
        members[name] = value

        # 创建新的枚举类
        new_enum = Enum(enum_class.__name__, members)

        # 复制原枚举类的特殊属性
        for attr in dir(enum_class):
            if not attr.startswith('_') and attr not in members:
                setattr(new_enum, attr, getattr(enum_class, attr))

        return new_enum

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