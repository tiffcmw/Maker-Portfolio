from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Message, Translation, GrammarCorrection, AudioSubmission, PronunciationFeedback, Dictionary

# this is just tedious referencing on the models

## MESSAGES
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'recipient', 'is_from_ai', 'language', 'timestamp')
    list_filter = ('is_from_ai', 'language', 'timestamp')
    search_fields = ('message_text', 'sender__username', 'recipient__username')
    readonly_fields = ('timestamp',)  # Prevent editing of the timestamp field

    fieldsets = (
        (None, {
            'fields': ('sender', 'recipient', 'message_text', 'is_from_ai', 'language', 'timestamp')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            # Don't allow editing the sender and recipient for existing messages
            return self.readonly_fields + ('sender', 'recipient')
        return self.readonly_fields
admin.site.register(Message, MessageAdmin)

## TRANSLATIONS
class TranslationAdmin(admin.ModelAdmin):
    list_display = ('translation_id', 'message', 'original_language', 'translated_language', 'timestamp')
    list_filter = ('original_language', 'translated_language', 'timestamp')
    search_fields = ('translated_text', 'message__message_text')
    readonly_fields = ('timestamp',)  # Prevent editing of the timestamp after creation

    fieldsets = (
        (None, {
            'fields': ('message', 'original_language', 'translated_language', 'translated_text', 'timestamp')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            # Prevent editing of message and languages for existing translations
            return self.readonly_fields + ('message', 'original_language', 'translated_language')
        return self.readonly_fields
admin.site.register(Translation, TranslationAdmin)


## GRAMMAR CORRECTION
class GrammarCorrectionAdmin(admin.ModelAdmin):
    list_display = (
        'correction_id',
        'message',
        'confidence',
        'should_replace',
        'correction_type',
        'top_category_id',
        'timestamp'
    )
    list_filter = ('should_replace', 'correction_type', 'top_category_id', 'timestamp')
    search_fields = ('mistake_text', 'message__message_text')
    readonly_fields = ('timestamp',)  # Prevent editing of the timestamp

    fieldsets = (
        (None, {
            'fields': (
                'message',
                'confidence',
                'should_replace',
                'correction_type',
                'top_category_id',
                'top_category_description',
                'mistake_text',
                'mistake_from',
                'mistake_to',
                'mistake_definition',
                'lrn_frg',
                'suggestions',
                'sentences',
                'timestamp'
            )
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            # Prevent certain fields from being edited after the correction has been created
            return self.readonly_fields + ('message', 'confidence', 'should_replace', 'correction_type')
        return self.readonly_fields
admin.site.register(GrammarCorrection, GrammarCorrectionAdmin)

## AUDIO SUBMISSIONS
class AudioSubmissionAdmin(admin.ModelAdmin):
    list_display = ('audio_id', 'user', 'message', 'audio_url', 'submission_date')
    list_filter = ('submission_date', 'user')
    search_fields = ('audio_url', 'message__message_text', 'user__username')  # Adjust field lookups according to user model fields
    readonly_fields = ('submission_date',)  # To ensure the submission date is not editable

    fieldsets = (
        (None, {
            'fields': ('user', 'message', 'audio_url', 'submission_date')
        }),
    )
admin.site.register(AudioSubmission, AudioSubmissionAdmin)

## PRONUNCIATION FEEBACK
class PronunciationFeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'feedback_id',
        'audio_submission',
        'accuracy_score',
        'fluency_score',
        'completeness_score',
        'prosody_score',
        'pron_score',
        'grammar_score',
        'topic_score',
        'feedback_timestamp'
    )
    list_filter = ('feedback_timestamp', 'accuracy_score', 'fluency_score', 'completeness_score', 'prosody_score', 'pron_score', 'grammar_score', 'topic_score')
    search_fields = ('audio_submission__audio_url', 'error_type')  # Adjust field lookups according to related models' fields
    readonly_fields = ('feedback_timestamp',)  # To ensure the timestamp is not editable

    fieldsets = (
        (None, {
            'fields': (
                'audio_submission',
                'accuracy_score',
                'fluency_score',
                'completeness_score',
                'prosody_score',
                'pron_score',
                'grammar_score',
                'topic_score',
                'error_type',
                'feedback_timestamp',
            )
        }),
    )
admin.site.register(PronunciationFeedback, PronunciationFeedbackAdmin)

## DICTIONARY
class DictionaryAdmin(admin.ModelAdmin):
    list_display = (
        'entry_id',
        'english_word',
        'english_phonetic',
        'chinese_translation',
        'familiarity_metric'
    )
    list_filter = ('familiarity_metric',)
    search_fields = ('english_word', 'english_phonetic', 'chinese_translation')
    list_editable = ('familiarity_metric',)  # Allows inline editing of the familiarity metric from the list view

    fieldsets = (
        (None, {
            'fields': (
                'english_word',
                'english_phonetic',
                'chinese_translation',
                'familiarity_metric',
            )
        }),
    )
admin.site.register(Dictionary, DictionaryAdmin)
