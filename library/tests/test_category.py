from email.quoprimime import body_check
from random import randrange
from rest_framework import status
from rest_framework.test import APIClient
from library.models import *
import pytest

def rand_username():
    tmp = [ascii(ord('a')+i) for i in range(26)]
    username = "".join([tmp[randrange(0, 26)] for i in range(8)])
    return username

librarian_body = {
        "password": "1234567890",
        "confirm_password": "1234567890",
        "first_name": "Henish",
        "last_name": "Patel",
        "email": "ompatle@gml.com",
        "sign_up_as": "Librarian",
        "phone_number": "7990577979",
        "address": "Vadnagar",
        "pin_code": "384355"
}

member_body = {
    **librarian_body,
    "aadhaar_card_id": "91596453245",
    "date_of_birth": "2002-09-05",
    "sign_up_as": "Member",
}


@pytest.mark.django_db
class TestCategory:
    body = {
        'name': "Tech",
        'description': "About Technology",
        'stack_location': 'A10',
    }
    
    
    def test_category_without_access_token_returns_401(self):
        client = APIClient()
        res = client.post("/category/", self.body)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_category_create_by_member_return_401(self):
        client = APIClient()
        member = {
            'username': rand_username(),
            **member_body
        }
        res1 = client.post("/auth/register/", member)
        auth = {
            'username': member.get("username"),
            "password": member.get("password")
        }
        jwt = client.post("/auth/login", auth)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + jwt.data.get("access"))
        res = client.post("/category/", self.body)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
        res = client.post("/book/", {})
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
        
    
@pytest.mark.django_db    
class TestBook:
    def create_category(self, by_librarien):
        body = {
            'title': "Python",
            'isbn': "1234567890",
            "published_year": 2018,
            "author": "Henish Patel",
            "bar_code": "1234567890",
        }
        client = APIClient()
        if by_librarien:
            member = {
                'username': rand_username(),
                **librarian_body
            }
        else:
            member = {
                'username': rand_username(),
                **member_body
            }
        res1 = client.post("/auth/register/", member)
        auth = {
            'username': member.get("username"),
            "password": member.get("password")
        }
        
        jwt = client.post("/auth/login", auth)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + jwt.data.get("access"))
                
        res = client.post("/category/", {
            'name': "Tech",
            'description': "About Technology",
            'stack_location': 'A10',
        })
        body['category'] = res.data["id"]
        
        return (body, jwt.data.get("access"))
    
    def test_create_book_by_librarien(self):
        client = APIClient()
        body = self.create_category(by_librarien=True)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + body[1])
        res = client.post("/book/", body[0])
        assert res.status_code == status.HTTP_201_CREATED
    
    def test_create_book_by_member(self):
        client = APIClient()
        body = self.create_category(by_librarien=True)[0]
        
        res = client.post("/book/", body)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_delete_book_by_librarien(self):
        client = APIClient()
        body = self.create_category(by_librarien=True)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + body[1])
        res = client.post("/book/", body[0])
        assert res.status_code == status.HTTP_201_CREATED
        res = client.delete(f"/book/{res.data['id']}/")
        
        assert res.status_code == status.HTTP_204_NO_CONTENT
        