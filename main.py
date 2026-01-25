import io
import os
import zipfile
import functions_framework
from google.cloud import storage
from datetime import datetime

# Function to handle Japanese/Shift-JIS filenames in ZIPs
def fix_filename(filename):
    try:
        return filename.encode('cp437').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        try:
            return filename.encode('cp437').decode('cp932')
        except:
            return filename

@functions_framework.cloud_event
def process_gcs_zip(cloud_event):
    data = cloud_event.data
    bucket_name = data["bucket"]
    file_name = data["name"]
    
    today_str = datetime.now().strftime('%Y%m%d')
    RESULT_FILE_NAME = f"SecondBrain_Joined_{today_str}.md"
    
    if file_name == RESULT_FILE_NAME or not file_name.endswith('.zip'):
        return

    print("INFO: Second Brain Joiner is running...")
    print(f"INFO: [START] Processing: {file_name}")

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    try:
        zip_bytes = blob.download_as_bytes()
        
        tree_map_output = io.StringIO()
        details_output = io.StringIO()
        
        md_count = 0
        failed_files = []

        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
            target_entries = []
            for info in z.infolist():
                decoded_name = fix_filename(info.filename)
                if decoded_name.endswith('.md') and '/.' not in decoded_name:
                    if not os.path.basename(decoded_name).startswith('.'):
                        target_entries.append((info.filename, decoded_name, info))


            target_entries.sort(key=lambda x: x[1])
            total_targets = len(target_entries)
            print(f"INFO: Found {total_targets} markdown files.")

            # Section 01: Tree Map 
            tree_map_output.write("# 01_Structure (Tree Map)\n")
            if not target_entries:
                tree_map_output.write("- No valid files found.\n")
            else:
                for _, decoded, _ in target_entries:
                    tree_map_output.write(f"- {decoded}\n")
            
            details_output.write("\n" + "*"*40 + "\n\n# 02_Note Details\n\n")

            # Section 02: Content Integration
            for raw_path, decoded_path, info in target_entries:
                try:
                    mod_time = datetime(*info.date_time).strftime('%Y-%m-%d %H:%M')
                    with z.open(raw_path) as f:
                        content = f.read().decode('utf-8', errors='ignore')
                        details_output.write(f"## [PATH]: /{decoded_path}\n")
                        details_output.write(f"[LAST_MODIFIED]: {mod_time}\n")
                        details_output.write("---\n")
                        details_output.write(f"{content}\n")
                        details_output.write("\n---\n---\n\n")
                        md_count += 1
                except Exception as e:
                    print(f"WARNING: Failed to process ({decoded_path}): {str(e)}")
                    failed_files.append(decoded_path)

            # Section 00: Integrity Report
            is_integrated = (md_count == total_targets)
            status_emoji = "✅" if is_integrated else "⚠️"
            
            report = f"""# 00_Integrity Verification Report
            Status: {status_emoji} {'Success' if is_integrated else 'Incomplete'}
            Verified at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            Total Targets: {total_targets}
            Successfully Processed: {md_count}
            Errors: {len(failed_files)}
            Source ZIP: {file_name}
            {"="*40}
            """
            if failed_files:
                report += "## Error Details:\n" + "\n".join([f"- {f}" for f in failed_files]) + "\n"
            report += "\n"

        final_md = report + tree_map_output.getvalue() + details_output.getvalue()
        footer_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        final_md += f"\n\n---\n**Sorted & Verified by Second Brain Joiner**"
        final_md += f"\n(AI Architect: **Dicon (Hirofumi Inoue)**) at {footer_time}\n"

        result_blob = bucket.blob(RESULT_FILE_NAME)
        result_blob.upload_from_string(final_md, content_type="text/markdown")
        
        print(f"INFO: Process Completed - {status_emoji} Result: {md_count}/{total_targets}")

    except Exception as e_global:
        print(f"CRITICAL: Fatal Error: {str(e_global)}")