from django.shortcuts import render, redirect
# from .models import NameRecord
# from .forms import NameForm
from django.db.models import Q

# def home(request):
#     pass
#
# def add_name(request):
#     if request.method == "POST":
#         form = NameForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = NameForm()
#     return render(request, 'transliterate/add_record.html', {'form': form})


from main.models import NameRecord
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


def update_transliterations(request):
    # Loop through all records in the NameRecord model
    for record in NameRecord.objects.all():
        # Check if transliterated first name is empty
        if not record.transliterated_first_name and record.first_name:
            transliterated = transliterate(record.first_name, sanscript.ITRANS, sanscript.DEVANAGARI)
            cleaned = transliterated.lower()
            if cleaned.endswith('a'):
                cleaned = cleaned[:-1]
            record.transliterated_first_name = cleaned

        # Check if transliterated last name is empty
        if not record.transliterated_last_name and record.last_name:
            transliterated = transliterate(record.last_name, sanscript.ITRANS, sanscript.DEVANAGARI)
            cleaned = transliterated.lower()
            if cleaned.endswith('a'):
                cleaned = cleaned[:-1]
            record.transliterated_last_name = cleaned

        # Save the updated record
        record.save()
    print('done')
    return redirect('home')

# Call the function to update transliterations
# update_transliterations()
