from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any
app=FastAPI(title='Scholarship Recommendation ML Service',version='1.0.0')
class RecommendationRequest(BaseModel):
    profile: dict[str,Any]={}
    scholarships: list[dict[str,Any]]=[]
def score(profile,s):
    interests={str(x).lower() for x in profile.get('interests',[])}
    tags={str(x).lower() for x in s.get('tags',[])}
    value=.55*len(interests&tags)/max(1,len(interests))
    e=s.get('eligibility',{})
    if profile.get('gpa') is not None and e.get('minGpa') is not None: value+=.25 if float(profile['gpa'])>=float(e['minGpa']) else 0
    if profile.get('income') is not None and e.get('maxIncome') is not None: value+=.20 if float(profile['income'])<=float(e['maxIncome']) else 0
    return round(min(1,value),4)
@app.get('/health')
def health(): return {'ok':True,'service':'ml-recommendation'}
@app.post('/recommend')
def recommend(req:RecommendationRequest):
    ranked=[{**s,'score':score(req.profile,s)} for s in req.scholarships]
    ranked.sort(key=lambda x:x['score'],reverse=True)
    return {'recommendations':ranked[:10]}
