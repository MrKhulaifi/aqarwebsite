from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Agency, AgencyMember, Area, Post, Comment


class AgencyTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            username="alkhulaifi",
            password="JustOpen4me!"
        )
        Agency.objects.create(  # TODO ImageField property not tested
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
        AgencyMember.objects.create(
            agency=User.objects.get(username="alkhulaifi"),
            member=Agency.objects.get(name="Maktab"),
            is_admin=False
        )
        Area.objects.create(
            name="Qurtuba"
        )
        Post.objects.create(  # TODO ImageField not tested
            agency=Agency.objects.get(name="Maktab"),
            title="New Deal!",
            body="Check out the new deal our agency made recently!",
            picture=SimpleUploadedFile(
                name='test_image.jpg', content=b'', content_type='image/jpeg'),
            area=Area.objects.get(name="Qurtuba")
        )
        Comment.objects.create(
            post=Post.objects.get(title="New Deal!"),
            user=User.objects.get(username="alkhulaifi"),
            message="This is a great deal, good job!"
        )

    def test_new_user(self):
        user = User.objects.get(username="alkhulaifi")
        self.assertEqual(user.username, "alkhulaifi")
        self.assertEqual(user.password, "JustOpen4me!")

    def test_new_agency(self):
        agency = Agency.objects.get(name="Maktab")
        self.assertEqual(agency.name, "Maktab")
        self.assertEqual(agency.phone_number, "+96598821030")
        self.assertEqual(agency.email, "mr_agency@gmail.com")
        self.assertEqual(
            agency.address, "Qurtuba, block4, Street5, Ave1, House69")
        self.assertEqual(agency.verification, True)
        self.assertEqual(agency.twitter, "agency_user_twitter")
        self.assertEqual(agency.instagram, "agency_user_instagram")

        self.assertEqual(agency.member, AgencyMember.objects.get(
            username="alkhulaifi", member="Maktab"))

    def test_new_agencymember(self):
        agencymember = AgencyMember.objects.get(
            username="alkhulaifi", member="Maktab")
        self.assertEqual(agencymember.username, "alkhulaifi")
        self.assertEqual(agencymember.member, "Maktab")
        self.assertEqual(agencymember.is_admin, False)

    def test_new_area(self):
        area = Area.objects.get(name="Qurtuba")
        self.assertEqual(area.name, "Qurtuba")

    def test_new_post(self):
        post = Post.objects.get(title="New Deal!")
        self.assertEqual(post.title, "New Deal!")
        self.assertEqual(
            post.body, "Check out the new deal our agency made recently!")

    def test_new_comment(self):
        comment = Comment.objects.get(
            message="This is a great deal, good job!")
        self.assertEqual(comment.message, "This is a great deal, good job!")
