"""Mechanical publication checks; never a substitute for legal or editorial review.

Hard errors: missing output, secrets, explicit brand restrictions, cross-brand leakage,
public personal-data patterns, unresolved placeholders/refusals.
Review flags: objective claims, commercial conditions, careful/pending brand terms.
Format warnings: soft suggestions only.
"""
from __future__ import annotations
import hashlib
import re
import unicodedata

SUGGESTED_LENGTHS = {'instagram': (60, 2200), 'linkedin': (200, 3000), 'comment': (20, 600)}
PERCENT = re.compile(r'(?<!\w)(\d+(?:[.,]\d+)?)\s*%')
MULTIPLIER = re.compile(r'(?<!\w)(\d+(?:[.,]\d+)?)\s*[xX](?!\w)')
PRICE = re.compile(r'(?<!\w)R\$\s*\d+(?:[.,]\d{1,2})?')
SECRET = re.compile(
    r'(?:sk-(?:proj-|live-)?[A-Za-z0-9_-]{20,}|'
    r'gh[pousr]_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|'
    r'xox[baprs]-[A-Za-z0-9-]{20,}|sk_live_[A-Za-z0-9]{20,}|'
    r'AIza[0-9A-Za-z_-]{30,}|-----BEGIN (?:RSA |EC )?PRIVATE KEY-----)'
)
PII_PATTERNS = {
    'cpf': re.compile(r'(?<!\d)\d{3}\.?\d{3}\.?\d{3}-?\d{2}(?!\d)'),
    'cnpj': re.compile(r'(?<!\d)\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}(?!\d)'),
    'email': re.compile(r'(?<![\w.+-])[\w.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![\w.-])'),
    'phone': re.compile(r'(?<!\d)(?:\+?55\s*)?(?:\(?\d{2}\)?[\s.-]*)?9?\d{4}[\s.-]?\d{4}(?!\d)'),
    'vehicle_plate': re.compile(r'(?<![A-Z0-9])[A-Z]{3}-?\d[A-Z0-9]\d{2}(?![A-Z0-9])', re.I),
}
ABSOLUTE = (
    'somos numero 1','numero um do mercado','resultado garantido','rendimento garantido',
    'aprovacao garantida','ganho garantido','risco zero','crescimento garantido',
    'dobre suas vendas','garantido','sem risco','guaranteed results','risk-free returns',
    'guaranteed cure','100% garantido'
)
OBJECTIVE_SUPERLATIVES = (
    'o melhor','a melhor','o mais barato','a mais barata','numero 1','nº 1','n° 1',
    'lider do mercado','lider de mercado','o unico','a unica','the best','number one',
    'market leader','the cheapest','the only'
)
PLACEHOLDER = re.compile(r'(?:\bR\$\s*(?:XX|X{2,})\b|\bX\s*%|\[(?:nome|cliente|preco|preço|valor|data)[^\]]*\])', re.I)
REFUSAL = re.compile(r'\b(?:nao posso ajudar|não posso ajudar|i can(?:not|\'t) help|i am unable to help)\b', re.I)


def finding(code, detail):
    identifier = hashlib.sha256((code + ':' + detail).encode('utf-8')).hexdigest()[:16]
    return {'id': identifier, 'code': code, 'detail': detail}


def normalize_text(value):
    value = unicodedata.normalize('NFKD', str(value)).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'\s+', ' ', value.casefold()).strip()


def _contains_term(content, term):
    norm_content = normalize_text(content)
    norm_term = normalize_text(term)
    if not norm_term:
        return False
    return re.search(r'(?<!\w)' + re.escape(norm_term) + r'(?!\w)', norm_content) is not None


def _term_rows(record, key):
    terms = record.get('terms', {}) if isinstance(record, dict) else {}
    values = terms.get(key, []) if isinstance(terms, dict) else []
    out = []
    for item in values:
        if isinstance(item, str):
            out.append({'term': item})
        elif isinstance(item, dict) and isinstance(item.get('term'), str):
            out.append(item)
    return out


def _redact(value):
    value = str(value)
    if len(value) <= 4:
        return '[redacted]'
    return value[:2] + '…' + value[-2:]


def format_warnings(task, content, requirements=None):
    """Ranges are editable heuristics, NOT platform limits. No language keyword gate."""
    if not isinstance(content, str):
        return []
    requirements = requirements or {}
    low, high = SUGGESTED_LENGTHS.get(task, (0, 10000))
    low = requirements.get('min_characters', low)
    high = requirements.get('max_characters', high)
    out = []
    if not low <= len(content) <= high:
        out.append(finding('length_suggestion', f'{len(content)} characters; suggested range {low}-{high}. Review the brief.'))
    limit = requirements.get('max_hashtags')
    if isinstance(limit, int) and len(re.findall(r'(?<!\w)#\w+', content)) > limit:
        out.append(finding('brief_hashtags', 'Hashtag count exceeds the explicit brief; review manually.'))
    if requirements.get('paragraphs_only') and re.search(r'^\s*(?:[-*] |\d+[.)] )', content, re.M):
        out.append(finding('brief_layout', 'A list may conflict with the requested prose format.'))
    return out


