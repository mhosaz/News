from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import News, Tag

class RealNewsApiTests(APITestCase):
    def setUp(self):
        # Create Tags
        tag_world = Tag.objects.create(name='world')
        tag_technology = Tag.objects.create(name='technology')
        tag_sports = Tag.objects.create(name='sports')
        self.url = reverse('api:news-list')  # Changed 'Api' to 'api' (lowercase)
        # Create Realistic News
        self.news1 = News.objects.create(
            title='NASA Discovers New Exoplanet',
            content='NASA has discovered a new Earth-like planet in the habitable zone of a distant star.',
            source='https://www.nasa.gov/news/exoplanet-discovery'
        )
        self.news1.tags.add(tag_technology)

        self.news2 = News.objects.create(
            title='Olympics 2024 to Be Held in Paris',
            content='The 2024 Olympic Games are scheduled to be held in Paris with new sports added.',
            source='https://www.olympics.com/en/news/paris-2024-games-overview'
        )
        self.news2.tags.add(tag_sports)

        self.news3 = News.objects.create(
            title='UN Calls for Global Climate Action',
            content='The UN has urged all nations to commit to stricter climate policies by 2030.',
            source='https://www.un.org/en/climate-change/news/global-call-to-action'
        )
        self.news3.tags.add(tag_world)

    def test_get_all_news(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        news_list = response.json()
        self.assertEqual(len(news_list), 3)
        return response

    def test_filter_by_tag_world(self):
        response = self.client.get(self.url, {'tag': 'world'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        news = response.json()
        self.assertEqual(len(news), 1)
        self.assertEqual(news[0]['title'], 'UN Calls for Global Climate Action')
        return response

    def test_filter_include_keyword_climate(self):
        response = self.client.get(self.url, {'include': 'climate'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        news = response.json()
        self.assertEqual(len(news), 1)
        self.assertIn('climate', news[0]['content'].lower())
        return response

    def test_filter_exclude_keyword_olympic(self):
        response = self.client.get(self.url, {'exclude': 'Olympic'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        news = response.json()
        self.assertEqual(len(news), 2)
        for item in news:
            self.assertNotIn('Olympic', item['title'])
        return response

    def test_include_and_exclude_keywords(self):
        response = self.client.get(self.url, {'include': 'planet', 'exclude': 'climate'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        news = response.json()
        self.assertEqual(len(news), 1)
        self.assertIn('planet', news[0]['content'].lower())
        return response

    def test_multiple_include_keywords(self):
        response = self.client.get(self.url, {'include': 'Olympic,UN'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        news = response.json()
        self.assertEqual(len(news), 2)
        return response

    def test_multiple_exclude_keywords(self):
        response = self.client.get(self.url, {'exclude': ['planet', 'Olympic']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        news = response.json()
        self.assertEqual(len(news), 1)
        self.assertEqual(news[0]['title'], 'UN Calls for Global Climate Action')
        return response

    def test_filter_by_nonexistent_tag(self):
        response = self.client.get(self.url, {'tag': 'health'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)
        return response

    def test_response_structure(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for news in response.json():
            self.assertIn('id', news)
            self.assertIn('title', news)
            self.assertIn('content', news)
            self.assertIn('source', news)
            self.assertIn('tags', news)
        return response