from django.test import TestCase

class ViewTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()
    
    def test_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
    
    