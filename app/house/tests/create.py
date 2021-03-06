import datetime
import os
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from utils.image.file import upload_file_cmp
from utils.image.resize import clear_imagekit_test_files
from ..models import (
    House,
    Amenities,
    Facilities
)

__all__ = (
    'HouseCreateTest',
)

User = get_user_model()


class HouseCreateTest(APITestCase):
    URL = '/house/'

    def setUp(self):
        test_user_data = {
            'username': 'test@gmail.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'first_name': '수민',
            'last_name': '박',
            'phone_num': '010123456789',
        }
        self.user = User.objects.create_django_user(**test_user_data)
        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_check_user(self):
        self.assertEqual(self.user.username, 'test@gmail.com')

    def test_create_house(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key,
        )
        file_path = os.path.join(settings.STATIC_DIR, 'iu.jpg')
        img_cover = open(file_path, 'rb')

        house_image1_path = os.path.join(settings.STATIC_DIR, 'test', 'test_inner_image.jpg')
        house_image2_path = os.path.join(settings.STATIC_DIR, 'test', 'test_outer_image.jpg')

        house_image1 = open(house_image1_path, 'rb')
        house_image2 = open(house_image2_path, 'rb')
        print(img_cover)
        print(type(img_cover))
        print(type(house_image1))
        print(type(house_image2))

        amenities_list = ['TV', '에어컨', '전자렌지', '커피포트', '컴퓨터', '공기청정기']
        facilities_list = ['수영장', '엘리베이터', '세탁소', '노래방', '오락실', '온천']

        [Amenities.objects.create(name=name) for name in amenities_list]
        [Facilities.objects.create(name=name) for name in facilities_list]

        data = {
            'house_type': House.HOUSE_TYPE_HOUSING,
            'name': '우리집',
            'description': '테스트용 집입니다.',
            'room': 1,
            'bed': 2,
            'bathroom': 2,
            'personnel': 3,
            'amenities': [],
            'facilities': [1, 2, 3, 4, 5],
            'minimum_check_in_duration': 1,
            'maximum_check_in_duration': 3,
            'maximum_check_in_range': 90,
            'price_per_night': 100000,
            'country': '대한민국',
            'city': '사랑시',
            'district': '고백구',
            'dong': '행복동',
            'address1': '777-1',
            # 'address2': '희망빌라 2동 301호',
            'latitude': '12.12345670000000',
            'longitude': '123.12345670000000',
            'disable_days': [
                '2014-01-01',
                '2014-02-01',
                '2014-03-01',
                '2014-04-01',
            ],
            'img_cover': img_cover,
            'house_images': [
                house_image1,
                house_image2,
            ],
        }

        response = self.client.post(self.URL, data)
        img_cover.close()
        house_image1.close()
        house_image2.close()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['house_type'], data['house_type'])
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['room'], data['room'])
        self.assertEqual(response.data['bed'], data['bed'])
        self.assertEqual(response.data['bathroom'], data['bathroom'])
        self.assertEqual(response.data['personnel'], data['personnel'])
        self.assertEqual(response.data['amenities'], data['amenities'])
        self.assertEqual(response.data['facilities'], data['facilities'])
        self.assertEqual(response.data['minimum_check_in_duration'], data['minimum_check_in_duration'])
        self.assertEqual(response.data['maximum_check_in_duration'], data['maximum_check_in_duration'])
        self.assertEqual(response.data['maximum_check_in_range'], data['maximum_check_in_range'])
        self.assertEqual(response.data['price_per_night'], data['price_per_night'])
        self.assertEqual(response.data['created_date'], datetime.date.today().strftime('%Y-%m-%d'))
        self.assertEqual(response.data['modified_date'], datetime.date.today().strftime('%Y-%m-%d'))
        self.assertEqual(response.data['host']['pk'], self.user.pk)
        self.assertEqual(response.data['country'], data['country'])
        self.assertEqual(response.data['city'], data['city'])
        self.assertEqual(response.data['district'], data['district'])
        self.assertEqual(response.data['dong'], data['dong'])
        self.assertEqual(response.data['address1'], data['address1'])
        # self.assertEqual(response.data['address2'], data['address2'])
        self.assertEqual(response.data['latitude'], data['latitude'])
        self.assertEqual(response.data['longitude'], data['longitude'])

        self.assertIn('disable_days', response.data)

        for index, date in enumerate(response.data['disable_days']):
            self.assertEqual(date.strftime('%Y-%m-%d'), data['disable_days'][index])

        house = House.objects.get(pk=response.data['pk'])

        self.assertIn('house_images', response.data)

        self.assertEqual(house.house_type, data['house_type'])
        self.assertEqual(house.name, data['name'])
        self.assertEqual(house.description, data['description'])
        self.assertEqual(house.room, data['room'])
        self.assertEqual(house.bed, data['bed'])
        self.assertEqual(house.bathroom, data['bathroom'])
        self.assertEqual(house.personnel, data['personnel'])
        self.assertEqual(list(house.amenities.values_list('pk', flat=True)), data['amenities'])
        self.assertEqual(list(house.facilities.values_list('pk', flat=True)), data['facilities'])
        self.assertEqual(house.minimum_check_in_duration, data['minimum_check_in_duration'])
        self.assertEqual(house.maximum_check_in_duration, data['maximum_check_in_duration'])
        self.assertEqual(house.maximum_check_in_range, data['maximum_check_in_range'])
        self.assertEqual(house.price_per_night, data['price_per_night'])
        self.assertEqual(house.created_date, datetime.date.today())
        self.assertEqual(house.modified_date, datetime.date.today())
        self.assertEqual(house.host.pk, self.user.pk)
        self.assertEqual(house.host.is_host, True)
        self.assertEqual(house.country, data['country'])
        self.assertEqual(house.city, data['city'])
        self.assertEqual(house.district, data['district'])
        self.assertEqual(house.dong, data['dong'])
        self.assertEqual(house.address1, data['address1'])
        # self.assertEqual(house.address2, data['address2'])
        self.assertEqual(house.latitude, Decimal(data['latitude']))
        self.assertEqual(house.longitude, Decimal(data['longitude']))

        self.assertEqual(house.disable_days.count(), len(data['disable_days']))
        disable_day_list = list(house.disable_days.values_list('date', flat=True))
        for index, date in enumerate(disable_day_list):
            self.assertEqual(date.strftime('%Y-%m-%d'), data['disable_days'][index])

        self.assertTrue(upload_file_cmp(file_path=file_path, img_name=house.img_cover.name))
        self.assertTrue(upload_file_cmp(file_path=house_image1_path, img_name=house.images.first().image.name))
        self.assertTrue(upload_file_cmp(file_path=house_image2_path, img_name=house.images.last().image.name))

        clear_imagekit_test_files()
