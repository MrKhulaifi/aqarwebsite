import os
from django.test import TestCase
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Agency, AgencyMember, Area, Post, Comment
from .forms import AgencyCreateForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from io import BytesIO


class AgencyModelTests(TestCase):

    def setUp(self):
        self.member = User.objects.create(username="alkhulaifi")

    def test_agency_creation(self):
        """The agency entry can be created, and the user is a member in it"""
        agency = Agency.objects.new(self.member, name="عقار بوحسين")
        self.assertIn(self.member, agency.members.all())

    def test_agency_creation_no_name(self):
        """If the agency is created with no name an error is raised"""
        with self.assertRaises(ValidationError):
            Agency.objects.new(self.member)

    def test_agency_creation_name_too_short(self):
        """If the agency is created with a name shorter than 10 chars an error is raised"""
        with self.assertRaises(ValidationError):
            Agency.objects.new(self.member, name="dds")

    def test_agency_creation_name_too_long(self):
        """If the agency is created with a name longer than 100 chars an error is raised"""
        with self.assertRaises(ValidationError):
            Agency.objects.new(self.member, name="""قار بوحسينقار بوحسينقار بوحسينقار بوحسين
            قار بوحسينقار بوحسينقار بوحسينقار بوحسينقار بوحسينقار بوحسين""")

    def test_agency_creation_bad_phone_number(self):
        """If the phone number is not 8 digits an error is raised"""
        with self.assertRaises(ValidationError):
            Agency.objects.new(
                self.member, name="عقار بوحسين", phone_number="888")

    def test_agency_creation_good_phone_number(self):
        """An agency is created if the phone number is 8 digits"""
        Agency.objects.new(self.member, name="عقار بوحسين",
                           phone_number="23455432")

    def test_agency_good_profile_picture(self):
        """An agency creation with a photo that has a proper file extension will pass"""
        Agency.objects.new(
            self.member,
            name="عقار بوحسين",
            profile_picture=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
            )
        mydir = "uploads/profile_picture"
        for photo in os.listdir(mydir):
            os.remove(os.path.join(mydir, photo)) # Delete all generated photos

    def test_agency_bad_profile_picture(self):
        """An agency creation with a photo that has the wrong file extension will raise an error"""
        with self.assertRaises(ValidationError):
            Agency.objects.new(
                self.member,
                name="عقار بوحسين",
                profile_picture=SimpleUploadedFile(name="test.txt", content=b"test", content_type='text/txt')
                )

    def test_agency_creation_bad_email(self):
        with self.assertRaises(ValidationError):
            Agency.objects.new(self.member, name="عقار بوحسين", email="888")

    def test_agency_creation_good_email(self):
        Agency.objects.new(self.member, name="عقار بوحسين",
                           email="add@bdd.com")

    def test_agency_creation_address_too_short(self):
        with self.assertRaises(ValidationError):
            Agency.objects.new(self.member, name="عقار بوحسين",
                               address="Qurtuba, block4")

    def test_agency_creation_address_too_long(self):
        with self.assertRaises(ValidationError):
            Agency.objects.new(self.member, name="عقار بوحسين", address="""Qurtuba, block4
            Qurtuba, block4Qurtuba, block4Qurtuba, block4Qurtuba, block4Qurtuba, block4
            Qurtuba, block4Qurtuba, block4Qurtuba, block4Qurtuba, block4Qurtuba, block4
            Qurtuba, block4Qurtuba, block4Qurtuba, block4Qurtuba, block4Qurtuba, block4""")

    def test_agency_creation_address_name(self):
        Agency.objects.new(self.member, name="عقار بوحسين",
                           address="Qurtuba, block4, Street5, Ave1, House69")

    def test_agency_verifying_user(self):
        agency = Agency.objects.new(self.member, name="عقار بوحسين")
        agency.verified_by(self.member)
        self.assertEqual(agency.verification, self.member)

    def test_agency_wrong_verifying_user(self):
        wrong_user = User.objects.create(username="notalkhulaifi")
        agency = Agency.objects.new(self.member, name="عقار بوحسين")
        agency.verified_by(self.member)
        self.assertNotEqual(agency.verification, wrong_user)

    def test_agency_verified_by_two_users(self):
        second_user = User.objects.create(username="alkhulaifi2")
        agency = Agency.objects.new(self.member, name="عقار بوحسين")
        agency.verified_by(self.member)
        with self.assertRaises(ValidationError):
            agency.verified_by(second_user)

    def test_agency_unverifying_user(self):
        agency = Agency.objects.new(self.member, name="عقار بوحسين")
        agency.verified_by(self.member)
        agency.unverify()
        self.assertNotEqual(agency.verification, self.member)
        self.assertIsNone(agency.verification)

    def test_agency_with_multiple_members(self):
        agency = Agency.objects.new(self.member, name="عقار بوحسين")
        member2 = User.objects.create(username="guy2")
        agency.add_member(member2, is_admin=False)
        member3 = User.objects.create(username="guy3")
        agency.add_member(member3, is_admin=False)
        self.assertEqual(agency.members.all()[0], self.member)
        self.assertEqual(agency.members.all()[1], member2)
        self.assertEqual(agency.members.all()[2], member3)
        self.assertEqual(len(agency.members.all()), 3)


