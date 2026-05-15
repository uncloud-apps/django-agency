import uuid
from django.db import models
from django.utils import timezone


class ServerManager(models.Manager):
    def available(self):
        return self.filter(status=Server.Status.AVAILABLE)

    def featured(self):
        return self.filter(status=Server.Status.AVAILABLE, is_featured=True)



class Server(models.Model):
    class Species(models.TextChoices):
        DELL = 'dell', 'Dell'
        HP = 'hp', 'HP'
        SUPERMICRO = 'supermicro', 'Supermicro'
        RASPBERRY_PI = 'rpi', 'Raspberry Pi'
        MAC_MINI = 'macmini', 'Mac Mini'
        WHITEBOX = 'whitebox', 'Whitebox'
        MYSTERY = 'mystery', 'Mystery'

    class Size(models.TextChoices):
        ONE_U = '1u', '1U'
        TWO_U = '2u', '2U'
        FOUR_U = '4u', '4U'
        SFF = 'sff', 'Small Form Factor'
        FULL_TOWER = 'tower', 'Full Tower'
        PALM_SIZED = 'palm', 'Palm-Sized'

    class Sex(models.TextChoices):
        SHE = 'she', 'She/Her'
        HE = 'he', 'He/Him'
        THEY = 'they', 'They/Them'
        ITS_COMPLICATED = 'complicated', "It's Complicated"

    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        ON_HOLD = 'on_hold', 'On Hold'
        ADOPTED = 'adopted', 'Adopted'
        IN_FOSTER = 'foster', 'In Foster Care'

    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)
    species = models.CharField(max_length=20, choices=Species)
    size = models.CharField(max_length=20, choices=Size)
    sex = models.CharField(max_length=20, choices=Sex)
    age_years = models.PositiveSmallIntegerField()
    arrival_date = models.DateField(default=timezone.localdate)
    status = models.CharField(max_length=20, choices=Status, default=Status.AVAILABLE)
    adoption_fee_cents = models.PositiveIntegerField(default=0)
    backstory = models.TextField()
    personality = models.CharField(max_length=255, help_text='Comma-separated traits')
    special_needs = models.CharField(max_length=255, blank=True)
    portrait = models.ImageField(upload_to='portraits/', blank=True)
    is_featured = models.BooleanField(default=False)
    adopted_by_name = models.CharField(max_length=120, blank=True)
    adopted_on = models.DateField(null=True, blank=True)

    objects = ServerManager()

    class Meta:
        ordering = ['-is_featured', 'name']

    def __str__(self):
        return self.name

    @property
    def adoption_fee_display(self):
        if self.adoption_fee_cents == 0:
            return 'Free to a good home'
        dollars = self.adoption_fee_cents / 100
        return f'${dollars:.0f} suggested'

    @property
    def personality_list(self):
        return [t.strip() for t in self.personality.split(',') if t.strip()]


class AdoptionApplicationManager(models.Manager):
    def pending(self):
        return self.filter(review_status=AdoptionApplication.ReviewStatus.PENDING).order_by('-created_at')


class AdoptionApplication(models.Model):
    class DecibelTolerance(models.TextChoices):
        QUIET = 'quiet', 'Whisper-quiet only'
        MEDIUM = 'medium', 'A gentle hum is fine'
        LOUD = 'loud', 'I love the sound of spinning fans'

    class ReviewStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        DECLINED = 'declined', 'Declined'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='applications')
    applicant_name = models.CharField(max_length=120)
    applicant_email = models.EmailField()
    applicant_location = models.CharField(max_length=160)
    decibel_tolerance = models.CharField(max_length=20, choices=DecibelTolerance)
    other_servers_present = models.CharField(max_length=255, blank=True)
    why_this_server = models.TextField()
    review_status = models.CharField(max_length=20, choices=ReviewStatus, default=ReviewStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    objects = AdoptionApplicationManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.applicant_name} -> {self.server.name}'
