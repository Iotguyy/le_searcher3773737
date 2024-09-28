from django.db import models

# Create your models here.


from django.db import models
# from polyglot.transliteration import Transliterator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

class NameRecord(models.Model):
    first_name = models.CharField(max_length=100)         # First name
    last_name = models.CharField(max_length=100)          # Surname
    transliterated_first_name = models.CharField(max_length=100)  # Transliterated first name
    transliterated_last_name = models.CharField(max_length=100)   # Transliterated surname

    # def save(self, *args, **kwargs):
    #     # Transliterate Hindi names to English using Polyglot
    #     # transliterator = Transliterator(source_lang='hi', target_lang='en')
    #     if self.first_name:
    #         # self.transliterated_first_name = transliterator.transliterate(self.first_name_hindi)
    #         self.transliterated_first_name = self.first_name
    #     if self.last_name:
    #         # self.transliterated_last_name = transliterator.transliterate(self.last_name_hindi)
    #         self.transliterated_last_name = self.last_name
    #
    #     super().save(*args, **kwargs)  # Call the real save method





    def save(self, *args, **kwargs):

        if self.first_name:
            transliterated = transliterate(self.first_name, sanscript.DEVANAGARI, sanscript.ITRANS)

            cleaned = transliterated.lower()  # Convert to lowercase

            # Remove trailing 'a' if present
            if cleaned.endswith('a'):
                cleaned = cleaned[:-1]
            self.transliterated_first_name = cleaned
        if self.last_name:
            transliterated = transliterate(self.last_name, sanscript.DEVANAGARI, sanscript.ITRANS)

            cleaned = transliterated.lower()  # Convert to lowercase

            # Remove trailing 'a' if present
            if cleaned.endswith('a'):
                cleaned = cleaned[:-1]


            self.transliterated_last_name = cleaned

        super().save(*args, **kwargs)  # Call the real save method


    def __str__(self):
        return f"{self.first_name} {self.last_name}"