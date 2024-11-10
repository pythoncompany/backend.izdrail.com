import logging
import re
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests

# Initialize logger
logger = logging.getLogger(__name__)

router = APIRouter()

class ScanRequest(BaseModel):
    query: str
    url: Optional[str] = "https://osint.izdrail.com/startscan"


@router.post("/osint/scan/")
def perform_scan(scan_request: ScanRequest):
    url = scan_request.url
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
        if response.status_code in [301, 303, 200]:
            redirect_url = response.headers.get('Location')
            if redirect_url:
                match = re.search(r'id=([A-Za-z0-9]+)', redirect_url)
                if match:
                    return {"success": True, "scanID": match.group(1)}
                else:
                    raise HTTPException(status_code=500, detail="ID not found in redirect URL")
            else:
                raise HTTPException(status_code=500, detail="Redirect URL not found")
        else:
            raise HTTPException(status_code=response.status_code, detail=f"HTTP error: {response.status_code}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
