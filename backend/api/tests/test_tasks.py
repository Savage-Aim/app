# stdlib
from datetime import timedelta
from typing import Dict
from unittest.mock import patch
# lib
from django.utils import timezone
# local
from api.models import Character, Notification
from api.tasks import xivapi_lookup, verify_character, cleanup
from .test_base import SavageAimTestCase


# Pretend to be a logger
LOGGER = type('logger', (), {'error': lambda msg: msg})


# Mock response functions
def get_desktop_response(url: str, headers: Dict[str, str]):
    """
    Return a faked http response object for the desktop site
    """
    char_id = url.split('/')[-1]
    obj = Character.objects.filter(lodestone_id=char_id).first()
    body = f'<html><head></head><body><div class="character__selfintroduction">{obj.token}</div></body></html>'
    return type('response', (), {'status_code': 200, 'content': body})


def get_mobile_response(url: str, headers: Dict[str, str]):
    """
    Return a faked http response object for the mobile site
    """
    char_id = url.split('/')[-1]
    obj = Character.objects.filter(lodestone_id=char_id).first()
    body = f'<html><head></head><body><div class="character__character_profile">{obj.token}</div></body></html>'
    return type('response', (), {'status_code': 200, 'content': body})


def get_empty_response(url: str, headers: Dict[str, str]):
    """
    Return a faked http response object for a site that doesn't contain the token we need
    """
    body = '<html><head></head><body><div class="character__character_profile"></div></body></html>'
    return type('response', (), {'status_code': 200, 'content': body})


def get_error_response(url: str, headers: Dict[str, str]):
    """
    Return a faked http response object for a non 200 error
    """
    return type('response', (), {'status_code': 400})


class TasksTestSuite(SavageAimTestCase):
    """
    Test the functions in the tasks file to make sure they work as intended

    Mock requests to return pre-determined html bodies
    """

    def tearDown(self):
        Notification.objects.all().delete()
        Character.objects.all().delete()

    def test_cleanup(self):
        """
        - Test the cleanup task by creating a couple of different Characters and running the task
        - Then ensure that the ones that should have been deleted are erased from the DB
        """
        old_unver = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
            verified=False,
        )
        old_ver = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=11289475,
            user=self._get_user(),
            name='Char 2',
            world='Lich',
            verified=True,
        )
        # Update all created stamps to 1 week ago
        Character.objects.update(created=timezone.now() - timedelta(days=7))
        # Create one last character that's new
        new_unver = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=2498174123,
            user=self._get_user(),
            name='Char 3',
            world='Lich',
            verified=False,
        )

        # Run the cleanup task and ensure the DB is as it should be
        cleanup()
        with self.assertRaises(Character.DoesNotExist):
            Character.objects.get(pk=old_unver.pk)
        self.assertEqual(Character.objects.filter(pk__in=[old_ver.pk, new_unver.pk]).count(), 2)

    @patch('requests.get', side_effect=get_desktop_response)
    def test_verify_character(self, mocked_get):
        """
        Test a full verification call for a character is successful

        Also ensure that other copies of this character get deleted
        """
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
            verified=False,
            token=Character.generate_token(),
        )
        other_version = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._create_user(),
            name='Char 2',
            world='Lich',
            verified=False,
            token=Character.generate_token(),
        )
        verify_character(char.pk)

        char.refresh_from_db()
        self.assertTrue(char.verified)
        self.assertEqual(Notification.objects.count(), 1)
        with self.assertRaises(Character.DoesNotExist):
            Character.objects.get(pk=other_version.pk)

        # Check for Notification
        notif = Notification.objects.first()
        message = f'The verification of {char} has succeeded!'
        self.assertEqual(notif.text, message)

    @patch('requests.get', side_effect=get_error_response)
    def test_verify_character_failures(self, mocked_get):
        """
        Handle errors in the verification code to ensure it all works as expected
        """
        # Start with an already verified character
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
            verified=True,
            token=Character.generate_token(),
        )
        verify_character(char.pk)
        mocked_get.assert_not_called()

        # Unverify the character and attempt to, then check the notifications for the reason why
        char.verified = False
        char.save()
        verify_character(char.pk)
        mocked_get.assert_called_once()

        # Check for Notification
        self.assertEqual(Notification.objects.count(), 1)
        notif = Notification.objects.first()
        error = 'Lodestone may be down.'
        message = f'The verification of {char} has failed! Reason: {error}'
        self.assertEqual(notif.text, message)

    @patch('requests.get', side_effect=get_desktop_response)
    def test_xivapi_lookup_desktop(self, mocked_get):
        """
        Check that the desktop search works for beautiful soup
        """
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
            verified=False,
            token=Character.generate_token(),
        )
        # Run the function and assert the response is None
        self.assertIsNone(xivapi_lookup(char.lodestone_id, char.token, LOGGER))

    @patch('requests.get', side_effect=get_mobile_response)
    def test_xivapi_lookup_mobile(self, mocked_get):
        """
        Check that the mobile search works for beautiful soup
        """
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
            verified=False,
            token=Character.generate_token(),
        )
        # Run the function and assert the response is None
        self.assertIsNone(xivapi_lookup(char.lodestone_id, char.token, LOGGER))

    @patch('requests.get', side_effect=get_empty_response)
    def test_xivapi_lookup_empty(self, mocked_get):
        """
        If no token can be found, we need to ensure the correct error message is returned
        """
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
            verified=False,
            token=Character.generate_token(),
        )
        # Run the function and assert the response is None
        self.assertEqual(
            xivapi_lookup(char.lodestone_id, char.token, LOGGER),
            'Could not find the verification code in the Lodestone profile.',
        )

    @patch('requests.get', side_effect=get_error_response)
    def test_xivapi_lookup_error(self, mocked_get):
        """
        If lodestone gets an error, ensure the right message is returned
        """
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
            verified=False,
            token=Character.generate_token(),
        )
        # Run the function and assert the response is None
        self.assertEqual(
            xivapi_lookup(char.lodestone_id, char.token, LOGGER),
            'Lodestone may be down.',
        )
