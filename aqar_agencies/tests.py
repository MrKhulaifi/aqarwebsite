from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Agency, AgencyMember, Area, Post, Comment
from django.core.exceptions import ValidationError

class AgencyTest(TestCase):

    def setUp(self):
        self.member = User.objects.create(username="alkhulaifi")

    def test_agency_creation(self):
        agency = Agency.objects.new(self.member, name="عقار بوحسين", phone_number="99025455")
        self.assertEqual(agency.phone_number, "99025455")
        self.assertIn(self.member,agency.members.all())
    
    def test_agency_creation_bad_phone_number(self):
        with self.assertRaises(ValidationError):
            Agency.objects.new(self.member, name="عقار بوحسين", phone_number="888")

    def test_agency_creation_bad_email(self):
        with self.assertRaises(ValidationError):
            Agency.objects.new(self.member, name="عقار بوحسين", email="888")

    def test_agency_creation_good_email(self):
        Agency.objects.new(self.member, name="عقار بوحسين", email="add@bdd.com")


class AgencyMemberTest(TestCase):
    def create_agencymember(self):
        member = User.objects.create()
        agency = Agency.objects.create()
        return AgencyMember.objects.create(member=member, agency=agency)

    def test_agencymember_creation(self):
        agencymember = self.create_agencymember()
        self.assertTrue(isinstance(agencymember, AgencyMember))


class AreaTest(TestCase):
    def create_area(self):
        return Area.objects.create()

    def test_area_creation(self):
        area = self.create_area()
        self.assertTrue(isinstance(area, Area))


class PostTest(TestCase):
    def create_post(self):
        agency = Agency.objects.create()
        area = Area.objects.create()
        return Post.objects.create(agency=agency, area=area)

    def test_post_creation(self):
        post = self.create_post()
        self.assertTrue(isinstance(post, Post))


class CommentTest(TestCase):
    def create_comment(self):
        user = User.objects.create()
        agency = Agency.objects.create()
        area = Area.objects.create()
        post = Post.objects.create(agency=agency, area=area)
        return Comment.objects.create(user=user, post=post)

    def test_comment_creation(self):
        comment = self.create_comment()
        self.assertTrue(isinstance(comment, Comment))


"""
class AgencyTestCase(TestCase):
    def create_user(self, name="Maktab"):
        return Agency.objects.create(name=name)

    def test_agency_creation(self):
        agency = Agency.objects.create(
            name="Maktab",
            phone_number="+96598821030",
            profile_picture=SimpleUploadedFile(
                name='test_image.jpg', content=b'', content_type='image/jpeg'),
            email="mr_agency@gmail.com",
            address="Qurtuba, block4, Street5, Ave1, House69",
            verification=True,
            twitter="agency_user_twitter",
            instagram="agency_user_instagram",
        )
        self.assertEqual(agency.name, "Maktab")
        self.assertEqual(agency.phone_number, "+96598821030")
        self.assertEqual(agency.email, "mr_agency@gmail.com")
        self.assertEqual(
            agency.address, "Qurtuba, block4, Street5, Ave1, House69")
        self.assertEqual(agency.verification, True)
        self.assertEqual(agency.twitter, "agency_user_twitter")
        # self.assertEqual(agency.instagram, "agency_user_instagram")


class AreaTestCase(TestCase):
    def test_new_area(self):
        area = Area.objects.create(name="Qurtuba")
        self.assertEqual(area.name, "Qurtuba")


class PostTestCase(TestCase):
    def test_new_post(self):
        agency = Agency.objects.create(name="Maktab")
        area = Area.objects.create()
        post = Post.objects.create(  # TODO ImageField not tested
            agency=agency,
            title="New Deal!",
            body="Check out the new deal our agency made recently!",
            picture=SimpleUploadedFile(
                name='test_image.jpg', content=b'', content_type='image/jpeg'),
            area=area
        )
        self.assertEqual(post.title, "New Deal!")
        self.assertEqual(
            post.body, "Check out the new deal our agency made recently!")


class CommentTestCase(TestCase):
    def test_new_comment(self):
        user = User.objects.create(username="alkhulaifi2", password="JustOpen4me!")
        agency = Agency.objects.create(name="Maktab")
        area = Area.objects.create()
        post = Post.objects.create(agency=agency, area=area)
        comment = Comment.objects.create(
            post=post,
            user=user,
            message="This is a great deal, good job!"
        )
        self.assertEqual(comment.message, "This is a great deal, good job!")

"""
