#!/usr/bin/env python
"""
Vehicle Info API - Flask Version
Deployable on Vercel
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

BASE_URL = "https://api-ct.vehicleinfo.app/gw/plt/bffctsvc/api/v1/garage/rc-search"

HEADERS = {
    'User-Agent': "okhttp/4.12.0",
    'Accept': "application/json, text/plain, */*",
    'Accept-Encoding': "gzip",
    'authorization': "Bearer eyJhbGciOiJFUzI1NiIsImtpZCI6IjI2YjM0NDgwLWQ5ZDEtNDQ4NS1iYzczLTRiN2IxOGJiOWUyNCIsInR5cCI6IkpXVCJ9.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJjbGllbnRfWXVGVmVodWdxV2tOTkJLOTNIZ1Q0dyIsImV4cCI6MTc4OTkyMTIxNiwiZXh0Ijp7Imdyb3VwX2lkIjoiNThhNGQ5MzEtMTZhZi00MGY5LWI0ZmYtOGExNDU4YzA2ZjNkIiwic2Vzc2lvbl9pZCI6ImEyNWVhMWMxLTBiZTMtNDY2NS05MjIyLWMyOWNlZjM5M2Y5NiIsInVzZXJfdHlwZSI6IkVYVEVSTkFMIn0sImlhdCI6MTc4ODcxMTYxNSwiaXNzIjoiaHR0cHM6Ly9hdXRoLmNhcnMyNC5jb20vIiwianRpIjoiMDNlNDNhMzItOGU3Yy00ODRhLTlmYzktYTc1MjBlNmM1YjIyIiwibmJmIjoxNzg4NzExNjE1LCJzY3AiOlsib2ZmbGluZV9hY2Nlc3MiXSwic3ViIjoiNmY0YWQ5ZjktOGRiMy00NGVlLWFhNDUtZjJlM2Q1YTYxNmQxIn0.p96b8srL3ybB0lMC-B9HN-0lpsFr4q5kGgOTLbXpoK26wDwbOp4EY-b0SpcZdyJn8ysIqb5CbTzFQEY2Z4fE5g",
    'x-user-city-id': "777",
    'super_app_source': "vehicleinfo_consumerapp",
    'x-api-key': "c91f6a2e4b78d0c5a31b2f8d7e09c3fa",
    'x_app_instance_id': "547247478ea8e416185d98fbeb629954",
    'x-device-id': "547247478ea8e416185d98fbeb629954",
    'x-tenant-id': "VI_INDIA",
    'userid': "6f4ad9f9-8db3-44ee-aa45-f2e3d5a616d1",
    'x_experiment_id': "252935e1-2b91-4b74-9734-9a40037cd09f",
    'clientid': "vehicleinfo_consumerapp",
    'appversion': "323",
    'osname': "android",
    'useragent': "vehicleinfo_consumerapp/323",
    'source': "MobileApp",
    'x_country': "IN",
    'x-tenant-slug': "vehicleinfo"
}

def calculate_days_left(date_str):
    """Calculate days left from date string (YYYY-MM-DD)"""
    try:
        if not date_str:
            return None
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        diff = dt - datetime.now()
        return diff.days
    except:
        return None

def parse_date_fields(date_str, prefix):
    """Parse date string and return year, month, day dict"""
    result = {}
    try:
        if not date_str:
            return result
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        result[f"{prefix}_year"] = str(dt.year)
        result[f"{prefix}_month"] = f"{dt.month:02d}"
        result[f"{prefix}_day"] = f"{dt.day:02d}"
    except:
        pass
    return result

def extract_vehicle_info(raw_data):
    # Full structure with all keys
    result = {
        "registration": {
            "number": None,
            "date": None,
            "rto_code": None,
            "rto_name": None,
            "status": None,
            "expiry_date": None,
            "registered_place": None,
            "permanent_address": None,
            "registration_year": None,
            "registration_month": None,
            "registration_day": None
        },
        "owner": {
            "name": None,
            "ownership_type": None,
            "ownership_number": None,
            "masked_name": None,
            "full_name": None
        },
        "vehicle": {
            "manufacturer": None,
            "make_id": None,
            "model": None,
            "model_id": None,
            "variant": None,
            "variant_id": None,
            "color": None,
            "fuel_type": None,
            "emission_norm": None,
            "vehicle_class": None,
            "vehicle_category": None,
            "seating_capacity": None,
            "body_type": None,
            "transmission_type": None,
            "cubic_capacity": None,
            "cylinders": None,
            "gross_weight": None,
            "manufacturing_month_year": None,
            "manufacturing_month": None,
            "manufacturing_year": None,
            "vehicle_age": None,
            "variant_year": None,
            "model_image_url": "https://static-cdn.cars24.com/prod/cms/2025/02/26/106a22c8-b9bc-46bc-be9e-c9f9b2531602Group%2031%281%29%281%29%281%29%281%29%281%29.png",
            "vehicle_type": None,
            "is_bike": None
        },
        "identification": {
            "engine_number": None,
            "chassis_number": None,
            "engine_partial": None,
            "chassis_partial": None,
            "engine_full": None,
            "chassis_full": None
        },
        "insurance": {
            "company": None,
            "validity": None,
            "status": None,
            "days_left": None,
            "is_expired": None,
            "insurance_year": None,
            "insurance_month": None,
            "insurance_day": None
        },
        "fitness": {
            "valid_upto": None,
            "status": None,
            "days_left": None,
            "is_expired": None,
            "fitness_year": None,
            "fitness_month": None,
            "fitness_day": None
        },
        "pollution": {
            "pucc_number": None,
            "valid_upto": None,
            "status": None,
            "days_left": None,
            "is_expired": None,
            "pucc_year": None,
            "pucc_month": None,
            "pucc_day": None
        },
        "financier": {
            "name": None,
            "type": "Corporate",
            "financier_code": None
        },
        "challan": {
            "count": 0,
            "total_amount": 0,
            "status": "CLEAR",
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "pending_count": 0,
            "paid_count": 0,
            "challan_history": []
        },
        "additional": {
            "rc_summary_fetched_at": None
        }
    }

    # Safe navigation
    data_wrapper = raw_data.get("data", {})
    if not isinstance(data_wrapper, dict):
        data_wrapper = {}
    
    inner_data = data_wrapper.get("data", {})
    if not isinstance(inner_data, dict):
        inner_data = {}
    
    data_list = inner_data.get("data", [])
    if not isinstance(data_list, list):
        data_list = []

    for section in data_list:
        if not isinstance(section, dict):
            continue

        widget_key = section.get("widgetKey", "")
        section_data = section.get("data", {})
        if not isinstance(section_data, dict):
            section_data = {}

        if widget_key == "garage_header":
            header = section_data.get("titleHeaderProps", {})
            if isinstance(header, dict):
                result["registration"]["number"] = header.get("title")
                result["owner"]["masked_name"] = header.get("subTitle")

        elif widget_key == "ownership_details":
            items = section_data.get("items", [])
            if isinstance(items, list):
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    title = item.get("title", "")
                    val = item.get("subTitle")
                    if title == "Owner's name":
                        result["owner"]["name"] = val
                        result["owner"]["full_name"] = val
                    elif title == "Ownership":
                        result["owner"]["ownership_type"] = val
                        if val:
                            result["owner"]["ownership_number"] = val.split()[0] if val else None

        elif widget_key == "vehicle_details":
            items = section_data.get("items", [])
            if isinstance(items, list):
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    title = item.get("title", "").lower().replace(" ", "_")
                    val = item.get("subTitle")
                    if title == "manufacturer":
                        result["vehicle"]["manufacturer"] = val
                    elif title == "model":
                        result["vehicle"]["model"] = val
                    elif title == "variant":
                        result["vehicle"]["variant"] = val
                    elif title == "fuel_type":
                        result["vehicle"]["fuel_type"] = val
                    elif title == "emission_norm":
                        result["vehicle"]["emission_norm"] = val
                    elif title == "class":
                        result["vehicle"]["vehicle_class"] = val
                    elif title == "seating_capacity":
                        result["vehicle"]["seating_capacity"] = val
                    elif title == "rc_status":
                        badge = item.get("badge", {})
                        if isinstance(badge, dict):
                            result["registration"]["status"] = badge.get("text")
                    elif title == "financier_name":
                        result["financier"]["name"] = val

        elif widget_key == "under_the_hood":
            items = section_data.get("items", [])
            if isinstance(items, list):
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    title = item.get("title", "").lower()
                    val = item.get("subTitle")
                    if "engine" in title:
                        result["identification"]["engine_number"] = val
                        result["identification"]["engine_full"] = val
                        if val and len(val) > 4:
                            result["identification"]["engine_partial"] = val[:-4]
                    elif "chassis" in title:
                        result["identification"]["chassis_number"] = val
                        result["identification"]["chassis_full"] = val
                        if val and len(val) > 4:
                            result["identification"]["chassis_partial"] = val[:-4]
                    elif "cubic" in title:
                        if val:
                            result["vehicle"]["cubic_capacity"] = f"{val} CC"
                    elif "cylinder" in title:
                        result["vehicle"]["cylinders"] = val

        elif widget_key == "important_dates":
            items = section_data.get("items", [])
            if isinstance(items, list):
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    title = item.get("title", "").lower()
                    val = item.get("subTitle")
                    if "age" in title:
                        result["vehicle"]["vehicle_age"] = val
                    elif "registration" in title:
                        result["registration"]["date"] = val
                        if val:
                            try:
                                dt = datetime.strptime(val, "%d %B %Y")
                                result["registration"]["registration_year"] = str(dt.year)
                                result["registration"]["registration_month"] = f"{dt.month:02d}"
                                result["registration"]["registration_day"] = f"{dt.day:02d}"
                            except:
                                pass
                    elif "fitness" in title:
                        result["fitness"]["valid_upto"] = val
                        if val:
                            try:
                                dt = datetime.strptime(val, "%d %B %Y")
                                ymd = dt.strftime("%Y-%m-%d")
                                result["fitness"]["valid_upto"] = ymd
                                days = calculate_days_left(ymd)
                                result["fitness"]["days_left"] = days
                                result["fitness"]["is_expired"] = days < 0 if days is not None else None
                                result["fitness"]["status"] = "Expired" if days is not None and days < 0 else "Active"
                                result["fitness"]["fitness_year"] = str(dt.year)
                                result["fitness"]["fitness_month"] = f"{dt.month:02d}"
                                result["fitness"]["fitness_day"] = f"{dt.day:02d}"
                            except:
                                pass
                    elif "insurance" in title:
                        result["insurance"]["validity"] = val
                        if val:
                            try:
                                dt = datetime.strptime(val, "%d %B %Y")
                                ymd = dt.strftime("%Y-%m-%d")
                                result["insurance"]["validity"] = ymd
                                days = calculate_days_left(ymd)
                                result["insurance"]["days_left"] = days
                                result["insurance"]["is_expired"] = days < 0 if days is not None else None
                                result["insurance"]["status"] = "Expired" if days is not None and days < 0 else "Active"
                                result["insurance"]["insurance_year"] = str(dt.year)
                                result["insurance"]["insurance_month"] = f"{dt.month:02d}"
                                result["insurance"]["insurance_day"] = f"{dt.day:02d}"
                            except:
                                pass
                    elif "pollution" in title:
                        result["pollution"]["valid_upto"] = val
                        if val:
                            try:
                                dt = datetime.strptime(val, "%d %B %Y")
                                ymd = dt.strftime("%Y-%m-%d")
                                result["pollution"]["valid_upto"] = ymd
                                days = calculate_days_left(ymd)
                                result["pollution"]["days_left"] = days
                                result["pollution"]["is_expired"] = days < 0 if days is not None else None
                                result["pollution"]["status"] = "Expired" if days is not None and days < 0 else "Active"
                                result["pollution"]["pucc_year"] = str(dt.year)
                                result["pollution"]["pucc_month"] = f"{dt.month:02d}"
                                result["pollution"]["pucc_day"] = f"{dt.day:02d}"
                            except:
                                pass
                    elif "rc expiry" in title:
                        result["registration"]["expiry_date"] = val
                        if val:
                            try:
                                dt = datetime.strptime(val, "%d %B %Y")
                                result["registration"]["expiry_date"] = dt.strftime("%Y-%m-%d")
                            except:
                                pass

        elif widget_key == "garage_alerts_list":
            items = section_data.get("items", [])
            if isinstance(items, list):
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    if "challan" in item.get("heading", "").lower():
                        result["challan"]["status"] = "CLEAR"
                        result["challan"]["count"] = 0
                        result["challan"]["total_amount"] = 0
                        result["challan"]["pending_count"] = 0
                        result["challan"]["paid_count"] = 0
                        result["challan"]["challan_history"] = []
                        result["challan"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")

    # rc_summary se missing fields
    debug = raw_data.get("debug", {})
    if isinstance(debug, dict):
        garage360 = debug.get("garageVehicle360", {})
        if isinstance(garage360, dict):
            detail = garage360.get("detail", {})
            if isinstance(detail, dict):
                rc_summary = detail.get("rc_summary", {})
                if isinstance(rc_summary, dict):
                    # Vehicle
                    result["vehicle"]["manufacturer"] = result["vehicle"]["manufacturer"] or rc_summary.get("make_name")
                    result["vehicle"]["make_id"] = rc_summary.get("make_id")
                    result["vehicle"]["model"] = result["vehicle"]["model"] or rc_summary.get("model_name")
                    result["vehicle"]["model_id"] = rc_summary.get("model_id")
                    result["vehicle"]["variant"] = result["vehicle"]["variant"] or rc_summary.get("variant_name")
                    result["vehicle"]["variant_id"] = rc_summary.get("variant_id")
                    result["vehicle"]["variant_year"] = rc_summary.get("variant_year")
                    result["vehicle"]["fuel_type"] = result["vehicle"]["fuel_type"] or rc_summary.get("fuel_type")
                    result["vehicle"]["emission_norm"] = result["vehicle"]["emission_norm"] or rc_summary.get("emission_norm")
                    result["vehicle"]["vehicle_class"] = result["vehicle"]["vehicle_class"] or rc_summary.get("vehicle_class")
                    result["vehicle"]["vehicle_category"] = rc_summary.get("vehicle_category")
                    result["vehicle"]["seating_capacity"] = result["vehicle"]["seating_capacity"] or str(rc_summary.get("seat_capacity", ""))
                    result["vehicle"]["color"] = rc_summary.get("vehicle_color")
                    result["vehicle"]["body_type"] = rc_summary.get("body_type")
                    result["vehicle"]["transmission_type"] = rc_summary.get("transmission_type")
                    if rc_summary.get("cubic_capacity"):
                        result["vehicle"]["cubic_capacity"] = result["vehicle"]["cubic_capacity"] or f"{rc_summary.get('cubic_capacity')} CC"
                    result["vehicle"]["cylinders"] = result["vehicle"]["cylinders"] or str(rc_summary.get("cylinders_no", ""))
                    if rc_summary.get("gross_vehicle_weight"):
                        result["vehicle"]["gross_weight"] = f"{rc_summary.get('gross_vehicle_weight')} KG"
                    result["vehicle"]["manufacturing_month_year"] = rc_summary.get("manufacturer_month_year")
                    if rc_summary.get("manufacturer_month_year"):
                        try:
                            parts = rc_summary.get("manufacturer_month_year").split("/")
                            if len(parts) == 2:
                                result["vehicle"]["manufacturing_month"] = parts[0]
                                result["vehicle"]["manufacturing_year"] = parts[1]
                        except:
                            pass
                    result["vehicle"]["vehicle_type"] = "Two Wheeler" if rc_summary.get("vehicle_category") == "2WN" else "Four Wheeler"
                    result["vehicle"]["is_bike"] = rc_summary.get("vehicle_category") == "2WN"
                    
                    # Registration
                    result["registration"]["rto_code"] = rc_summary.get("rto_code")
                    result["registration"]["rto_name"] = rc_summary.get("rto_name")
                    result["registration"]["registered_place"] = rc_summary.get("rto_name")
                    result["registration"]["permanent_address"] = rc_summary.get("rto_name")
                    if not result["registration"]["date"]:
                        result["registration"]["date"] = rc_summary.get("registration_date")
                    if not result["registration"]["expiry_date"]:
                        result["registration"]["expiry_date"] = rc_summary.get("rc_expiry_date")
                    if not result["registration"]["status"]:
                        result["registration"]["status"] = rc_summary.get("rc_status")
                    
                    # Financier
                    result["financier"]["name"] = result["financier"]["name"] or rc_summary.get("financer")
                    
                    # Insurance
                    result["insurance"]["company"] = result["insurance"]["company"] or rc_summary.get("insurance_company")
                    if not result["insurance"]["validity"]:
                        result["insurance"]["validity"] = rc_summary.get("insurance_expiry")
                        if result["insurance"]["validity"]:
                            days = calculate_days_left(result["insurance"]["validity"])
                            result["insurance"]["days_left"] = days
                            result["insurance"]["is_expired"] = days < 0 if days is not None else None
                            result["insurance"]["status"] = "Expired" if days is not None and days < 0 else "Active"
                            date_parts = parse_date_fields(result["insurance"]["validity"], "insurance")
                            result["insurance"]["insurance_year"] = date_parts.get("insurance_year")
                            result["insurance"]["insurance_month"] = date_parts.get("insurance_month")
                            result["insurance"]["insurance_day"] = date_parts.get("insurance_day")
                    
                    # Fitness
                    if not result["fitness"]["valid_upto"]:
                        result["fitness"]["valid_upto"] = rc_summary.get("fitness_upto")
                        if result["fitness"]["valid_upto"]:
                            days = calculate_days_left(result["fitness"]["valid_upto"])
                            result["fitness"]["days_left"] = days
                            result["fitness"]["is_expired"] = days < 0 if days is not None else None
                            result["fitness"]["status"] = "Expired" if days is not None and days < 0 else "Active"
                            date_parts = parse_date_fields(result["fitness"]["valid_upto"], "fitness")
                            result["fitness"]["fitness_year"] = date_parts.get("fitness_year")
                            result["fitness"]["fitness_month"] = date_parts.get("fitness_month")
                            result["fitness"]["fitness_day"] = date_parts.get("fitness_day")
                    
                    # Pollution
                    result["pollution"]["pucc_number"] = rc_summary.get("pucc_number")
                    if not result["pollution"]["valid_upto"]:
                        result["pollution"]["valid_upto"] = rc_summary.get("pucc_expiry")
                        if result["pollution"]["valid_upto"]:
                            days = calculate_days_left(result["pollution"]["valid_upto"])
                            result["pollution"]["days_left"] = days
                            result["pollution"]["is_expired"] = days < 0 if days is not None else None
                            result["pollution"]["status"] = "Expired" if days is not None and days < 0 else "Active"
                            date_parts = parse_date_fields(result["pollution"]["valid_upto"], "pucc")
                            result["pollution"]["pucc_year"] = date_parts.get("pucc_year")
                            result["pollution"]["pucc_month"] = date_parts.get("pucc_month")
                            result["pollution"]["pucc_day"] = date_parts.get("pucc_day")
                    
                    # Additional
                    result["additional"]["rc_summary_fetched_at"] = rc_summary.get("fetched_at")
                    
                    # Owner name from rc_owner_name if available
                    if not result["owner"]["name"]:
                        result["owner"]["name"] = detail.get("rc_owner_name")
                        result["owner"]["full_name"] = detail.get("rc_owner_name")

    return result

def fetch_vehicle_info(registration_number):
    params = {'registration_number': registration_number}
    try:
        resp = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=15)
        return resp.status_code, resp.json() if resp.text else {}
    except Exception as e:
        return 500, {"error": str(e)}

@app.route("/")
def home():
    return jsonify({
        "name": "Vehicle Info API",
        "version": "2.0",
        "developer": "ARHAN (ANONYMOUS)",
        "endpoint": "/vehicleinfo?rc=<registration_number>",
        "example": "http://127.0.0.1:5000/vehicleinfo?rc=JH05DE7988"
    })

@app.route("/vehicleinfo", methods=["GET"])
def vehicle_info():
    start_time = time.time()
    reg_no = request.args.get("rc", "").upper().strip()
    
    if not reg_no or len(reg_no) < 6:
        return jsonify({
            "success": False,
            "response_time_seconds": round(time.time() - start_time, 2),
            "error": "Valid registration number required",
            "developer": "ARHAN (ANONYMOUS)"
        }), 400
    
    status_code, raw_data = fetch_vehicle_info(reg_no)
    
    if status_code != 200:
        return jsonify({
            "success": False,
            "response_time_seconds": round(time.time() - start_time, 2),
            "error": raw_data.get("error", "Failed to fetch vehicle info"),
            "status_code": status_code,
            "developer": "ARHAN (ANONYMOUS)"
        }), status_code
    
    try:
        extracted = extract_vehicle_info(raw_data)
        return jsonify({
            "success": True,
            "response_time_seconds": round(time.time() - start_time, 2),
            "data": extracted,
            "developer": "ARHAN (ANONYMOUS)"
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "response_time_seconds": round(time.time() - start_time, 2),
            "error": f"Parsing error: {str(e)}",
            "developer": "ARHAN (ANONYMOUS)"
        }), 500

# Vercel handler
def handler(event, context):
    return app(event, context)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))