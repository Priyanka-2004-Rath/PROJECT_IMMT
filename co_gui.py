import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# === Load Excel Files Separately ===
file_path_cooccur = r"c:\Users\Priyanka Rath\Desktop\IMMT\sum_column_100.xlsx"
file_path_phrases = r"C:\Users\Priyanka Rath\Desktop\IMMT\phrases_with_year_author.xlsx"
file_path_variants = r"C:\Users\Priyanka Rath\Desktop\IMMT\pre_min6.txt"

cooccur_df = pd.read_excel(file_path_cooccur)
phrases_df = pd.read_excel(file_path_phrases)

with open(file_path_variants, "r", encoding="utf-8") as file:
    variant_lines = [line.strip() for line in file if line.strip()]

cooccur_df.rename(columns={cooccur_df.columns[0]: 'Phrase'}, inplace=True)
cooccur_df['Phrase'] = cooccur_df['Phrase'].astype(str).str.strip().str.lower()
phrases_df['Phrase'] = phrases_df['Phrase'].astype(str).str.strip().str.lower()
phrases_year_map = dict(zip(phrases_df['Phrase'], phrases_df['PY']))
phrases_author_map = dict(zip(phrases_df['Phrase'], phrases_df['AU']))  # AU mapping

# === Build variant_to_main mapping ===
variant_to_main = {}
current_main_term = None
for line in variant_lines:
    line = str(line).strip()
    if line.startswith("[") and "]" in line:
        group = line[1:].split("]")[0].strip()
        mapping_dict = {
            "nanopart": "nano-particle",
            "nanotube": "nano-tube",
            "nanomate": "nano-material",
            "nanowire": "nano-wire",
            "nanocrys": "nano-crystal",
            "nanostru": "nano-structure",
            "nanoshee": "nano-sheet",
            "nanocomp": "nano-composite",
            "nanofibe": "nano-fiber",
            "nanodiam": "nano-diamond",
            "nanoplat": "nano-platelet",
            "nanocomp": "nano-compartment",
            "nanorods": "nano-rods",
            "nanotech": "nanotech",
            "nanoscal": "nano-scale",
            "nanosphe": "nano-sphere",
            "nanoclus": "nano-clusters",
            "nanosize": "nano-size",
            "nanohybr": "nano-hybrid",
            "nanoflui": "nano-fluid",
            "nanofibr": "nano-fibrillated",
            "nanomedi": "nano-mediated",
            "nanocata": "nano-catalysis",
            "nanoribb": "nano-ribbon",
            "nanotoxi": "nano-toxicity",
            "nanoflak": "nano-flakes"
        }
        current_main_term = mapping_dict.get(group, f"nano-{group}")
    elif line.startswith("- "):
        variant = line[2:].split(":")[0].strip().lower()
        variant_to_main[variant] = current_main_term

# === GUI Setup ===
root = tk.Tk()
root.title("Phrase/Nano-Term Co-occurrence Viewer")
root.geometry("1300x750")

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Enter Nano-Term(s):", font=("Arial", 12)).grid(row=0, column=0, padx=5)
entry = tk.Entry(input_frame, width=40)
entry.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Enter Years:", font=("Arial", 12)).grid(row=0, column=2, padx=5)
year_entry = tk.Entry(input_frame, width=20)
year_entry.grid(row=0, column=3, padx=5)

tk.Label(input_frame, text="Top Phrases (or 'all'):", font=("Arial", 12)).grid(row=0, column=4, padx=5)
limit_entry = tk.Entry(input_frame, width=7)
limit_entry.insert(0, "10")
limit_entry.grid(row=0, column=5, padx=5)

search_button = tk.Button(input_frame, text="Search")
search_button.grid(row=0, column=6, padx=5)

clear_button = tk.Button(input_frame, text="Clear")
clear_button.grid(row=0, column=7, padx=5)

download_button = tk.Button(input_frame, text="Download Image")
download_button.grid(row=0, column=8, padx=5)

# === Table Frame ===
table_frame = tk.Frame(root)
table_frame.pack(pady=10)
tree = ttk.Treeview(table_frame)
scroll_y = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
tree.configure(yscrollcommand=scroll_y.set)
tree.grid(row=0, column=0, sticky='nsew')
scroll_y.grid(row=0, column=1, sticky='ns')
table_frame.grid_columnconfigure(0, weight=1)
table_frame.grid_rowconfigure(0, weight=1)
table_frame.pack_configure(anchor='center')

# === Chart Frame ===
chart_frame = tk.Frame(root)
chart_frame.pack(fill='both', expand=True)
canvas_widget = None
  
def draw_cluster_multi(nano_terms, combined_data, title):
    global canvas_widget
    for widget in chart_frame.winfo_children():
        widget.destroy()
    G = nx.Graph()
    for term in nano_terms:
        G.add_node(term)
    for phrase, links in combined_data.items():
        G.add_node(phrase)
        for term, weight in links.items():
            if weight > 0:
                G.add_edge(term, phrase, weight=weight)

    pos = nx.spring_layout(G, seed=42, k=10)
    max_weight = max([weight for links in combined_data.values() for weight in links.values()], default=1)
    global_sums = cooccur_df.sum(numeric_only=True)
    max_sum = global_sums[nano_terms].max() if nano_terms else 1

    sizes = []
    for node in G.nodes():
        if node in nano_terms:
            raw_sum = global_sums.get(node, 1)
            size = 1500 + (raw_sum / max_sum) * 3500
            sizes.append(size)
        else:
            sizes.append(1500)

    edge_widths = [1 + (G[u][v]['weight'] / max_weight) * 5 for u, v in G.edges()]
    colors = ['red' if node in nano_terms else 'skyblue' for node in G.nodes()]
    fig, ax = plt.subplots(figsize=(16, 12))
    nx.draw_networkx_edges(G, pos, ax=ax, width=edge_widths, edge_color='gray', alpha=0.6)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=sizes, node_color=colors)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10)
    edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges() if G[u][v]['weight'] >= 15}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    ax.set_title(title, fontsize=16)
    ax.set_axis_off()
    fig.tight_layout(pad=1.5)
    fig.subplots_adjust(top=0.85)
    canvas_widget = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack(fill='both', expand=True)

