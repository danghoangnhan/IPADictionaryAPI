from django.db import models

from dictionaries.models import dictionary


class vocabulary(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=50)
    symbol_text = models.CharField(max_length=50)
    symbol_image = models.CharField(max_length=50)
    tone = models.CharField(max_length=5)
    dictionary_name = models.ForeignKey(dictionary,
                                        related_name='dictionary_name',
                                        on_delete=models.CASCADE,
                                        to_field='name',
                                        db_column='dictionary_name')
    ipa = models.CharField(max_length=5)
    description = models.CharField(max_length=1000, db_column='description')

    class Meta:
        db_table = 'vocabulary'

    def __str__(self):
        return self.word