"""
Generate large realistic cybersecurity training datasets for SentinelForge
"""
import json
import random
from datetime import datetime, timedelta

# Configuration
USERS = ["alice", "bob", "charlie", "diana", "ed", "frank", "grace", "henry", "iris", "jack", 
         "kate", "liam", "maya", "noah", "olivia", "peter", "quinn", "rachel", "sam", "tina",
         "victor", "wanda", "xavier", "yara", "zoe", "admin", "service-account", "intern"]

DEVICES = ["corp-laptop-{}", "workstation-{}", "vpn-gateway", "home-laptop", "mobile-device-{}",
           "server-{}", "admin-workstation", "lab-computer-{}", "finance-vdi", "dev-vm-{}"]

LOCATIONS = ["Bangalore", "Mumbai", "Delhi", "Hyderabad", "Chennai", "Pune", "Kolkata",
             "Singapore", "London", "New York", "Paris", "Tokyo", "Sydney", "Dubai"]

ACTIONS = ["login", "download", "upload", "config_change", "privilege_escalation", "file_access"]

SENSITIVE_RESOURCES = ["customer-database.sql", "payroll-data.xlsx", "genome-dataset.tar.gz",
                       "quarterly-reports.zip", "financial-records.db", "user-credentials.json",
                       "firewall-policy", "backup-archive.tar", "research-data.zip"]

def random_ip():
    return f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"

def random_timestamp(start_date, end_date):
    delta = end_date - start_date
    seconds = random.randint(0, int(delta.total_seconds()))
    return start_date + timedelta(seconds=seconds)

def generate_brute_force_dataset(num_entries=800):
    """Generate dataset with multiple brute-force attack patterns"""
    entries = []
    base_date = datetime(2025, 11, 14, 8, 0, 0)
    
    # Normal activity (60%)
    for _ in range(int(num_entries * 0.6)):
        user = random.choice(USERS)
        entries.append({
            "timestamp": random_timestamp(base_date, base_date + timedelta(hours=8)).isoformat() + "Z",
            "source_ip": random_ip(),
            "user": user,
            "action": "login",
            "status": random.choice(["success", "failed"]),
            "device": random.choice(DEVICES).format(random.randint(1, 50)),
            "geo": random.choice(LOCATIONS)
        })
    
    # Brute-force attacks (40%)
    attack_users = random.sample(USERS, 5)
    for user in attack_users:
        attack_ip = random_ip()
        attack_start = random_timestamp(base_date, base_date + timedelta(hours=6))
        # Generate 8-15 failed attempts in quick succession
        for i in range(random.randint(8, 15)):
            entries.append({
                "timestamp": (attack_start + timedelta(seconds=i*15)).isoformat() + "Z",
                "source_ip": attack_ip,
                "user": user,
                "action": "login",
                "status": "failed",
                "device": random.choice(DEVICES).format(random.randint(1, 20)),
                "geo": random.choice(LOCATIONS)
            })
    
    # Sort by timestamp
    entries.sort(key=lambda x: x["timestamp"])
    return entries

def generate_data_exfiltration_dataset(num_entries=1200):
    """Generate dataset with data exfiltration patterns"""
    entries = []
    base_date = datetime(2025, 11, 14, 9, 0, 0)
    
    # Normal activity (70%)
    for _ in range(int(num_entries * 0.7)):
        user = random.choice(USERS)
        action = random.choice(["login", "download", "upload", "file_access"])
        entry = {
            "timestamp": random_timestamp(base_date, base_date + timedelta(hours=12)).isoformat() + "Z",
            "source_ip": random_ip(),
            "user": user,
            "action": action,
            "status": "success",
            "device": random.choice(DEVICES).format(random.randint(1, 50)),
            "geo": random.choice(LOCATIONS)
        }
        if action == "download":
            entry["resource"] = f"document-{random.randint(1, 100)}.pdf"
            entry["bytes_transferred"] = random.randint(1024, 50 * 1024 * 1024)
        entries.append(entry)
    
    # Data exfiltration attacks (30%)
    malicious_users = random.sample(USERS, 3)
    for user in malicious_users:
        attack_start = random_timestamp(base_date, base_date + timedelta(hours=10))
        # Login first
        entries.append({
            "timestamp": attack_start.isoformat() + "Z",
            "source_ip": random_ip(),
            "user": user,
            "action": "login",
            "status": "success",
            "device": "compromised-laptop",
            "geo": random.choice(LOCATIONS)
        })
        # Then large downloads
        for i in range(random.randint(3, 8)):
            entries.append({
                "timestamp": (attack_start + timedelta(minutes=i*5)).isoformat() + "Z",
                "source_ip": random_ip(),
                "user": user,
                "action": "download",
                "status": "success",
                "device": "compromised-laptop",
                "resource": random.choice(SENSITIVE_RESOURCES),
                "bytes_transferred": random.randint(250 * 1024 * 1024, 2 * 1024 * 1024 * 1024),
                "geo": random.choice(LOCATIONS)
            })
    
    entries.sort(key=lambda x: x["timestamp"])
    return entries

