from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from .models import Server, AdoptionApplication


def make_server(**kwargs):
    defaults = dict(
        name='Test Server',
        slug='test-server',
        species=Server.Species.DELL,
        size=Server.Size.TWO_U,
        sex=Server.Sex.SHE,
        age_years=5,
        status=Server.Status.AVAILABLE,
        adoption_fee_cents=2000,
        backstory='A fine machine.',
        personality='loyal, dependable',
        is_featured=False,
    )
    defaults.update(kwargs)
    return Server.objects.create(**defaults)


def make_application(server, **kwargs):
    defaults = dict(
        server=server,
        applicant_name='Alice',
        applicant_email='alice@example.com',
        applicant_location='Helsinki',
        decibel_tolerance=AdoptionApplication.DecibelTolerance.MEDIUM,
        why_this_server='This server is exactly what I have been looking for in a machine.',
    )
    defaults.update(kwargs)
    return AdoptionApplication.objects.create(**defaults)


class ServerModelTests(TestCase):
    def test_adoption_fee_display_free(self):
        server = make_server(adoption_fee_cents=0)
        self.assertEqual(server.adoption_fee_display, 'Free to a good home')

    def test_adoption_fee_display_with_amount(self):
        server = make_server(adoption_fee_cents=5000)
        self.assertEqual(server.adoption_fee_display, '$50 suggested')

    def test_personality_list_splits_on_comma(self):
        server = make_server(personality='loyal, loud, runs hot')
        self.assertEqual(server.personality_list, ['loyal', 'loud', 'runs hot'])

    def test_personality_list_empty_string(self):
        server = make_server(personality='')
        self.assertEqual(server.personality_list, [])


class ServerManagerTests(TestCase):
    def setUp(self):
        self.available = make_server(slug='avail', status=Server.Status.AVAILABLE)
        self.adopted = make_server(slug='adopted', status=Server.Status.ADOPTED, name='Old Box')
        self.featured = make_server(slug='feat', is_featured=True, status=Server.Status.AVAILABLE, name='Featured')
    def test_available_excludes_adopted(self):
        qs = Server.objects.available()
        self.assertIn(self.available, qs)
        self.assertNotIn(self.adopted, qs)

    def test_featured_returns_only_featured_available(self):
        qs = Server.objects.featured()
        self.assertIn(self.featured, qs)
        self.assertNotIn(self.available, qs)

    def test_pending_manager_excludes_approved(self):
        server = make_server(slug='pending-test')
        pending = make_application(server)
        approved = make_application(server, review_status=AdoptionApplication.ReviewStatus.APPROVED)
        qs = AdoptionApplication.objects.pending()
        self.assertIn(pending, qs)
        self.assertNotIn(approved, qs)


class HomeViewTests(TestCase):
    def test_home_returns_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_shows_featured_servers(self):
        make_server(slug='feat', is_featured=True, name='Bertha')
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Bertha')

    def test_stats_show_on_home(self):
        make_server(slug='a1', status=Server.Status.AVAILABLE)
        make_server(slug='a2', status=Server.Status.ADOPTED, name='Gone')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class ServerListViewTests(TestCase):
    def setUp(self):
        make_server(slug='s1', name='Alpha')
        make_server(slug='s2', name='Beta', status=Server.Status.ADOPTED)

    def test_list_returns_200(self):
        response = self.client.get(reverse('server_list'))
        self.assertEqual(response.status_code, 200)

    def test_htmx_request_returns_partial(self):
        response = self.client.get(reverse('server_list'), HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '<!DOCTYPE html>')

    def test_filter_by_status(self):
        response = self.client.get(reverse('server_list'), {'status': 'adopted'})
        self.assertContains(response, 'Beta')
        self.assertNotContains(response, 'Alpha')


class ServerDetailViewTests(TestCase):
    def setUp(self):
        self.server = make_server()

    def test_detail_returns_200(self):
        response = self.client.get(reverse('server_detail', args=['test-server']))
        self.assertEqual(response.status_code, 200)

    def test_detail_shows_server_name(self):
        response = self.client.get(reverse('server_detail', args=['test-server']))
        self.assertContains(response, 'Test Server')

    def test_nonexistent_slug_returns_404(self):
        response = self.client.get(reverse('server_detail', args=['does-not-exist']))
        self.assertEqual(response.status_code, 404)


class ApplyViewTests(TestCase):
    def setUp(self):
        self.server = make_server()
        self.valid_data = {
            'applicant_name': 'Bob',
            'applicant_email': 'bob@example.com',
            'applicant_location': 'Sydney',
            'decibel_tolerance': 'loud',
            'why_this_server': 'This is a very compelling reason to adopt this particular server.',
        }

    def test_valid_submission_creates_application(self):
        self.client.post(reverse('apply', args=['test-server']), self.valid_data)
        self.assertEqual(AdoptionApplication.objects.count(), 1)
        self.assertEqual(AdoptionApplication.objects.first().applicant_name, 'Bob')

    def test_valid_submission_redirects_to_status_page(self):
        response = self.client.post(reverse('apply', args=['test-server']), self.valid_data)
        application = AdoptionApplication.objects.first()
        self.assertRedirects(response, reverse('application_status', args=[application.pk]))

    def test_nonexistent_server_returns_404(self):
        response = self.client.post(reverse('apply', args=['ghost']), self.valid_data)
        self.assertEqual(response.status_code, 404)


class ApplicationStatusViewTests(TestCase):
    def test_status_page_returns_200(self):
        server = make_server()
        application = make_application(server)
        response = self.client.get(reverse('application_status', args=[application.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice')


class AdminApproveActionTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.client.force_login(self.staff)
        self.server = make_server()
        self.application = make_application(self.server)

    def test_approve_marks_application_approved(self):
        self.client.post(
            '/admin/shelter/adoptionapplication/',
            {
                'action': 'approve_selected',
                '_selected_action': [str(self.application.pk)],
            },
        )
        self.application.refresh_from_db()
        self.assertEqual(self.application.review_status, AdoptionApplication.ReviewStatus.APPROVED)

    def test_approve_marks_server_adopted(self):
        self.client.post(
            '/admin/shelter/adoptionapplication/',
            {
                'action': 'approve_selected',
                '_selected_action': [str(self.application.pk)],
            },
        )
        self.server.refresh_from_db()
        self.assertEqual(self.server.status, Server.Status.ADOPTED)

    def test_approve_stamps_adopter_name_on_server(self):
        self.client.post(
            '/admin/shelter/adoptionapplication/',
            {
                'action': 'approve_selected',
                '_selected_action': [str(self.application.pk)],
            },
        )
        self.server.refresh_from_db()
        self.assertEqual(self.server.adopted_by_name, 'Alice')
