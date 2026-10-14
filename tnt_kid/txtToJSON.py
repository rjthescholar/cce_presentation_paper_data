import os
import json
import argparse

def process_folder(input_folder, output_file, custom_name=None, do_chunk=False, chunk_size=512):
    # 1. Determine the base name for the ID
    if custom_name:
        base_name = custom_name
    else:
        base_name = os.path.basename(os.path.normpath(input_folder))
    
    json_array = []
    
    # 2. List all text files
    try:
        files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
        files.sort() 
    except FileNotFoundError:
        print(f"Error: The folder '{input_folder}' was not found.")
        return

    print(f"Found {len(files)} text files in '{input_folder}'...")
    if do_chunk:
        print(f"Chunking enabled: Splitting files into segments of {chunk_size} tokens.")

    # 3. Loop through files
    for index, filename in enumerate(files, start=1):
        file_path = os.path.join(input_folder, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read().strip()
                
                # --- CLEANING ---
                # Remove newlines/double spaces to make it safe for the model
                clean_text = content.replace('\n', ' ').replace('\r', '')
                clean_text = " ".join(clean_text.split())
                
                # Base metadata
                file_title = os.path.splitext(filename)[0]
                base_id = f"{base_name}-{index}"

                # --- CHUNKING LOGIC ---
                if do_chunk:
                    # Split text into a list of words ("tokens")
                    words = clean_text.split()
                    
                    # If file is empty, skip
                    if not words:
                        continue

                    # Create chunks
                    total_chunks = (len(words) + chunk_size - 1) // chunk_size
                    
                    for i in range(0, len(words), chunk_size):
                        chunk_words = words[i:i + chunk_size]
                        chunk_text = " ".join(chunk_words)
                        
                        part_num = (i // chunk_size) + 1
                        
                        # Generate Part-specific ID and Title
                        # ID format: CS0447-1-P1
                        chunk_id = f"{base_id}-P{part_num}"
                        # Title format: Intro to C (Part 1)
                        chunk_title = f"{file_title} (Part {part_num})"

                        doc_obj = {
                            "name": chunk_id,
                            "title": chunk_title,
                            "abstract": chunk_text,
                            "fulltext": "",
                            "keywords": ""
                        }
                        json_array.append(doc_obj)
                        
                else:
                    # --- ORIGINAL LOGIC (No Chunking) ---
                    doc_obj = {
                        "name": base_id,
                        "title": file_title,
                        "abstract": clean_text,
                        "fulltext": "",
                        "keywords": ""
                    }
                    json_array.append(doc_obj)
                
        except Exception as e:
            print(f"Skipping file {filename}: {e}")

    # 4. Save to JSON
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_array, f, indent=4, ensure_ascii=False)
        
        print("-" * 50)
        print(f"Success! Generated {len(json_array)} entries.")
        print(f"Output saved to: {output_file}")
        print("-" * 50)
        
    except IOError as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert folder of text files to JSON Array")
    
    # Required Arguments
    parser.add_argument("--input_folder", type=str, required=True, help="Path to folder with .txt files")
    parser.add_argument("--output_file", type=str, required=True, help="Where to save the .json file")
    
    # Optional Arguments
    parser.add_argument("--folder_name", type=str, help="Override ID prefix (e.g., 'Lecture')")
    
    # New Chunking Arguments
    parser.add_argument("--chunk", action="store_true", help="Enable splitting files into smaller chunks")
    parser.add_argument("--chunk_size", type=int, default=512, help="Number of tokens per chunk (default: 512)")

    args = parser.parse_args()
    
    process_folder(args.input_folder, args.output_file, args.folder_name, args.chunk, args.chunk_size)