def clear_fields():
    entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    limit_entry.delete(0, tk.END)
    limit_entry.insert(0, "10")
    tree.delete(*tree.get_children())
    for widget in chart_frame.winfo_children():
        widget.destroy()

import re
import re

def search():
    raw_input = entry.get().strip().lower()
    year_input = year_entry.get().strip()
    limit_input = limit_entry.get().strip().lower()

    # === Top phrases limit ===
    if limit_input == "all":
        top_n = None
    else:
        try:
            top_n = int(limit_input)
        except ValueError:
            messagebox.showerror("Invalid Limit", "Please enter a number or 'all'.")
            return

    # === Year filter logic ===
    year_filter = set()
    if year_input:
        parts = [p.strip().replace(" to ", "-") for p in year_input.split(',')]
        for part in parts:
            if '-' in part:
                try:
                    start, end = map(int, part.split('-'))
                    year_filter.update(range(start, end + 1))
                except:
                    messagebox.showerror("Invalid Range", f"Invalid year range: {part}")
                    return
            else:
                try:
                    year_filter.add(int(part))
                except:
                    messagebox.showerror("Invalid Year", f"Invalid year: {part}")
                    return

    # === Nano-term input parsing and resolution ===
    input_terms = [term.strip() for term in raw_input.split(',') if term.strip()]
    all_nano_terms = [col for col in cooccur_df.columns if col != 'Phrase']
    global_sums = cooccur_df.sum(numeric_only=True)

    resolved_terms = set()
    for term in input_terms:
        term = term.lower()
        if term in variant_to_main:
            resolved_terms.add(variant_to_main[term])
        elif term in all_nano_terms:
            resolved_terms.add(term)
        elif term == "nano" or term == "nano*":
            top_terms = global_sums[all_nano_terms].sort_values(ascending=False).head(5).index.tolist()
            resolved_terms.update(top_terms)
        else:
            variant_matches = [v for v in variant_to_main if v.startswith(term)]
            if variant_matches:
                for v in variant_matches:
                    resolved_terms.add(variant_to_main[v])
            else:
                pattern = re.compile(rf"^{re.escape(term)}")
                matched = [col for col in all_nano_terms if pattern.match(col)]
                if matched:
                    resolved_terms.update(matched)

    # === Prepare working dataframe ===
    temp_df = cooccur_df.copy()
    temp_df['PY'] = temp_df['Phrase'].map(phrases_year_map)
    temp_df['AU'] = temp_df['Phrase'].map(phrases_author_map)
    temp_df = temp_df.dropna(subset=['PY'])

    if year_filter:
        temp_df = temp_df[temp_df['PY'].apply(lambda x: int(x) in year_filter)]

    # === If no nano-term entered, infer top used nano-terms from filtered data ===
    if not resolved_terms:
        inferred_terms = set()
        for _, row in temp_df.iterrows():
            for term in all_nano_terms:
                if row[term] > 0:
                    inferred_terms.add(term)
        resolved_terms = inferred_terms

    valid_terms = [term for term in resolved_terms if term in all_nano_terms]

    if not valid_terms:
        messagebox.showinfo("Info", "No valid nano-terms found.")
        return

    # === Build co-occurrence data ===
    combined_data = {}
    for nano_term in valid_terms:
        term_df = temp_df[['Phrase', nano_term, 'PY']].copy()
        term_df = term_df[term_df[nano_term] > 0].sort_values(by=nano_term, ascending=False)
        if top_n:
            term_df = term_df.head(top_n)
        for _, row in term_df.iterrows():
            phrase = row['Phrase']
            if phrase not in combined_data:
                combined_data[phrase] = {}
            combined_data[phrase][nano_term] = row[nano_term]

    for phrase in combined_data:
        for term in valid_terms:
            combined_data[phrase].setdefault(term, 0)

    # === Table Display ===
    tree.delete(*tree.get_children())
    tree["columns"] = ("Phrase", "Year", "Author") + tuple(valid_terms)
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    for phrase, links in combined_data.items():
        year = phrases_year_map.get(phrase, "NA")
        author = phrases_author_map.get(phrase, "NA")
        if isinstance(year, float):
            year = int(year)
        if pd.isna(year) or year == "NA":
            continue
        values = tuple(links[term] for term in valid_terms)
        tree.insert("", "end", values=(phrase, year, author, *values))

    # === Title and Graph ===
    title = f"Co-Occurrence: {', '.join(valid_terms)}"
    if year_filter:
        years = sorted(year_filter)
        title += f" (Years: {years[0]} - {years[-1]})"
    draw_cluster_multi(valid_terms, combined_data, title)



def download_image():
    if not canvas_widget:
        messagebox.showwarning("No Chart", "Please search first to generate a chart.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG Image", ".png"), ("JPEG Image", ".jpg")])
    if not file_path:
        return
    try:
        fig = canvas_widget.figure
        fig.savefig(file_path, dpi=300)
        messagebox.showinfo("Success", f"Image saved to: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save image: {e}")

search_button.config(command=search)
clear_button.config(command=clear_fields)
download_button.config(command=download_image)
root.mainloop()