def assess_output(record, content, brands=(), task='instagram'):
    result = {'safety_errors': [], 'review_flags': [], 'format_warnings': []}
    if not isinstance(content, str) or not content.strip():
        result['safety_errors'].append(finding('missing_output', 'A nonempty text output is required.'))
        return result
    folded = normalize_text(content)
    if SECRET.search(content):
        result['safety_errors'].append(finding('possible_secret', 'Possible credential; remove it before any public export.'))
    if PLACEHOLDER.search(content):
        result['safety_errors'].append(finding('unresolved_placeholder', 'Unresolved placeholder found in publication text.'))
    if REFUSAL.search(content):
        result['safety_errors'].append(finding('assistant_refusal', 'Assistant refusal text must not be treated as publishable content.'))

    allowed_identifiers = [normalize_text(x) for x in record.get('allowed_public_identifiers', []) if isinstance(x, str)]
    for kind, pattern in PII_PATTERNS.items():
        for match in pattern.finditer(content):
            if normalize_text(match.group(0)) not in allowed_identifiers:
                result['safety_errors'].append(finding('possible_personal_data', f'Possible {kind} in public copy: {_redact(match.group(0))}'))

    voice = record.get('voice', {}) if isinstance(record.get('voice'), dict) else {}
    legacy_forbidden = list(record.get('forbidden_terms', [])) + list(voice.get('avoid_terms', []))
    for term in legacy_forbidden:
        if isinstance(term, str) and term.strip() and _contains_term(content, term):
            result['safety_errors'].append(finding('forbidden_term', 'Explicit brand restriction matched: ' + term))
    for row in _term_rows(record, 'dont_use'):
        if _contains_term(content, row['term']):
            detail = 'Brand term marked do-not-use: ' + row['term']
            if row.get('replacement'):
                detail += '; preferred replacement: ' + str(row['replacement'])
            result['safety_errors'].append(finding('brand_term_dont_use', detail))
    for key, code in (('use_carefully', 'brand_term_careful'), ('pending', 'brand_term_pending')):
        for row in _term_rows(record, key):
            if _contains_term(content, row['term']):
                result['review_flags'].append(finding(code, 'Review brand term: ' + row['term']))

    allowed = set(record.get('allowed_brand_mentions', []))
    for other in brands:
        name = other.get('display_name', '')
        if other.get('brand_id') != record.get('brand_id') and other.get('brand_id') not in allowed and name and name.casefold() in content.casefold():
            result['safety_errors'].append(finding('brand_leakage', 'Unapproved reference to ' + other.get('brand_id', name)))

    # Exact sourced statements are removed from generic claim heuristics. This is a declaration,
    # not independent verification of the evidence itself.
    unverified = content
    for claim in record.get('confirmed_claims', []):
        if isinstance(claim, dict) and isinstance(claim.get('text'), str) and claim['text'].strip() and claim.get('source'):
            unverified = unverified.replace(claim['text'], '')
    norm_unverified = normalize_text(unverified)
    for match in PERCENT.finditer(unverified):
        result['review_flags'].append(finding('unverified_percentage', 'Check source and context for ' + match.group(0) + '.'))
    for match in MULTIPLIER.finditer(unverified):
        result['review_flags'].append(finding('unverified_multiplier', 'Check source and context for ' + match.group(0) + '.'))
    for match in PRICE.finditer(unverified):
        result['review_flags'].append(finding('price_or_offer', 'Confirm price, validity and conditions for ' + match.group(0) + '.'))
    for term in ABSOLUTE:
        if normalize_text(term) in norm_unverified:
            result['review_flags'].append(finding('absolute_claim', 'Check evidence/context for phrase: ' + term))
    for term in OBJECTIVE_SUPERLATIVES:
        if normalize_text(term) in norm_unverified:
            result['review_flags'].append(finding('objective_superlative', 'Objective superiority claim needs evidence/context: ' + term))
    if any(_contains_term(unverified, term) for term in ('gratis', 'gratuito', 'free')):
        result['review_flags'].append(finding('free_claim', 'Confirm that the free/gratuitous claim has no undisclosed material condition.'))
    if re.search(r'[“\"](?:[^”\"]{8,})[”\"]\s*[-—]\s*[A-ZÁÉÍÓÚÂÊÔÃÕÇ]', unverified):
        result['review_flags'].append(finding('testimonial_or_quote', 'Confirm quoted testimonial/source and authorization before publication.'))

    if record.get('sponsorship_disclosure_required'):
        disclosure = ('#publi', '#publicidade')
        if not any(tag in content.casefold() for tag in disclosure):
            result['review_flags'].append(finding('sponsorship_disclosure', 'Sponsored/received content requires explicit disclosure review.'))

    result['format_warnings'] = format_warnings(task, content, record.get('format_requirements'))
    return result


def unresolved_review_flags(flags, decisions):
    """A declaration must resolve each exact flag with a rationale and source/context."""
    if not isinstance(decisions, list):
        decisions = []
    resolved = {
        d.get('id') for d in decisions if isinstance(d, dict)
        and d.get('decision') == 'accepted'
        and isinstance(d.get('reason'), str) and len(d['reason'].strip()) >= 8
        and isinstance(d.get('evidence'), str) and len(d['evidence'].strip()) >= 4
    }
    return [f for f in flags if f['id'] not in resolved]
