# 📞 Contact Probe

## 📌 Overview
**Contact Probe** is an end-to-end pipeline for:
- Enriching contact data via an external API.
- Cleaning, standardizing, and analyzing results.
- Visualizing insights in Power BI.

It is optimized for **large datasets** using **multiprocessing** and **chunk-based processing** to ensure minimal data loss in case of system interruptions.

---

## ⚙️ Workflow

1. **Load Raw Data**  
   The pipeline starts with a raw Excel file (`Raw_Contacts.xlsx`) containing contact phone numbers.

2. **Data Enrichment via API**  
   - Data is split into chunks using `utils.chunk_data()`.
   - Each chunk is processed in parallel using `multiprocessing.Pool` for faster API calls.
   - Results are saved into individual chunk files for fault tolerance.

3. **Merge Results**  
   After all chunks are processed, they are merged into a single file (`final_output.xlsx`) using `merge_chunk_excels()`.

4. **Post-Processing & Analysis**  
   - Column cleanup (trimming, case formatting).
   - Standardization of text/number formats.
   - Generation of summary insights (success rates, payment status counts).
   - Output saved as `final_cleaned.xlsx`.

5. **Visualization in Power BI**  
   - The uncleaned final output is loaded into Power BI.
   - Key visuals include:
     - **Needs Payment %**
     - **Success %**
     - **Success Count**
     - **Total Contacts**
   - Dashboards are stored in `/Power BI/Contacts_Report.pbix` with screenshots.

---

## 📊 Example Visuals

| Success vs Needs Payment | Success % | Other Visuals |
|--------------------------|-----------|---------------|
| ![Bar Chart](Powerbi/screenshots/visual1.png) | ![Bar Chart](Powerbi/screenshots/visual2.png) | ![Pie Chart](Powerbi/screenshots/visual3.png) |

**Additional Insight**  
![Table](Powerbi/screenshots/visual4.png)

---

## 🚀 Features
- **Parallel Execution** using Python's `multiprocessing`.
- **Fault-Tolerant Processing** via chunk-based storage.
- **Automated Cleaning & Insights** with Pandas.
- **Visual Dashboards** in Power BI.

---

## 📂 Project Structure

Contact_Probe/
│
├── README.md
├── requirements.txt
├── LICENSE
│
├── utils/
│ ├── utils.py
│ ├── post_processing_analyser.py
│ └── api_handler.py
│
├── Scripts/
│ └── main.py
│
├── Data/
│ └── Raw_Contacts.xlsx
│
├── Power BI/
│ ├── Contacts_Report.pbix
│ └── screenshots/
│ ├── visual1.png
│ ├── visual2.png
│ ├── visual3.png
│ └── visual4.png
│
├── Output/
│ ├── final_output.xlsx
│ └── final_cleaned.xlsx

## ▶️ How to Run

1. **Clone the Repository**
```bash
    git clone https://github.com/yourusername/Contact_Probe.git
    cd Contact_Probe
```
2. **Install Dependencies**
    pip install -r requirements.txt

3. **Prepare Your Data**
    Place your Raw_Contacts.xlsx inside the Data/ folder.
    Ensure it contains a column with phone numbers.

4. **Run the Enrichment Script**
    python Scripts/main.py

    This will:
        o) Split the data into chunks.
        o) Send each chunk to the API in parallel.
        o) Save processed results as separate chunk files.

5. **Merge & Clean Results**
    python utils/post_processing_analyser.py

    This will:
        o) Merge all chunk files into final_output.xlsx.
        o) Clean and standardize the data.
        o) Generate final_cleaned.xlsx with insights.

6. **Open in Power BI**
    o) Load final_output.xlsx into Power BI for visualization.
    o) View the .pbix file inside Power BI/ for pre-made visuals.


## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.