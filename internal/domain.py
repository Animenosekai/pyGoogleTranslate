"""

"""

from . import google_translate_data

gt_domain = 'translate.google.com'

class GoogleTranslateDomainError(Exception):
    """
    When the domain is incorrect.
    """
    def __init__(self, msg=None):
        self.msg = msg 
    def __str__(self):
        exception_msg = f"\n\n⚠️ ⚠️ ⚠️\n{self.msg}\n"
        return exception_msg

def google_translate_domain(domain='translate.google.com'):
    """
    Changes the used google translate domain name (i.e translate.google.com) to the given domain (i.e translate.google.co.jp)
    """
    global gt_domain
    clean_domain = domain.lower().replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]
    if clean_domain in google_translate_data.google_translate_domains_data():
        gt_domain = clean_domain
        return gt_domain
    else:
        raise GoogleTranslateDomainError(f'{clean_domain} is not a correct Google Translate domain.\n {gt_domain} will be used instead.')
