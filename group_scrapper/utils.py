import os

def save_results(results, filename="result.txt"):
    """
    Save group URLs to a text file
    
    Args:
        results: List of group URLs
        filename: Output filename (default: result.txt)
    """
    try:
        with open(filename, 'w') as f:
            for url in results:
                f.write(f"{url}\n")
        return True
    except Exception as e:
        print(f"Error saving results: {e}")
        return False