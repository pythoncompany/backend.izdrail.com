import logging
import json
import re

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import pandas as pd
from jobspy import scrape_jobs

# Initialize logger
logger = logging.getLogger(__name__)

router = APIRouter()


class ScanRequest(BaseModel):
    query: str


@router.post("/osint/scan/")
def perform_scan(scan_request: ScanRequest):
    url = 'https://osint.izdrail.com/startscan'
    headers = {
        'cookie': 'mobile-session-cookie-here',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'insomnia/10.0.0'
    }
    data = {
        'scanname': f"Mobile Osint App  {scan_request.query}",
        'scantarget': scan_request.query,
        'usecase': 'all',
        'modulelist': '',
        'typelist': ''
    }

    try:
        response = requests.post(url, headers=headers, data=data, allow_redirects=False)
        if response.status_code in [301, 303]:
            redirect_url = response.headers.get('Location')
            if not redirect_url:
                raise HTTPException(status_code=500, detail="Redirect URL not found")
            return {"redirectUrl": redirect_url}
        elif response.status_code == 200:
            html_content = response.text
            match = re.search(r'downloadLogs\("([A-Za-z0-9]+)"\)', html_content)
            if match:
                scan_id = match.group(1)
                return {"scanID": scan_id, "name": scan_request.domain}
            raise HTTPException(status_code=500, detail="Scan ID not found in HTML content")
        else:
            raise HTTPException(status_code=response.status_code, detail=f"HTTP error: {response.status_code}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
