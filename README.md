# AN INTERACTIVE TKINTER-BASED TOOL FOR CO-OCCURRENCE AND CLUSTER VISUALISATION
---

## 📘 Co-Occurrence & Cluster Visualization Tool
A Python-based interactive application to analyze co-occurrence patterns between scientific phrases and nano-related terms using data preprocessing, NLP, and network visualization techniques.

---
## 🚀 Project Overview
- This project processes nanoscience research literature to identify relationships between extracted scientific phrases and nano-related terms.
- It generates a refined co-occurrence matrix and provides a Tkinter-based GUI that enables users to visualize and explore phrase–nano term associations through interactive graphs.
---

## 🧩 Key Features
- 📂 Data Aggregation: Reads and combines multiple .txt files into a structured dataset.

- 📝 Phrase Extraction: Removes stopwords, filters nano-prefix words, and extracts meaningful scientific phrases.

- 🔍 Nano-Term Grouping: Detects nano-related terms using regex and groups similar variants.

- 📊 Co-occurrence Matrix: Builds and optimizes a matrix showing phrase–nano term linkages.

- 🖥️ Interactive GUI: Visualizes cluster graphs using NetworkX + Matplotlib inside a Tkinter application.

- 📈 Export Support: Save processed data and visual graphs for research use.


## 🛠️ Technologies & Libraries Used

- Python 3.x
- Pandas – data handling
- NumPy – numerical operations
- NLTK – tokenization, stopwords, POS tagging
- Regex (re) – nano-term extraction and phrase cleaning
- collections.Counter – term frequency counting
- NetworkX – network graph generation
- Matplotlib – visualization
- Tkinter / ttk – GUI development
- OS module – file handling


<img width="2547" height="1150" alt="image" src="https://github.com/user-attachments/assets/0ceaf570-f72d-4c2b-8413-c58f7b96a8d3" />

## ⚙️ How It Works
### 1. Data Collection & Cleaning
- Reads 155+ raw .txt files
- Extracts relevant metadata
- Stores everything into a combined Excel sheet

  <img width="2723" height="989" alt="image" src="https://github.com/user-attachments/assets/eace1873-1059-4d89-b402-599f5fc8b7e1" />
- (Rows): 72,950
- (Columns): 67


### 2. Phrase Extraction
- Tokenizes titles using NLTK
- Removes stopwords + nano-prefix words
- Extracts final scientific phrases

   <img width="1511" height="596" alt="image" src="https://github.com/user-attachments/assets/5aacab3f-5fb7-49e8-b4b8-093f9fe8155d" />


### 3. Nano-Term Grouping
- Regex-based extraction of words starting with "nano"
- Groups similar variants based on prefix rules
- Filters groups with at least 6 terms
<img width="1009" height="466" alt="image" src="https://github.com/user-attachments/assets/4d55c523-a479-40ee-ac75-5eb21323826c" />
<img width="951" height="428" alt="image" src="https://github.com/user-attachments/assets/1849d17b-2f74-492c-b818-ddb67c1f1ad3" />
<img width="2353" height="1183" alt="image" src="https://github.com/user-attachments/assets/8c6a2e6c-c277-4631-8c84-8ab15d66fcb2" />

### 4. Co-Occurrence Matrix
- Matches scientific phrases with grouped nano-terms
- Builds an initial 97,351 × 84 matrix
- Applies frequency filtering
- Produces a final refined matrix of 130 × 25
  <img width="2712" height="1102" alt="image" src="https://github.com/user-attachments/assets/f74a777e-66a7-46f6-9555-b92626e4b984" />

### 5. GUI Visualization
- User inputs: nano-term, year range, phrase limit
- Shows filtered tables
- Generates cluster graphs (NetworkX + Matplotlib)
- Export options available

<img width="3000" height="1519" alt="image" src="https://github.com/user-attachments/assets/76e3e257-8667-4506-b10f-e5a5fdb0a67d" />


## 👩‍💻 Author

Priyanka Rath
Final Year Student
Silicon University, Bhubaneswar
