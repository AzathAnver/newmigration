import re
import csv
from collections import defaultdict
from datetime import datetime

def analyze_log_file(log_file_path):
    """
    Analyze the log file and generate a summary report.
    """
    
    # Track row data
    row_data = defaultdict(lambda: {
        'group': None,
        'user': None,
        'status': None,
        'reason': None,
        'fragment_search': False,
        'fragment_username': None,
        'matched_email': None,
        'group_id': None
    })
    
    # Track success events that need to be matched
    success_events = []
    
    # Read log file
    with open(log_file_path, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Pattern 1: Processing Row
        match = re.search(r"Processing Row (\d+): Group='([^']*)', User='([^']*)'", line)
        if match:
            row_num = int(match.group(1))
            row_data[row_num]['group'] = match.group(2)
            row_data[row_num]['user'] = match.group(3)
            continue
        
        # Pattern 2: Group not found
        match = re.search(r"Row (\d+): Group '([^']*)' not found", line)
        if match:
            row_num = int(match.group(1))
            row_data[row_num]['status'] = 'FAILED'
            row_data[row_num]['reason'] = 'Group not found'
            continue
        
        # Pattern 3: Searching users by username fragment
        match = re.search(r"Row (\d+): Searching users by username fragment: '([^']*)'", line)
        if match:
            row_num = int(match.group(1))
            row_data[row_num]['fragment_search'] = True
            row_data[row_num]['fragment_username'] = match.group(2)
            continue
        
        # Pattern 4: Found potential match
        match = re.search(r"Row (\d+): Found potential match: (\S+)", line)
        if match:
            row_num = int(match.group(1))
            row_data[row_num]['matched_email'] = match.group(2)
            continue
        
        # Pattern 5: No users found
        match = re.search(r"Row (\d+): No users found for username '([^']*)'", line)
        if match:
            row_num = int(match.group(1))
            row_data[row_num]['status'] = 'FAILED'
            row_data[row_num]['reason'] = 'User not found'
            continue
        
        # Pattern 6: WARNING No users
        match = re.search(r"WARNING: Row (\d+): No users for (\S+) in group (\S+)", line)
        if match:
            row_num = int(match.group(1))
            row_data[row_num]['status'] = 'FAILED'
            row_data[row_num]['reason'] = 'User not found'
            row_data[row_num]['group_id'] = match.group(3)
            continue
        
        # Pattern 7: Successfully assigned (in INFO log)
        match = re.search(r"Successfully assigned (\S+) to group (\S+)", line)
        if match:
            success_events.append({
                'email': match.group(1),
                'group_id': match.group(2),
                'matched': False
            })
            continue
        
        # Pattern 8: SUCCESS: line
        match = re.search(r"SUCCESS: (\S+) -> (\S+)", line)
        if match:
            success_events.append({
                'email': match.group(1),
                'group_id': match.group(2),
                'matched': False
            })
            continue
    
    # Now match success events to rows
    # First try: match by matched_email
    for event in success_events:
        if event['matched']:
            continue
        for rn, data in row_data.items():
            if data['matched_email'] == event['email'] and data['status'] is None:
                row_data[rn]['status'] = 'SUCCESS'
                row_data[rn]['group_id'] = event['group_id']
                row_data[rn]['reason'] = ''
                event['matched'] = True
                break
    
    # Second try: match by username part of input email to success email
    for event in success_events:
        if event['matched']:
            continue
        success_username = event['email'].split('@')[0].lower()
        
        for rn, data in row_data.items():
            if data['status'] is not None:
                continue
            if data['user'] is None:
                continue
            
            input_username = data['user'].split('@')[0].lower()
            
            if input_username == success_username:
                row_data[rn]['status'] = 'SUCCESS'
                row_data[rn]['group_id'] = event['group_id']
                row_data[rn]['matched_email'] = event['email']
                row_data[rn]['reason'] = f'User fragment matched to {event["email"]}'
                row_data[rn]['fragment_search'] = True
                row_data[rn]['fragment_username'] = input_username
                event['matched'] = True
                break
    
    # Calculate statistics
    stats = {
        'total': 0,
        'success': 0,
        'failed_group': 0,
        'failed_user': 0,
        'failed_other': 0,
        'fragment_used': 0
    }
    
    for row_num, data in row_data.items():
        if data['group'] is None:
            continue
        stats['total'] += 1
        
        if data['status'] == 'SUCCESS':
            stats['success'] += 1
        elif data['reason'] == 'Group not found':
            stats['failed_group'] += 1
        elif data['reason'] == 'User not found':
            stats['failed_user'] += 1
        else:
            stats['failed_other'] += 1
        
        if data['fragment_search']:
            stats['fragment_used'] += 1
    
    return row_data, stats


def generate_csv_report(row_data, output_path="summary_report.csv"):
    """Generate clean CSV report"""
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow(['Input', 'Result', 'Reason'])
        
        # Write data rows
        for row_num in sorted(row_data.keys()):
            data = row_data[row_num]
            if data['group'] is None:
                continue
            
            # Format input as "Group,Email"
            input_value = f"{data['group']},{data['user']}"
            
            # Format result
            if data['status'] == 'SUCCESS':
                result = 'Success'
            else:
                result = 'Failed'
            
            # Format reason
            if data['status'] == 'SUCCESS':
                if data['matched_email'] and data['matched_email'] != data['user']:
                    reason = f"User fragment matched to {data['matched_email']}"
                else:
                    reason = ''
            else:
                reason = data['reason'] or 'Unknown'
            
            writer.writerow([input_value, result, reason])
    
    return output_path


def print_statistics(stats):
    """Print only statistics to terminal"""
    
    print("\n📈 STATISTICS:")
    print(f"   Total Rows Processed:        {stats['total']}")
    print(f"   ✅ Successful:               {stats['success']}")
    print(f"   ❌ Failed (Group Not Found): {stats['failed_group']}")
    print(f"   ❌ Failed (User Not Found):  {stats['failed_user']}")
    print(f"   ❌ Failed (Other/Unknown):   {stats['failed_other']}")
    print(f"   🔍 Fragment Search Used:     {stats['fragment_used']}")
    print()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze log file')
    parser.add_argument('log_file', nargs='?', default='output.txt')
    parser.add_argument('-o', '--output', default='summary_report.csv')
    
    args = parser.parse_args()
    
    try:
        print(f"📂 Analyzing log file: {args.log_file}")
        
        row_data, stats = analyze_log_file(args.log_file)
        
        # Print only statistics to terminal
        print_statistics(stats)
        
        # Generate CSV report
        generate_csv_report(row_data, args.output)
        
        print(f"📄 Report saved to: {args.output}")
        
    except FileNotFoundError:
        print(f"❌ Error: Log file '{args.log_file}' not found!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()