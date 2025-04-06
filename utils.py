from pymongo import MongoClient
from collections import defaultdict
import os

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.job_portal

def load_data():
    recruiters = list(db.recruiter_emails.find().sort("sent_at", -1))
    companies = list(db.companies.find())
    jobs = list(db.job_listings.find())
    return recruiters, companies, jobs

def compute_metrics(recruiters):
    stats = {
        "total": len(recruiters),
        "sent": sum(1 for r in recruiters if r.get("mail_send_success")),
        "failed": sum(1 for r in recruiters if not r.get("mail_send_success", True)),
        "followup": sum(1 for r in recruiters if r.get("followup")),
        "read": sum(1 for r in recruiters if r.get("read_status")),
        "by_company": defaultdict(int),
        "by_job": defaultdict(int)
    }

    for r in recruiters:
        company = db.companies.find_one({"_id": r["company"]["$id"]})
        job = db.job_listings.find_one({"company.$id": r["company"]["$id"]})
        if company:
            stats["by_company"][company["company_name"]] += 1
        if job:
            stats["by_job"][job["job_title"]] += 1

    return stats

def fetch_model_logs():
    return list(db.model_logs.find().sort("timestamp", -1))
