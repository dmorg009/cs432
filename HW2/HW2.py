import requests
import os
from boilerpy3 import extractors
import time
import hashlib

def get_hash_filename(uri):
    """Create MD5 hash from URI string."""
    return hashlib.md5(uri.strip().encode('utf-8')).hexdigest()

def process_uris(input_file, raw_dir, processed_dir):
    """Process URIs from input file, download content, and remove boilerplate."""
    
    # Create directories if they don't exist
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)
    
    # Initialize extractor for boilerplate removal
    extractor = extractors.ArticleExtractor()
    
    # Read URIs from file
    with open(input_file, 'r', encoding='utf-8') as f:
        uris = [line.strip() for line in f if line.strip()]
    
    # Process each URI
    for uri in uris:
        try:
            # Create hash for filename
            filename = get_hash_filename(uri)
            
            # Define filenames using hash
            raw_file = os.path.join(raw_dir, f"{filename}.html")
            processed_file = os.path.join(processed_dir, f"{filename}.txt")
            
            # Skip if already processed
            if os.path.exists(raw_file) and os.path.exists(processed_file):
                print(f"Skipping {uri} - already processed")
                continue
            
            # Download content
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(uri, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Save raw HTML
            with open(raw_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            # Remove boilerplate and save processed content
            processed_text = extractor.get_content(response.text)
            if processed_text and len(processed_text.strip()) > 0:
                with open(processed_file, 'w', encoding='utf-8') as f:
                    f.write(processed_text)
            else:
                print(f"Warning: No content extracted from {uri}")
                # Remove empty processed file if it exists
                if os.path.exists(processed_file):
                    os.remove(processed_file)
            
            # Be nice to servers
            time.sleep(1)
            
            print(f"Successfully processed {uri}")
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {uri}: {str(e)}")
        except (UnicodeDecodeError, UnicodeEncodeError) as e:
            print(f"Unicode error processing {uri}: {str(e)}")
        except Exception as e:
            print(f"Error processing {uri}: {str(e)}")

def main():
    # Define paths
    test_file = "../HW1/test_uris.txt"
    main_file = "../HW1/collected_uris.txt"
    input_file = main_file
    raw_dir = "./raw_html"
    processed_dir = "./processed_text"
    
    # Process URIs
    process_uris(input_file, raw_dir, processed_dir)

if __name__ == "__main__":
    main()