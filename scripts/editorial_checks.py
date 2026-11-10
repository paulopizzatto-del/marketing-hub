"""Mechanical checks, not a text-quality or language classifier.

Hard errors: malformed output, secrets, explicit brand restrictions, brand leakage.
Review flags: potentially unsupported numerical/absolute claims.
Format suggestions: warnings, never automatic rejection by length or keywords.
"""
from __future__ import annotations
import hashlib
import re

SUGGESTED_LENGTHS = {'instagram': (60, 2200), 'linkedin': (200, 3000), 'comment': (20, 600)}
PERCENT = re.compile(r'(?<!\w)(\d+(?:[.,]\d+)?)\s*%')
SECRET = re.compile(r'(?:sk-(?:proj-|live-)?[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |EC )?PRIVATE KEY-----)')
ABSOLUTE = ('somos n\u00famero 1','n\u00famero um do mercado','resultado garantido',
            'rendimento garantido','aprova\u00e7\u00e3o garantida','ganho garantido',
            'risco zero','crescimento garantido','dobre suas vendas',
            'guaranteed results','risk-free returns','guaranteed cure')

def finding(code, detail):
    identifier=hashlib.sha256((code+':'+detail).encode('utf-8')).hexdigest()[:16]
    return {'id':identifier,'code':code,'detail':detail}

def format_warnings(task, content, requirements=None):
    """Ranges are editable heuristics, NOT platform limits. No language keyword gate."""
    if not isinstance(content,str): return []
    requirements=requirements or {}
    low,high=SUGGESTED_LENGTHS.get(task,(0,10000))
    low=requirements.get('min_characters',low);high=requirements.get('max_characters',high)
    out=[]
    if not low <= len(content) <= high:
        out.append(finding('length_suggestion',f'{len(content)} characters; suggested range {low}-{high}. Review the brief.'))
    limit=requirements.get('max_hashtags')
    if isinstance(limit,int) and len(re.findall(r'(?<!\w)#\w+',content))>limit:
        out.append(finding('brief_hashtags','Hashtag count exceeds the explicit brief; review manually.'))
    if requirements.get('paragraphs_only') and re.search(r'^\s*(?:[-*] |\d+[.)] )',content,re.M):
        out.append(finding('brief_layout','A list may conflict with the requested prose format.'))
    return out

def assess_output(record, content, brands=(), task='instagram'):
    result={'safety_errors':[], 'review_flags':[], 'format_warnings':[]}
    if not isinstance(content,str) or not content.strip():
        result['safety_errors'].append(finding('missing_output','A nonempty text output is required.'));return result
    folded=content.casefold()
    if SECRET.search(content):
        result['safety_errors'].append(finding('possible_secret','Possible credential; remove it before any public export.'))
    forbidden=record.get('forbidden_terms',[])
    for term in forbidden:
        if isinstance(term,str) and term.strip() and term.casefold() in folded:
            result['safety_errors'].append(finding('forbidden_term','Explicit brand restriction matched: '+term))
    allowed=set(record.get('allowed_brand_mentions',[]))
    for other in brands:
        name=other.get('display_name','')
        if other.get('brand_id')!=record.get('brand_id') and other.get('brand_id') not in allowed and name and name.casefold() in folded:
            result['safety_errors'].append(finding('brand_leakage','Unapproved reference to '+other.get('brand_id',name)))
    # Only exact statements accompanied by a source in the task record are exempted.
    # This records evidence supplied by a reviewer, not verification of that source.
    unverified=content
    for claim in record.get('confirmed_claims',[]):
        if isinstance(claim,dict) and isinstance(claim.get('text'),str) and claim['text'].strip() and claim.get('source'):
            unverified=unverified.replace(claim['text'],'')
    for match in PERCENT.finditer(unverified):
        result['review_flags'].append(finding('unverified_percentage','Check source and context for '+match.group(0)+'. A percentage is not automatically a false claim.'))
    for term in ABSOLUTE:
        if term in unverified.casefold():
            result['review_flags'].append(finding('absolute_claim','Check context/evidence for phrase: '+term))
    result['format_warnings']=format_warnings(task,content,record.get('format_requirements'))
    return result

def unresolved_review_flags(flags, decisions):
    """A declaration must resolve each exact flag with a rationale and source/context."""
    if not isinstance(decisions,list): decisions=[]
    resolved={d.get('id') for d in decisions if isinstance(d,dict)
              and d.get('decision')=='accepted'
              and isinstance(d.get('reason'),str) and len(d['reason'].strip())>=8
              and isinstance(d.get('evidence'),str) and len(d['evidence'].strip())>=4}
    return [f for f in flags if f['id'] not in resolved]