def generate_privilege_abuse_dataset(num_entries=1000):
    """Generate dataset with privilege abuse patterns"""
    entries = []
    base_date = datetime(2025, 11, 14, 0, 0, 0)
    admin_users = ["admin", "charlie", "diana", "root"]
    
    # Normal activity (65%)
    for _ in range(int(num_entries * 0.65)):
        user = random.choice(USERS)
        action = random.choice(["login", "file_access", "download"])
        entry = {
            "timestamp": random_timestamp(base_date, base_date + timedelta(hours=24)).isoformat() + "Z",
            "source_ip": random_ip(),
            "user": user,
            "action": action,
            "status": "success",
            "device": random.choice(DEVICES).format(random.randint(1, 50)),
            "geo": random.choice(LOCATIONS)
        }
        if action == "download":
            entry["resource"] = f"file-{random.randint(1, 200)}.pdf"
            entry["bytes_transferred"] = random.randint(1024, 100 * 1024 * 1024)
        entries.append(entry)
    
    # After-hours admin activity (20%)
    for admin in admin_users:
        for _ in range(random.randint(2, 5)):
            # Late night or early morning
            hour = random.choice([0, 1, 2, 3, 4, 5, 22, 23])
            attack_time = base_date.replace(hour=hour, minute=random.randint(0, 59))
            entries.append({
                "timestamp": attack_time.isoformat() + "Z",
                "source_ip": random_ip(),
                "user": admin,
                "action": "login",
                "status": "success",
                "device": "admin-workstation",
                "geo": random.choice(LOCATIONS)
            })
    
    # Unauthorized privilege actions (15%)
    non_admin_users = [u for u in USERS if u not in admin_users]
    for _ in range(int(num_entries * 0.15)):
        user = random.choice(non_admin_users)
        attack_time = random_timestamp(base_date, base_date + timedelta(hours=24))
        entries.append({
            "timestamp": attack_time.isoformat() + "Z",
            "source_ip": random_ip(),
            "user": user,
            "action": random.choice(["config_change", "privilege_escalation"]),
            "status": "success",
            "device": random.choice(DEVICES).format(random.randint(1, 20)),
            "resource": random.choice(["firewall-policy", "user-permissions", "system-config"]),
            "geo": random.choice(LOCATIONS)
        })
    
    entries.sort(key=lambda x: x["timestamp"])
    return entries

