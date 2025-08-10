import pandas as pd
import time
from tqdm import tqdm
import os

def clean_number(number):
    try:
        # Handle float or int types
        number = str(number).strip()
        for prefix in ("0092", "+92", "92", "0"):
            if number.startswith(prefix):
                number = number[len(prefix):]
                break

        number = number.split('.')[0] # Or we can do this too: number = number[:number.index('.')]
        if not number.isdigit() or len(number) != 10: raise ValueError

        return number
    except:
        print(f"Skipping invalid number: {number}")
        return None


# Break data into chunks
def chunk_data(data, chunk_size):
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


def wrapper(args):
    chunk, url, headers, chunk_index = args
    
    result = main_processing(chunk, url, headers)


    # Save this chunk’s result
    df = pd.DataFrame(result)
    output_dir = "Processed_Chunks"
    os.makedirs(output_dir, exist_ok=True)
    df.to_excel(f"Output/{output_dir}/chunk_{chunk_index+1}.xlsx", index=False)

    return result


def merge_chunk_excels(folder="Processed_Chunks", output="final_output.xlsx"):
    import os
    import pandas as pd

    base_dir = os.path.dirname(os.path.abspath(__file__))  # points to utils/
    chunks_folder_path = os.path.join(base_dir, '..', 'Output', folder)
    output_file_path = os.path.join(base_dir, '..', 'Output', output)

    all_dfs = []
    for filename in sorted(os.listdir(chunks_folder_path)):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(chunks_folder_path, filename)
            df = pd.read_excel(file_path)
            all_dfs.append(df)

    merged_df = pd.concat(all_dfs, ignore_index=True)
    merged_df.to_excel(output_file_path, index=False)

    print(f"Merged {len(all_dfs)} chunks into {output}")
    
def delete_chunks_folder(folder="Processed_Chunks"):
    import os
    import shutil

    base_dir = os.path.dirname(os.path.abspath(__file__))  # points to utils/
    folder_path = os.path.join(base_dir, '..', 'Output', folder)

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
        print(f"Folder deleted: '{folder_path}'")
    else:
        print(f"Folder '{folder_path}' does not exist or is not a directory.")

def details(data):
    """
    Extracts the most meaningful info from a list of dicts.
    Assumes data is a list of 1 or more dictionaries, each possibly containing:
    'name', 'cnic', 'phone', 'address'
    """

    name, cnic, phone, address = "", "", "", ""

    if isinstance(data, dict):  # Handle dict input just in case
        data = [data]

    if len(data) == 1:
        entry = data[0]
        name = entry.get('name', 'no record')
        cnic = entry.get('cnic', 'no record')
        phone = entry.get('phone', 'no record')
        address = entry.get('address', 'no record')

    elif len(data) >= 2:
        first, second = data[0], data[1]

        # Name: Prefer a valid one (not 'Not Available')
        name = (
            first.get('name') if first.get('name') and first.get('name') != 'Not Available'
            else second.get('name') if second.get('name') and second.get('name') != 'Not Available'
            else 'no record'
        )

        # CNIC: Prefer the valid one (not 'Unknown')
        cnic = (
            second.get('cnic') if second.get('cnic') and second.get('cnic') != 'Unknown'
            else first.get('cnic') if first.get('cnic') and first.get('cnic') != 'Unknown'
            else 'no record'
        )

        # Phone: Prefer the longer one (likely complete)
        phones = [entry.get('phone') for entry in [first, second] if entry.get('phone')]
        phone = max(phones, key=len) if phones else 'no record'

        # Address: Prefer meaningful address (not 'no' or 'Record not found')
        for entry in [second, first]:
            addr = entry.get('address', '').strip().lower()
            if addr not in ['no', 'record not found', '']:
                address = entry.get('address')
                break
            else:
                address = 'no record'

    return name, cnic, phone, address


def main_processing(phone_numbers_chunk, url, headers):
    from utils.utils import details
    from utils.api_handler import make_request_with_retry

    results = []

    for number in tqdm(phone_numbers_chunk, desc="🔍 Enriching"):
        time.sleep(0.5) 
        cleaned = clean_number(number)
        if not cleaned or len(cleaned) != 10:
            print(f"Skipping invalid number: {number}")
            results.append({
                "name": "no record",
                "cnic": "no record",
                "phone": "no record",
                "address": "no record",
                "status": "Invalid Number"
            })
            continue

        files = {"searchNumber": (None, cleaned)}

        try:
            response = make_request_with_retry(cleaned, url, headers)
            if response.status_code == 200:
                try:
                    jsx = response.json()
                    data = jsx['data']
                    name, cnic, phone, address = details(data)

                    results.append({
                        "name": name or "no record",
                        "cnic": cnic or "no record",
                        "phone": phone or "no record",
                        "address": address or "no record",
                        "status": "Success"
                    })

                except Exception as decode_error:
                    message = response.json().get('message')
                    if "For paid service" in message:
                        results.append({
                            "name": "no record",
                            "cnic": "no record",
                            "phone": "no record",
                            "address": "no record",
                            "status": "Needs payment"
                        })

            else:
                results.append({
                    "name": "no record",
                    "cnic": "no record",
                    "phone": "no record",
                    "address": "no record",
                    "status": f"HTTP {response.status_code}"
                })

        except Exception as e:
            message = response.json().get('message') if response else None
            results.append({
                "name": "no record",
                "cnic": "no record",
                "phone": "no record",
                "address": "no record",
                "status": "Needs payment" if message and "For paid service" in message else f"HTTP {response.status_code}"
            })

        time.sleep(1)

    return results

