from fastapi import FastAPI
import requests
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "SEC Filings API is running!"}

@app.get("/download_filings")
def download_filings(cik: str, form_types: str = "10-K,10-Q,8-K"):
    headers = {'User-Agent': 'HM Asif (asif@osfdigital.com)'}  # SEC requires this
    
    cik_padded = cik.zfill(10)
    submissions_url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"
    
    response = requests.get(submissions_url, headers=headers)
    
    if response.status_code != 200:
        return {"error": f"Failed to get filings for {cik}"}

    company_data = response.json()
    
    filings = company_data['filings']['recent']
    form_list = form_types.split(",")
    
    downloaded_files = []

    for i in range(len(filings['form'])):
        form_type = filings['form'][i]
        if form_type not in form_list:
            continue
        
        accession_number = filings['accessionNumber'][i].replace('-', '')
        primary_doc = filings['primaryDocument'][i]
        filing_date = filings['filingDate'][i]
        
        doc_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession_number}/{primary_doc}"

        downloaded_files.append({
            "form_type": form_type,
            "filing_date": filing_date,
            "doc_url": doc_url
        })
    
    return {"message": f"Found {len(downloaded_files)} filings", "filings": downloaded_files}