class AgencyMemberModelTests(TestCase):

    def setUp(self):
        self.member = User.objects.create()
        self.agency = Agency.objects.new(self.member, name="Test Agency")

    def test_agencymember_creation(self):
        agencymember = AgencyMember.objects.create(
            member=self.member, agency=self.agency)
        self.assertTrue(isinstance(agencymember, AgencyMember))

    def test_agencymember_default_is_admin(self):
        agencymember = AgencyMember.objects.create(
            member=self.member, agency=self.agency)
        self.assertTrue(agencymember.is_admin)

    def test_agencymember_is_admin_False(self):
        agencymember = AgencyMember.objects.create(
            member=self.member, agency=self.agency, is_admin=False)
        self.assertFalse(agencymember.is_admin)


class AreaModelTests(TestCase):
    def test_create_area(self):
        Area.objects.new(name="Qortuba")

    def test_create_area_no_name(self):
        with self.assertRaises(ValidationError):
            Area.objects.new()

    def test_create_area_short_name(self):
        with self.assertRaises(ValidationError):
            Area.objects.new(name="Q")

    def test_create_area_long_name(self):
        with self.assertRaises(ValidationError):
            Area.objects.new(name="longlonglonglonglonglonglonglonglonglonglonglonglonglong")

    def test_create_area_name_already_exists(self):
        Area.objects.new(name="Qortuba")
        with self.assertRaises(ValidationError):
            Area.objects.new(name="Qortuba")


