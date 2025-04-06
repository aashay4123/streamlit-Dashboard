from bson import ObjectId, DBRef
from pymongo import MongoClient
from collections import defaultdict
import os


MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.get_database("job_hunt")


def load_data():
    recruiters = list(db.recruiter_emails.find())
    companies = list(db.companies.find())
    jobs = list(db.job_listings.find())
    return recruiters, companies, jobs


# def compute_metrics(recruiters):
#     stats = {
#         "total": len(recruiters),
#         "sent": sum(1 for r in recruiters if r.get("mail_send_success")),
#         "failed": sum(1 for r in recruiters if not r.get("mail_send_success", True)),
#         "followup": sum(1 for r in recruiters if r.get("followup")),
#         "read": sum(1 for r in recruiters if r.get("read_status")),
#         "by_company": defaultdict(int),
#         "by_job": defaultdict(int)
#     }

#     for r in recruiters:
#         try:
#             company = db.companies.find_one({"_id": r["company"]["$id"]})
#             job = db.job_listings.find_one(
#                 {"company.$id": r["company"]["$id"]})
#             if company:
#                 stats["by_company"][company["company_name"]] += 1
#             if job:
#                 stats["by_job"][job["job_title"]] += 1
#         except:
#             continue
#     return stats

def compute_metrics(recruiters):
    stats = {
        "total": len(recruiters),
        "sent": 0,
        "failed": 0,
        "followup": 0,
        "read": 0,
        "by_company": defaultdict(int),
        "by_job": defaultdict(int)
    }

    for r in recruiters:
        if r.get("mail_send_success") is True:
            stats["sent"] += 1
        elif r.get("mail_send_success") is False:
            stats["failed"] += 1

        if r.get("followup"):
            stats["followup"] += 1
        if r.get("read_status"):
            stats["read"] += 1

        try:
            company_ref = r.get("company")
            if isinstance(company_ref, DBRef):
                company_id = company_ref.id
                company = db.companies.find_one({"_id": company_id})
                if company:
                    stats["by_company"][company.get(
                        "company_name", "Unknown")] += 1

                job = db.job_listings.find_one({"company": company_id})
                if job:
                    stats["by_job"][job.get("job_title", "Unknown")] += 1
        except Exception as e:
            print("⚠️ Skipped recruiter (company/job lookup failed):", e)

    return stats
