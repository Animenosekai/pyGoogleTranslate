"""
pyGoogleTranslate caching system.

INCLUDES:
- import_cache()
- export_cache()
- search_translation_cache()
- add_translation_cache()

© Anime no Sekai - 2020
"""

import os
from lifeeasy import read_file, write_file, today, current_time, working_dir, find_inside_file
from .language_code import verify_language_code

translation_caches_path = os.path.dirname(os.path.abspath(__file__)) + '/translation_caches/'
translation_caches_name = 'translation_caches.animenosekai_caches'

def import_cache(cache_file_location):
    """
    Import a .animenosekai_caches translation cache file.

    © Anime no Sekai - 2020
    """
    current_cache_file_content = read_file(translation_caches_path + translation_caches_name).split('\n')
    new_cache_file_content = read_file(cache_file_location).split('\n')
    write_file(translation_caches_name, f'\n\n[IMPORTED {today()} {current_time()}]\n', translation_caches_path, append=True)
    for line in new_cache_file_content:
        if not line in current_cache_file_content:
            write_file(translation_caches_name, line, translation_caches_path, append=True)
    
def export_cache(destination=working_dir):
    """
    Export the cache file to be imported later (after an update for example).

    © Anime no Sekai - 2020
    """
    write_file('pyGoogleTranslateCacheExport.animenosekai_caches', read_file(translation_caches_path + translation_caches_name), destination=destination)

def search_translation_cache(source_language, destination_language, source):
    """
    Searches a translation through the caches.
    """
    line_start = f'[sl={verify_language_code(source_language)}]｜[dl={verify_language_code(destination_language)}]｜[source={source}]'
    search_result = find_inside_file(translation_caches_path + translation_caches_name, line_start)
    if not search_result == {}:
        return {'result': search_result['line'].split('｜')[3][8:][:-2], 'line_number': str(search_result['line_number'])}
    else:
        line_start = f'[sl={verify_language_code(destination_language)}]｜[dl={verify_language_code(source_language)}]'
        search_result = find_inside_file(translation_caches_path + translation_caches_name, line_start, whole_document=True)
        if not search_result == {}:
            found = False
            for result in search_result:
                if result['line'].split('｜')[3][8:][:-2] == source:
                    found = True
                    return {'result': result['line'].split('｜')[2][8:][:-1], 'line_number': str(result['line_number'])}
            if not found:
                return None
        else:
            return None

def add_translation_cache(source_language, destination_language, source, result):
    """
    Adds a translation to the cache file.
    """   
    line = f'[sl={verify_language_code(source_language)}]｜[dl={verify_language_code(destination_language)}]｜[source={source}]｜[result={result}]\n'
    write_file(translation_caches_name, line, translation_caches_path, append=True)