class PostModelTests(TestCase):

    def setUp(self):
        self.member = User.objects.create(username="alkhulaifi")
        self.agency = Agency.objects.new(self.member, name="Test Agency")
        self.area = Area.objects.new(name="Qortuba")

    def test_create_post(self):
        Post.objects.new(agency=self.agency, area=self.area, title="Best Sale", body="This Sale is Great")

    def test_create_post_no_title(self):
        with self.assertRaises(ValidationError):
            Post.objects.new(agency=self.agency, area=self.area, body="This Sale is Great")

    def test_create_post_title_too_long(self):
        with self.assertRaises(ValidationError):
            Post.objects.new(agency=self.agency, area=self.area, title="Best SaleBest SaleBest SaleBest SaleBest SaleBest SaleBest SaleBest SaleBest SaleBest SaleBest SaleBest Sale", body="This Sale is Great")

    def test_create_post_body_too_long(self):
        with self.assertRaises(ValidationError):
            Post.objects.new(agency=self.agency, area=self.area, title="Best Sale",
            body="""Best SaleBest SaleBBest SaleBest SaleBBest SaleBest SaleBBest SaleBest SaleB
            Best SaleBest SaleBBest SaleBest SaleBBest SaleBest SaleBBest SaleBest SaleB
            Best SaleBest SaleBBest SaleBest SaleBBest SaleBest SaleBBest SaleBest SaleB
            Best SaleBest SaleBBest SaleBest SaleBBest SaleBest SaleBBest SaleBest SaleB
            Best SaleBest SaleBBest SaleBest SaleBBest SaleBest SaleBBest SaleBest SaleB""")

    def test_post_good_post_picture(self):
        Post.objects.new(agency=self.agency, area=self.area, title="Best Sale", body="This Sale is Great", 
            picture=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'))
        mydir = "uploads/posts"
        for photo in os.listdir(mydir):
            os.remove(os.path.join(mydir, photo)) # Delete all generated photos

    def test_post_bad_post_picture(self):
        with self.assertRaises(ValidationError):
            Post.objects.new(agency=self.agency, area=self.area, title="Best Sale", body="This Sale is Great", 
                picture=SimpleUploadedFile(name="test.txt", content=b"test", content_type='text/txt'))
        mydir = "uploads/posts"
        for photo in os.listdir(mydir):
            os.remove(os.path.join(mydir, photo)) # Delete all generated photos


class CommentModelTests(TestCase):

    def setUp(self):
        self.member = User.objects.create(username="alkhulaifi")
        self.agency = Agency.objects.new(self.member, name="Test Agency")
        self.area = Area.objects.new(name="Qortuba")
        self.post = Post.objects.new(agency=self.agency, area=self.area, title="Amazing Sale", body="Look at this sale")

    def test_create_new_comment(self):
        Comment.objects.new(post=self.post, user=self.member, message="Nice Sale, good job")

    def test_create_new_comment_no_message(self):
        with self.assertRaises(ValidationError):
            Comment.objects.new(post=self.post, user=self.member)

    def test_create_new_comment_message_too_long(self):
        with self.assertRaises(ValidationError):
            Comment.objects.new(post=self.post, user=self.member, message="""
            Best SaleBest SaleBBest SaleBest SaleBBest SaleBest SaleBBest SaleBest SaleB
            Best SaleBest SaleBBest SaleBest SaleBBest SaleBest SaleBBest SaleBest SaleB
            Best SaleBest SaleBBest SaleBest SaleBBest SaleBest SaleBBest SaleBest SaleB
            Best SaleBest SaleBBest SaleBest SaleBBest SaleBest SaleBBest SaleBest SaleB
            Best SaleBest SaleBBest SaleBest SaleBBest SaleBest SaleBBest SaleBest SaleB""")

# --------------------------------------------------------------------------------------

class IndexViewTests(TestCase):
    
    def test_response(self):
        get_response = self.client.get(reverse("index"))
        self.assertContains(get_response, "This is the index page!", status_code=200)
    
    def test_response(self):
        get_response = self.client.get(reverse("index"))
        self.assertContains(get_response, "This is the index page!", status_code=200)
        self.assertContains(get_response, "You are not logged in.", status_code=200)
    
    def test_response_if_logged_in(self):
        self.client.post(reverse("register"), {
            "username": "alkhulaifi",
            "password1": "Open4khulaifi",
            "password2": "Open4khulaifi"})
        get_response = self.client.get(reverse("index"))
        self.assertContains(get_response, "Your name is: alkhulaifi", status_code=200)


class RegisterViewTests(TestCase):

    def test_get_response(self):
        get_response = self.client.get(reverse("register"))
        self.assertContains(get_response, "Registration Page!", status_code=200)
    
    def test_user_form(self):
        form_data = {
            "username": "alkhulaifi",
            "password1": "Open4khulaifi",
            "password2": "Open4khulaifi",}
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_post_response(self):
        post_response = self.client.post(reverse("register"), {
            "username": "alkhulaifi",
            "password1": "Open4khulaifi",
            "password2": "Open4khulaifi"})
        self.assertTrue(self.client.login(username="alkhulaifi", password="Open4khulaifi"))
        self.assertRedirects(post_response, "/")


class AuthViewsTests(TestCase):
    def setUp(self):
        self.client.post(reverse("register"), {
            "username": "alkhulaifi",
            "password1": "Open4khulaifi",
            "password2": "Open4khulaifi"})
        self.client.logout()

    def test_login_view_get(self):
        get_response = self.client.get(reverse('login'))

        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, "registration/login.html")

    def test_login_view_post_response_bad_login(self):
        """If login is fails client stays in login page with status code 200"""
        post_response = self.client.post(reverse("login"), {"username":"", "password":""})
        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated)
        self.assertEquals(post_response.status_code, 200)

    def test_login_view_post_response_login_works(self):
        """Creates a user through the register view, then logs in through the login view.
        If the login succeeds the client redirects to the index page."""
        post_response = self.client.post(reverse('login'), {
            "username": "alkhulaifi",
            "password": "Open4khulaifi"
        })
        user = auth.get_user(self.client)

        self.assertTrue(user.is_authenticated)
        self.assertRedirects(post_response, "/") 

    def test_login_view_error(self):
        """Theres a mistake in the password that should raise an error"""
        post_response = self.client.post(reverse('login'), {
            "username": "alkhulaifi",
            "password": "Open4khulifi"
        })

        self.assertContains(post_response, "There's something wrong with what you entered",  status_code=200)

    def test_logout_view_works(self):
        self.client.post(reverse('login'), {
            "username": "alkhulaifi",
            "password": "Open4khulaifi"
        })
        self.client.get(reverse('logout'))

        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)        

    def test_password_change_redirects_if_logged_out(self):
        get_response = self.client.get(reverse('password_change'))

        self.assertRedirects(get_response, '/accounts/login/?next=/accounts/password_change/')

    def test_password_change_get_response_if_logged_in(self):
        self.client.post(reverse('login'), {
            "username": "alkhulaifi",
            "password": "Open4khulaifi"
        })
        get_response = self.client.get(reverse('password_change'))

        self.assertTemplateUsed(get_response, 'registration/password_change.html')

    def test_password_change_bad_input(self):
        """Theres an error in the old password field"""
        self.client.post(reverse('login'), {
            "username": "alkhulaifi",
            "password": "Open4khulaifi"
        })
        post_response = self.client.post(reverse('password_change'), {
            "old_password": "open4khulaifi",
            "new_password1": "open4khulaifi",
            "new_password2": "Open4khulaifi"
        })

        self.assertContains(post_response, "There are errors in the form!")

    def test_password_change_good_inputs(self):
        self.client.login(username="alkhulaifi", password="Open4khulaifi")
        post_response = self.client.post(reverse('password_change'), {
            "old_password": "Open4khulaifi",
            "new_password1": "open4khulaifi",
            "new_password2": "open4khulaifi"
        })

        self.assertRedirects(post_response, reverse("password_change_done"))

    def test_password_change_done_without_login(self):
        get_request = self.client.get(reverse("password_change_done"))

        self.assertRedirects(get_request, "/accounts/login/?next=/accounts/password_change/done/")

    def test_password_change_done_after_login(self):
        self.client.login(username="alkhulaifi", password="Open4khulaifi")
        get_request = self.client.get(reverse("password_change_done"))

        self.assertTemplateUsed(get_request, "registration/password_change_done.html")


