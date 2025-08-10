import pandas as pd
import time
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from utils.utils import chunk_data 
from utils.utils import wrapper
from utils.utils import merge_chunk_excels
from utils.utils import delete_chunks_folder
from utils.post_processing_analyser import clean_and_analyze_final_excel

if __name__ == "__main__":
    
    # Load Excel file
    df = pd.read_excel('Data\\Raw_Contacts.xlsx', dtype=str)

    phone_numbers = df['Phone Numbers'].astype(str).tolist()  # Change if your column name is different
    # API setup
    url = "https://simownership.online/newdb.php"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://simownership.online/",
        "Origin": "https://simownership.online"
    }


    chunk_size = 100  # for example 500 contacts --> [100, 100, 100, 100, 100]

    # Create chunks
    chunks = chunk_data(phone_numbers, chunk_size)

    print("Process Started")
    start = time.time()
    # Create argument tuples for each chunk
    args_list = [(chunk, url, headers, idx) for idx, chunk in enumerate(chunks)]


    with Pool(processes=min(5, cpu_count())) as pool:  # Use 5 or less cores
        list(tqdm(pool.imap(wrapper, args_list), total=len(args_list), desc="⚙️ Processing Chunks"))
    
    end = time.time()
    print("Process Ended")
    print("Time Taken:", int((end - start)/60), "mins and", int(abs((end - start) - int(end - start))*60), "secs")

    print("\nYour enriched data is saved to 'Processed chunks' folder in chunk files!\n")

    MERGE_MODE = "delete"  # options: "keep", "delete", "none"

    if MERGE_MODE == "keep":
        merge_chunk_excels()
        print("Merged done")
    elif MERGE_MODE == "delete":
        merge_chunk_excels()
        delete_chunks_folder()
        print("Merged done and chunks folder deleted")
    elif MERGE_MODE == "none":
        print("You just have chunks of 500 contacts each")

    clean_and_analyze_final_excel("Output\\final_output.xlsx")

    


