from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase, TestCase
from django.urls import reverse_lazy
from selenium.webdriver.chrome.webdriver import WebDriver

from ..models import Diary


class LoggedInTestCase(TestCase):
    """Original TestCase class which overrides common preprocessing method in each test class"""

    def setUp(self):
        """Preconfiguration of test method"""

        self.password = "large054"

        self.test_user = get_user_model().objects.create_user(
            username="largefieldmasa",
            email="largefieldmasa@gmail.com",
            password=self.password,
        )

        self.client.login(email=self.test_user.email, password=self.password)


class TestDiaryCreateView(LoggedInTestCase):
    """Test class for DiaryCreateView"""

    def test_create_diary_success(self):
        """日記作成処理が成功することを検証する"""

        params = {
            "title": "テストタイトル",
            "content": "本文",
            "photo1": "",
            "photo2": "",
            "photo3": "",
        }

        response = self.client.post(reverse_lazy("diary:diary_create"), params)

        # 日記一覧ページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy("diary:diary_list"))

        # 日記データがデータベースに登録されたかを検証
        self.assertEqual(Diary.objects.filter(title="テストタイトル").count(), 1)

    def test_create_diary_failure(self):
        """新規日記作成処理が失敗することを検証する"""

        response = self.client.post(reverse_lazy("diary:diary_create"))

        # 必須フォームフィールドが未入力によりエラーになることを検証
        self.assertFormError(response, "form", "title", "このフィールドは必須です。")


class TestDiaryUpdateView(LoggedInTestCase):
    """Test class for DiaryUpdateView"""

    def test_update_diary_success(self):
        """日記編集処理が成功することを検証する"""

        diary = Diary.objects.create(user=self.test_user, title="タイトル編集前")

        params = {"title": "タイトル編集後"}

        response = self.client.post(
            reverse_lazy("diary:diary_update", kwargs={"pk": diary.pk}), params
        )

        # 日記詳細ページへのリダイレクトを検証
        self.assertRedirects(
            response, reverse_lazy("diary:diary_detail", kwargs={"pk": diary.pk})
        )

        # 日記データが編集されたかを検証
        self.assertEqual(Diary.objects.get(pk=diary.pk).title, "タイトル編集後")

    def test_update_diary_failure(self):
        """日記編集処理が失敗することを検証する"""

        response = self.client.post(
            reverse_lazy("diary:diary_update", kwargs={"pk": 999})
        )

        self.assertEqual(response.status_code, 404)


class TestDiaryDeleteView(LoggedInTestCase):
    """Test class for DiaryDeleteView"""

    def test_delete_diary_success(self):
        """日記削除処理が成功することを検証する"""

        diary = Diary.objects.create(user=self.test_user, title="タイトル")

        response = self.client.post(
            reverse_lazy("diary:diary_delete", kwargs={"pk": diary.pk})
        )

        # 日記一覧ページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy("diary:diary_list"))

        # 日記データが削除されたかを検証
        self.assertEqual(Diary.objects.filter(pk=diary.pk).count(), 0)

    def test_delete_diary_failure(self):
        """日記削除処理が失敗することを検証する"""

        response = self.client.post(
            reverse_lazy("diary:diary_delete", kwargs={"pk": 999})
        )

        # 存在しない日記データを削除しようとしてエラーになることを検証
        self.assertEqual(response.status_code, 404)


class TestLogin(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(executable_path="/Users/hironomasayuki/chromedriver")

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get("http://localhost:8000" + str(reverse_lazy("account_login")))

        username_input = self.selenium.find_element_by_name("login")
        username_input.send_keys("largefieldmasa@gmail.com")
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys("large054")
        self.selenium.find_element_by_class_name("btn").click()

        # ページタイトルの検証
        self.assertEquals("日記一覧 | Private Diary", self.selenium.title)