def generate_comprehensive_dataset(num_entries=2000):
    """Generate comprehensive dataset with all attack types"""
    entries = []
    base_date = datetime(2025, 11, 14, 0, 0, 0)
    
    # Normal baseline activity (50%)
    for _ in range(int(num_entries * 0.5)):
        user = random.choice(USERS)
        action = random.choice(["login", "download", "upload", "file_access"])
        entry = {
            "timestamp": random_timestamp(base_date, base_date + timedelta(hours=24)).isoformat() + "Z",
            "source_ip": random_ip(),
            "user": user,
            "action": action,
            "status": random.choice(["success", "failed"]),
            "device": random.choice(DEVICES).format(random.randint(1, 100)),
            "geo": random.choice(LOCATIONS)
        }
        if action == "download":
            entry["resource"] = f"document-{random.randint(1, 500)}.pdf"
            entry["bytes_transferred"] = random.randint(1024, 100 * 1024 * 1024)
        entries.append(entry)
    
    # Brute-force attacks (15%)
    for _ in range(8):
        user = random.choice(USERS)
        attack_ip = random_ip()
        attack_start = random_timestamp(base_date, base_date + timedelta(hours=20))
        for i in range(random.randint(6, 12)):
            entries.append({
                "timestamp": (attack_start + timedelta(seconds=i*20)).isoformat() + "Z",
                "source_ip": attack_ip,
                "user": user,
                "action": "login",
                "status": "failed",
                "device": random.choice(DEVICES).format(random.randint(1, 30)),
                "geo": random.choice(LOCATIONS)
            })
    
    # Impossible travel (10%)
    travel_users = random.sample(USERS, 4)
    for user in travel_users:
        loc1, loc2 = random.sample(LOCATIONS, 2)
        time1 = random_timestamp(base_date, base_date + timedelta(hours=18))
        time2 = time1 + timedelta(minutes=random.randint(5, 45))
        entries.append({
            "timestamp": time1.isoformat() + "Z",
            "source_ip": random_ip(),
            "user": user,
            "action": "login",
            "status": "success",
            "device": "vpn-gateway",
            "geo": loc1
        })
        entries.append({
            "timestamp": time2.isoformat() + "Z",
            "source_ip": random_ip(),
            "user": user,
            "action": "login",
            "status": "success",
            "device": "vpn-gateway",
            "geo": loc2
        })
    
    # Data exfiltration (15%)
    for _ in range(5):
        user = random.choice(USERS)
        attack_start = random_timestamp(base_date, base_date + timedelta(hours=20))
        entries.append({
            "timestamp": attack_start.isoformat() + "Z",
            "source_ip": random_ip(),
            "user": user,
            "action": "login",
            "status": "success",
            "device": "compromised-device",
            "geo": random.choice(LOCATIONS)
        })
        for i in range(random.randint(3, 6)):
            entries.append({
                "timestamp": (attack_start + timedelta(minutes=i*3)).isoformat() + "Z",
                "source_ip": random_ip(),
                "user": user,
                "action": "download",
                "status": "success",
                "device": "compromised-device",
                "resource": random.choice(SENSITIVE_RESOURCES),
                "bytes_transferred": random.randint(300 * 1024 * 1024, 3 * 1024 * 1024 * 1024),
                "geo": random.choice(LOCATIONS)
            })
    
    # Privilege abuse (10%)
    admin_users = ["admin", "charlie", "diana"]
    for admin in admin_users:
        for _ in range(random.randint(2, 4)):
            hour = random.choice([0, 1, 2, 3, 22, 23])
            attack_time = base_date.replace(hour=hour, minute=random.randint(0, 59))
            entries.append({
                "timestamp": attack_time.isoformat() + "Z",
                "source_ip": random_ip(),
                "user": admin,
                "action": "login",
                "status": "success",
                "device": "admin-workstation",
                "geo": random.choice(LOCATIONS)
            })
    
    non_admin = [u for u in USERS if u not in admin_users]
    for _ in range(6):
        user = random.choice(non_admin)
        attack_time = random_timestamp(base_date, base_date + timedelta(hours=24))
        entries.append({
            "timestamp": attack_time.isoformat() + "Z",
            "source_ip": random_ip(),
            "user": user,
            "action": random.choice(["config_change", "privilege_escalation"]),
            "status": "success",
            "device": random.choice(DEVICES).format(random.randint(1, 20)),
            "resource": random.choice(["firewall-policy", "user-permissions"]),
            "geo": random.choice(LOCATIONS)
        })
    
    entries.sort(key=lambda x: x["timestamp"])
    return entries

if __name__ == "__main__":
    print("Generating large training datasets for cybersecurity project...")
    
    print("  Generating brute-force dataset (2000 entries)...")
    dataset1 = generate_brute_force_dataset(2000)
    with open("data/dataset_1_brute_force.json", "w", encoding="utf-8") as f:
        json.dump(dataset1, f, indent=2)
    print(f"    Created with {len(dataset1)} entries")
    
    print("  Generating data exfiltration dataset (3000 entries)...")
    dataset2 = generate_data_exfiltration_dataset(3000)
    with open("data/dataset_2_data_theft.json", "w", encoding="utf-8") as f:
        json.dump(dataset2, f, indent=2)
    print(f"    Created with {len(dataset2)} entries")
    
    print("  Generating privilege abuse dataset (2500 entries)...")
    dataset3 = generate_privilege_abuse_dataset(2500)
    with open("data/dataset_3_privilege_abuse.json", "w", encoding="utf-8") as f:
        json.dump(dataset3, f, indent=2)
    print(f"    Created with {len(dataset3)} entries")
    
    print("  Generating comprehensive training dataset (5000 entries)...")
    dataset4 = generate_comprehensive_dataset(5000)
    with open("data/dataset_4_comprehensive.json", "w", encoding="utf-8") as f:
        json.dump(dataset4, f, indent=2)
    print(f"    Created with {len(dataset4)} entries")
    
    print("  Generating massive training dataset (10000 entries)...")
    dataset5 = generate_comprehensive_dataset(10000)
    with open("data/dataset_5_massive_training.json", "w", encoding="utf-8") as f:
        json.dump(dataset5, f, indent=2)
    print(f"    Created with {len(dataset5)} entries")
    
    print("\nAll datasets generated successfully!")
    total = len(dataset1) + len(dataset2) + len(dataset3) + len(dataset4) + len(dataset5)
    print(f"  Total entries across all datasets: {total}")
    print(f"  Average entries per dataset: {total // 5}")