class AgencyCreateViewTest(TestCase):
    
    def setUp(self):
        self.client.post(reverse("register"), {
            "username": "alkhulaifi",
            "password1": "Open4khulaifi",
            "password2": "Open4khulaifi"})
        self.upload_file = open(
            "/Users/alialkhelaifi/Google_Drive/Projects/aqarwebsite/static/images/test.jpeg", 'rb')

    def test_agency_view_logged_out(self):
        """Tests that the user cannot see the agency create page without logging in"""
        self.client.logout()
        get_response = self.client.get(reverse('agency_create'))

        self.assertContains(get_response, "You are not logged in. Please log in to be able to create an agency")
        

    def test_agency_create_view(self):
        """Tests that the view does create and validate an agency instance 
        using the AgencyManager's new() method in the database"""
        post_response = self.client.post(reverse('agency_create'), {
            'name': "Ali's agency",
            'phone_number': "98821030"
        })
        agency = Agency.objects.get(name="Ali's agency")

        self.assertEqual(agency.phone_number, "98821030")
        self.assertEqual(agency.members.all()[0].username, "alkhulaifi")
        self.assertRedirects(post_response, reverse('index'))
    
    def test_agency_create_validates(self):
        """Invalid phone number, checks that AgencyManager's validation works"""
        with self.assertRaises(ValidationError):
            self.client.post(reverse('agency_create'), {
                'name': "Ali's agency",
                'phone_number': "9881030"
            })
    
    def test_agency_create_form_imagefield(self):
        text_data = {'name': "Ali's Agency"}
        file_data = {'profile_picture': 
            SimpleUploadedFile(self.upload_file.name, self.upload_file.read())}
        form = AgencyCreateForm(text_data, file_data)
        self.assertTrue(form.is_valid())
        mydir = "uploads/profile_picture"
        for photo in os.listdir(mydir):
            os.remove(os.path.join(mydir, photo)) # Delete all generated photos
        
    def test_agency_create_validates_all_fields(self):
        """Tests the all fields in the form work along with their validation"""
        profile_picture = SimpleUploadedFile(self.upload_file.name, self.upload_file.read())
        post_response = self.client.post(reverse('agency_create'), {
                'name': "Ali's agency",
                'phone_number': "98821030",
                'email': "alkhelaifi.ali@gmail.com",
                'profile_picture': profile_picture,
                'address': "Qurtuba, Block4, Street1, House91",
                'twitter': "@alkhulaifi",
                'instagram': "ali.i.alkhulaifi"
            })
        agency = Agency.objects.get(name="Ali's agency")

        self.assertEqual(agency.phone_number, "98821030")
        self.assertEqual(agency.profile_picture.size, profile_picture.size)
        self.assertEqual(agency.email, "alkhelaifi.ali@gmail.com")
        self.assertEqual(agency.address, "Qurtuba, Block4, Street1, House91")
        self.assertEqual(agency.twitter, "@alkhulaifi")
        self.assertEqual(agency.instagram, "ali.i.alkhulaifi")
        self.assertEqual(agency.members.all()[0].username, "alkhulaifi")
        self.assertRedirects(post_response, reverse('index'))

        mydir = "uploads/profile_picture"
        for photo in os.listdir(mydir):
            os.remove(os.path.join(mydir, photo)) # Delete all generated photos
        

class AgencyProfileViewTest(TestCase):
    def setUp(self):
        self.client.post(reverse("register"), {
            "username": "alkhulaifi",
            "password1": "Open4khulaifi",
            "password2": "Open4khulaifi"})
        self.upload_file = open(
            "/Users/alialkhelaifi/Google_Drive/Projects/aqarwebsite/static/images/test.jpeg", 'rb')
        profile_picture = SimpleUploadedFile(self.upload_file.name, self.upload_file.read())
        self.client.post(reverse('agency_create'), {
                'name': "Ali's agency",
                'phone_number': "98821030",
                'email': "alkhelaifi.ali@gmail.com",
                'profile_picture': profile_picture,
                'address': "Qurtuba, Block4, Street1, House91",
                'twitter': "@alkhulaifi",
                'instagram': "ali.i.alkhulaifi"
            })

    def test_agency_profile(self):
        pass

    def test_agency_profile_without_logging_in(self):
        pass

    def test_agency_profile_from_nonmember_user(self):
        pass

    def test_agency_profile_from_multiple_members(self):
        pass
        