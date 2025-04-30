#!/usr/bin/env python
import argparse
import os
import sys

# Import project modules
from auth import authenticate, load_cookies
from search import search_groups
from utils import save_results

def main():
    parser = argparse.ArgumentParser(description='Facebook Group Scraper')
    parser.add_argument('--login', action='store_true', help='Login to Facebook and save cookies')
    parser.add_argument('--logout', action='store_true', help='Logout and delete all cookies and saved account data')
    parser.add_argument('--search', type=str, help='Search keyword for Facebook groups')
    parser.add_argument('--limit', type=int, default=50, help='Limit of search results (default: 50)')
    parser.add_argument('--help', '-h', action='help', help='Show this help message and exit')
    args = parser.parse_args()
    
    if args.login:
        authenticate()
        print("Login successful. Cookies saved.")
        return
    
    if args.logout:
        try:
            os.remove('facebook_cookies.pkl')
            print('Logout successful. Cookies and account data deleted.')
        except FileNotFoundError:
            print('No cookies found to delete.')
        return
    
    if not args.search:
        parser.error("--search argument is required unless --login is used")
    
    # Load cookies for authenticated session
    session = load_cookies()
    if not session:
        print("Error: No saved cookies found. Please login first using --login")
        return
    
    # Search for groups
    print(f"Searching for groups with keyword: {args.search}")
    print(f"Limit set to: {args.limit}")
    
    results = search_groups(session, args.search, args.limit)
    
    if results:
        save_results(results)
        print(f"Found {len(results)} groups. Results saved to result.txt")
    else:
        print("No groups found.")

if __name__ == "__main__":
    main()