from django.shortcuts import render, redirect
from .models import NameRecord

from django.db.models import Q

# def home(request):
#     return render(request,'home.html')
#
# def add_name(request):
#     if request.method == "POST":
#         form = NameForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = NameForm()
#     return render(request, 'add_record.html', {'form': form})
#
# def fuzzy_search(request):
#     query = request.GET.get('q', '')
#     phonetic_records = NameRecord.objects.all()
#
# def phonetic_search(request):
#     query = request.GET.get('q', '')
#     pass

from django.shortcuts import render, redirect
from django.db.models import Q
from .models import NameRecord
from .forms import NameSearchForm, NameRecordForm
from fuzzywuzzy import fuzz
import jellyfish
import phonetics
import re


def home(request):
    records = NameRecord.objects.all()
    form = NameSearchForm(request.GET or None)
    results = []
    fun = True
    if form.is_valid():
        query = form.cleaned_data['query']
        search_type = form.cleaned_data['search_type']
        print(query)
        print(search_type)
        results = perform_search(query, search_type)
        print(results)

        if results:
            print('hai')
            fun = False
        else:
            fun = False

    context = {
        'records': records,
        'form': form,
        'results': results,
        'fun': fun
    }
    return render(request, 'home.html', context)

def add_record(request):
    if request.method == 'POST':
        form = NameRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NameRecordForm()
    return render(request, 'add_record.html', {'form': form})

def perform_search(query, search_type):
    words = query.split()
    if len(words) == 1:
        if search_type == 'exact':
            return NameRecord.objects.filter(
                Q(first_name__iexact=query) |
                Q(last_name__iexact=query) |
                Q(transliterated_first_name__iexact=query) |
                Q(transliterated_last_name__iexact=query)
            )
        elif search_type == 'fuzzy':
            return fuzzy_search(query)
        elif search_type == 'phonetic':
            return phonetic_search(query)
    elif len(words) >= 2:
        print('came')
        first_name, last_name = words[0], ' '.join(words[1:])
        print(first_name)
        print(last_name)
        if search_type == 'exact':
            return NameRecord.objects.filter(
                (Q(first_name__iexact=first_name) & Q(last_name__iexact=last_name)) |
                (Q(transliterated_first_name__iexact=first_name) & Q(transliterated_last_name__iexact=last_name))
            )
        elif search_type == 'fuzzy':
            return fuzzy_search(first_name, last_name)
        elif search_type == 'phonetic':
            return phonetic_search(first_name, last_name)
    return NameRecord.objects.none()

def fuzzy_search(first_name, last_name=None):
    threshold = 70
    if last_name is None:
        return [
            record for record in NameRecord.objects.all()
            if fuzz.partial_ratio(first_name, record.first_name) >= threshold or
               fuzz.partial_ratio(first_name, record.last_name) >= threshold or
               fuzz.partial_ratio(first_name, record.transliterated_first_name) >= threshold or
               fuzz.partial_ratio(first_name, record.transliterated_last_name) >= threshold
        ]
    else:
        return [
            record for record in NameRecord.objects.all()
            if (fuzz.partial_ratio(first_name, record.first_name) >= threshold and
                fuzz.partial_ratio(last_name, record.last_name) >= threshold) or
               (fuzz.partial_ratio(first_name, record.transliterated_first_name) >= threshold and
                fuzz.partial_ratio(last_name, record.transliterated_last_name) >= threshold)
        ]






def clean_name(name):
    """Remove non-alphabetic characters and return a lowercase version."""
    if name:
        return re.sub(r'[^a-zA-Z]', '', name.lower())  # Keep only alphabetic characters
    return ''

def phonetic_search(first_name, last_name=None):
    print(first_name)
    print(last_name)
    # if last_name is None:
    #     return NameRecord.objects.filter(
    #         Q(first_name__iexact=jellyfish.soundex(first_name)) |
    #         Q(last_name__iexact=jellyfish.soundex(first_name)) |
    #         Q(transliterated_first_name__iexact=jellyfish.soundex(first_name)) |
    #         Q(transliterated_last_name__iexact=jellyfish.soundex(first_name))
    #     )
    # else:
    #     return NameRecord.objects.filter(
    #         (Q(first_name__iexact=jellyfish.soundex(first_name)) &
    #          Q(last_name__iexact=jellyfish.soundex(last_name))) |
    #         (Q(transliterated_first_name__iexact=jellyfish.soundex(first_name)) &
    #          Q(transliterated_last_name__iexact=jellyfish.soundex(last_name)))
    #     )

    # first_name_soundex = phonetics.soundex(first_name)
    # if last_name is None:
    #     return [
    #         record for record in NameRecord.objects.all()
    #         if (phonetics.soundex(record.first_name) == first_name_soundex or
    #             phonetics.soundex(record.last_name) == first_name_soundex or
    #             phonetics.soundex(record.transliterated_first_name) == first_name_soundex or
    #             phonetics.soundex(record.transliterated_last_name) == first_name_soundex)
    #     ]
    # else:
    #     last_name_soundex = phonetics.soundex(last_name)
    #     return [
    #         record for record in NameRecord.objects.all()
    #         if (phonetics.soundex(record.first_name) == first_name_soundex and
    #             phonetics.soundex(record.last_name) == last_name_soundex) or
    #            (phonetics.soundex(record.transliterated_first_name) == first_name_soundex and
    #             phonetics.soundex(record.transliterated_last_name) == last_name_soundex)
    #     ]

    # if not first_name:  # Check if first_name is None or empty
    #     return []
    #
    # first_name_soundex = phonetics.soundex(first_name)
    # print(first_name_soundex)
    # if last_name is None:
    #     return [
    #         record for record in NameRecord.objects.all()
    #         if (phonetics.soundex(record.first_name) == first_name_soundex or
    #             phonetics.soundex(record.last_name) == first_name_soundex or
    #             phonetics.soundex(record.transliterated_first_name) == first_name_soundex or
    #             phonetics.soundex(record.transliterated_last_name) == first_name_soundex)
    #     ]
    # else:
    #     if not last_name:  # Check if last_name is None or empty
    #         return []  # Return an empty list if last_name is not provided
    #
    #     last_name_soundex = phonetics.soundex(last_name)
    #     print(last_name_soundex)
    #     return [
    #         record for record in NameRecord.objects.all()
    #         if (phonetics.soundex(record.first_name) == first_name_soundex and
    #             phonetics.soundex(record.last_name) == last_name_soundex) or
    #            (phonetics.soundex(record.transliterated_first_name) == first_name_soundex and
    #             phonetics.soundex(record.transliterated_last_name) == last_name_soundex)
    #     ]

    query_soundex = phonetics.soundex(first_name)
    return [record for record in NameRecord.objects.all()
            if phonetics.soundex(record.transliterated_first_name) == query_soundex
            or phonetics.soundex(record.transliterated_last_name) == query_soundex]