from mpi4py import MPI
from collections import Counter
import os
import time

# --- CONFIGURATION ---
TARGET_WORDS = ['risk', 'prohibited', 'transparency', 'biometric', 'surveillance', 'compliance', 'penalty']

def count_keywords(filepath):
    """ Reads a file and counts occurrences of TARGET_WORDS. """
    c = Counter()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            words = f.read().lower().split()
            for w in words:
                clean_w = w.strip(".,;:'\"()[]")
                if clean_w in TARGET_WORDS:
                    c[clean_w] += 1
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return c

def main():
    # --- MPI SETUP ---
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # --- MASTER NODE (Rank 0) ---
    if rank == 0:
        start_time = time.time()
        
        # 1. SETUP DATA PATH
        # We look for the 'data/chunks' folder relative to where this script is running
        data_dir = os.path.join(os.getcwd(), "data", "chunks")
        
        print(f"--- Starting Parallel Analysis on {size} Cores ---")
        print(f"Looking for data in: {data_dir}")

        if not os.path.exists(data_dir):
            print("\n!!! ERROR: DATA FOLDER NOT FOUND !!!")
            print("You must run 'generate_data.py' or 'preprocess.py' first.")
            all_files = []
        else:
            all_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".txt")]
            print(f"Found {len(all_files)} files to process.")
        
        # 2. DISTRIBUTE FILES
        chunks = [[] for _ in range(size)]
        for i, file in enumerate(all_files):
            chunks[i % size].append(file)
    else:
        chunks = None

    # --- SCATTER ---
    my_files = comm.scatter(chunks, root=0)

    # --- WORKER ---
    my_total = Counter()
    for fpath in my_files:
        my_total += count_keywords(fpath)

    # --- GATHER ---
    all_results = comm.gather(my_total, root=0)

    # --- MASTER (Final Tally) ---
    if rank == 0:
        final_count = Counter()
        for res in all_results:
            final_count += res
            
        duration = time.time() - start_time
        
        print("\n" + "="*40)
        print(f"FINAL RESULTS (Time: {duration:.4f} seconds)")
        print("="*40)
        print(f"{'TERM':<15} | {'COUNT':<10}")
        print("-" * 30)
        for word in TARGET_WORDS:
            count = final_count[word]
            print(f"{word.upper():<15} | {count:<10}")
        print("="*40)

if __name__ == "__main__":
    main()