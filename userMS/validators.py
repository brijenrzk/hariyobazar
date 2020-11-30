# def validateRegForm(first_name, last_name, email, password, username):
#     err = None
#     print(first_name)
#     if(first_name is None):
#         err = "First name is missing"
#         print(err)
#     else:
#         err = None
#     return False
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError


def file_size(value):
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large.Size should not exceed 2mb.')
