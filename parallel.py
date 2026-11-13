import os

# CONFIGURATION
INPUT_FILE = "/Users/arminakhlaghinia/Desktop/project/data/ai_act.txt"  # Your big AI Act file
OUTPUT_DIR = "/Users/arminakhlaghinia/Desktop/project/data/chunks"         # Where the pieces will go
LINES_PER_CHUNK = 200               # How many lines per small file

def split_file():
    # 1. Create the output folder if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        print(f"Creating folder: {OUTPUT_DIR}")
        os.makedirs(OUTPUT_DIR)
    
    # 2. Check if input file exists
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: Could not find {INPUT_FILE}")
        print("Please upload your text file and rename it to 'full_text.txt' inside the 'data' folder.")
        return

    # 3. Read and Split
    print(f"Reading {INPUT_FILE}...")
    with open(INPUT_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        count = 0
        file_idx = 0
        current_lines = []
        
        for line in f:
            current_lines.append(line)
            count += 1
            
            # When we reach the limit, save a chunk
            if count >= LINES_PER_CHUNK:
                output_name = os.path.join(OUTPUT_DIR, f"chunk_{file_idx}.txt")
                with open(output_name, 'w', encoding='utf-8') as out:
                    out.writelines(current_lines)
                print(f"  Created {output_name}")
                
                # Reset for next chunk
                current_lines = []
                count = 0
                file_idx += 1
        
        # Save any remaining lines
        if current_lines:
            output_name = os.path.join(OUTPUT_DIR, f"chunk_{file_idx}.txt")
            with open(output_name, 'w', encoding='utf-8') as out:
                out.writelines(current_lines)
            print(f"  Created {output_name}")

    print("Done! You can now run the parallel analysis.")

if __name__ == "__main__":
    split_file()