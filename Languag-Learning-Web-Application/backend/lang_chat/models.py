from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import JSONField

# before i created these models i just kind of graphed out 
# - what kind of functions i would like in the web app
# - what kind of apis or information i would need for those functions
# - what do i need to store to maintain smooth functionality and full user experiencce


# Chats (groups of messages)     
class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    chat_name = models.CharField(max_length=30)
    participants = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        participant_usernames = ', '.join([user.username for user in self.participants.all()])
        return f"Chat {self.chat_id} between {participant_usernames}"

    class Meta:
        db_table = 'Chats'
        
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_chat = models.ForeignKey(Chat, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

# so the message model. it define each chat message's characteristics.
# i just looked at exisitng web chat apps like chatgpt for reference, and they mostly had functions like 
# display past message with username and time, so i added the fields sender, and timestamp
# i also thought of having functionalities like translation so having the langauge field would be useful later on

# Messages
class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    chat_id = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE, db_column='chat_id')
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.SET_NULL, null=True, blank=True)
    is_from_ai = models.BooleanField(default=False)
    message_text = models.TextField()
    language = models.CharField(max_length=10)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} in Chat {self.chat_id.chat_id} at {self.timestamp}"

    class Meta:
        db_table = 'Original Messages'

# all the below models are for functionalities and apis. 
# i look at what is availale in the responses of the apis and take into consideration what i need, 
# then register the items into the tables. 
# APIs:
# translations: Google Cloud Translation API
# grammar corrections: Ginger Grammar API
# speaking corrections: Azure Speech Services

# Translations
class Translation(models.Model):
    translation_id = models.AutoField(primary_key=True)
    message = models.ForeignKey('Message', on_delete=models.CASCADE)  # Assuming 'Message' is already defined
    original_language = models.CharField(max_length=10)
    translated_language = models.CharField(max_length=10)
    translated_text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Translation from {self.original_language} to {self.translated_language}"

    class Meta:
        db_table = 'Message Translations'

# Grammar Correction
class GrammarCorrection(models.Model):
    correction_id = models.AutoField(primary_key=True)
    message = models.ForeignKey(Message, related_name='corrections', on_delete=models.CASCADE)
    confidence = models.IntegerField()
    should_replace = models.BooleanField()
    correction_type = models.IntegerField()
    top_category_id = models.IntegerField()
    top_category_description = models.TextField()
    mistake_text = models.TextField()
    mistake_from = models.IntegerField()
    mistake_to = models.IntegerField()
    mistake_definition = models.TextField(null=True, blank=True)
    lrn_frg = models.TextField()
    suggestions = models.JSONField()
    sentences = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Correction for "{self.mistake_text}" in message {self.message_id}'

    class Meta:
        db_table = 'User Message Corrections'

# Pronounciation Feedback
class PronunciationFeedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    audio_submission = models.ForeignKey('AudioSubmission', on_delete=models.CASCADE)
    accuracy_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fluency_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    completeness_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    prosody_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pron_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grammar_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    topic_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    error_type = JSONField(null=True, blank=True)  # Use JSONField from Django's PostgreSQL specific fields
    feedback_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback {self.feedback_id} for Audio {self.audio_submission_id}'

    class Meta:
        db_table = 'User Pronunciation Feedback'


# Dictionary (for the dictionary function)
# phonetics from the IBM watson text to speech
class Dictionary(models.Model):
    FAMILIARITY_CHOICES = [
        ('excellent', 'Excellent'),
        ('mediocre', 'Mediocre'),
        ('unsatisfactory', 'Unsatisfactory'),
    ]

    entry_id = models.AutoField(primary_key=True)
    english_word = models.CharField(max_length=255, unique=True)
    english_phonetic = models.CharField(max_length=255, blank=True, null=True)
    chinese_translation = models.CharField(max_length=255)
    familiarity_metric = models.CharField(
        max_length=15,
        choices=FAMILIARITY_CHOICES,
        default='mediocre'
    )

    def __str__(self):
        return self.english_word

    class Meta:
        unique_together = (('english_word', 'chinese_translation'),)
        db_table = 'User Dictionary'
