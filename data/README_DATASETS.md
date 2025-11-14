# How to Add New Datasets

## Quick Guide

1. **Create a new JSON file** in the `data/` folder (e.g., `my_new_dataset.json`)

2. **Format your dataset** as a JSON array of log entries. Each entry should have:
   ```json
   {
     "timestamp": "2025-11-14T10:00:00Z",
     "source_ip": "192.168.1.100",
     "user": "username",
     "action": "login",
     "status": "success",
     "device": "device-name",
     "geo": "Location",
     "resource": "optional-resource-name",
     "bytes_transferred": 0
   }
   ```

3. **Save the file** - The dashboard will automatically detect it!

4. **Refresh the dashboard** - Your new dataset will appear in the dropdown menu

## Available Datasets

### Training Datasets (Large Scale)

- **dataset_1_brute_force.json** - ~1,256 entries focused on brute-force attacks
- **dataset_2_data_theft.json** - ~2,117 entries with data exfiltration scenarios
- **dataset_3_privilege_abuse.json** - ~2,012 entries with privilege escalation and admin abuse
- **dataset_4_comprehensive.json** - ~2,618 entries with mixed attack patterns
- **dataset_5_massive_training.json** - ~5,120 entries comprehensive training dataset

### Demo Dataset

- **sample_logs.json** - 13 entries complete demo with all detection types (quick test)

**Total Training Data: 13,000+ log entries across all datasets**

## Tips

- Use descriptive filenames (they'll be shown in the dropdown)
- Include enough events to trigger detections (5+ for brute-force, etc.)
- Timestamps should be in ISO format: `YYYY-MM-DDTHH:MM:SSZ`
- The system automatically counts events and shows them in the dropdown

