import json
import os
from datetime import datetime

# --- Configuration and Data Storage ---

# The name of the file where knowledge data will be stored persistently.
DATA_FILE = 'knowledge_data.json'

# Global list to hold all knowledge items in memory during the session.
knowledge_items = []

# --- File Handling Functions (Persistent Storage) ---

def load_data():
    """Loads knowledge items from the JSON file into the global list."""
    global knowledge_items
    try:
        # Check if the data file exists
        if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
            with open(DATA_FILE, 'r') as f:
                knowledge_items = json.load(f)
            print(f"\n[INFO] Loaded {len(knowledge_items)} knowledge items from {DATA_FILE}.")
        else:
            knowledge_items = []
            print(f"\n[INFO] {DATA_FILE} not found or empty. Starting with an empty list.")
    except json.JSONDecodeError:
        print("\n[ERROR] Data file is corrupted (JSON Error). Starting with an empty list.")
        knowledge_items = []
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred while loading data: {e}")
        knowledge_items = []

def save_data():
    """Saves the current knowledge items from the global list to the JSON file."""
    try:
        with open(DATA_FILE, 'w') as f:
            # Use indent=4 for human-readable formatting in the JSON file
            json.dump(knowledge_items, f, indent=4)
        print(f"\n[INFO] Successfully saved {len(knowledge_items)} items to {DATA_FILE}.")
    except Exception as e:
        print(f"\n[ERROR] Could not save data: {e}")

# --- Core Operations (CRUD) ---

def display_items(items_list):
    """A helper function to display a list of items clearly."""
    if not items_list:
        print("No items found matching your criteria.")
        return

    for item in items_list:
        print("-" * 30)
        print(f"ID: {item['id']} | Category: {item['category']}")
        print(f"Title: {item['title']}")
        print(f"Added: {item['date_added']}")
        # Truncate content for a cleaner report view
        content_preview = item['content'][:50] + '...' if len(item['content']) > 50 else item['content']
        print(f"Content Preview: {content_preview}")
    print("-" * 30)
    print(f"Displayed Items: {len(items_list)}")

def add_item():
    """Prompts user for a new knowledge item and adds it to the list."""
    print("\n--- Add New Knowledge Item ---")
    title = input("Title (e.g., 'Python Dictionaries'): ").strip()
    content = input("Content/Definition: ").strip()
    category = input("Category (e.g., 'Code', 'History', 'Math'): ").strip()

    if not title or not content:
        print("[WARNING] Title and Content cannot be empty. Item not added.")
        return

    # Assign a unique ID (based on current list size + 1, sufficient for a starter project)
    # NOTE: Since IDs are reassigned after deletion, this is safe.
    new_id = len(knowledge_items) + 1
    
    new_item = {
        "id": new_id,
        "title": title,
        "content": content,
        "category": category if category else "General", # Default category
        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    knowledge_items.append(new_item)
    save_data() # Save immediately after adding
    print(f"\n[SUCCESS] Item '{title}' added successfully with ID: {new_id}.")

def view_all_items():
    """Displays all stored knowledge items."""
    print("\n--- All Knowledge Items ---")
    if not knowledge_items:
        print("Your knowledge base is currently empty. Add some items!")
        return
    display_items(knowledge_items)

def search_filter_items():
    """Allows user to search items by keyword or filter by category."""
    print("\n--- Search & Filter ---")
    if not knowledge_items:
        print("[WARNING] The knowledge base is empty. Nothing to search.")
        return
    
    print("1. Search by Keyword (Title/Content/Category)")
    print("2. Filter by Specific Category")
    
    search_choice = input("Enter search option (1 or 2, or press Enter to cancel): ").strip()
    
    if not search_choice:
        print("[INFO] Search cancelled.")
        return

    results = []

    if search_choice == '1':
        keyword = input("Enter search keyword: ").strip().lower()
        if not keyword:
            print("[WARNING] Keyword cannot be empty.")
            return

        for item in knowledge_items:
            # Check if keyword is in title, content, or category (case-insensitive)
            if (keyword in item['title'].lower() or
                keyword in item['content'].lower() or
                keyword in item['category'].lower()):
                results.append(item)
        
        print(f"\n--- Search Results for '{keyword}' ---")

    elif search_choice == '2':
        category_filter = input("Enter category to filter by (e.g., 'Code', 'Math'): ").strip()
        if not category_filter:
            print("[WARNING] Category filter cannot be empty.")
            return

        for item in knowledge_items:
            # Check if the item's category matches the filter (case-insensitive)
            if item['category'].lower() == category_filter.lower():
                results.append(item)
        
        print(f"\n--- Filter Results for Category '{category_filter}' ---")

    else:
        print("[ERROR] Invalid search option.")
        return

    display_items(results)

def update_item():
    """Prompts user for an item ID and allows modification of its details."""
    print("\n--- Update Knowledge Item ---")
    
    if not knowledge_items:
        print("[WARNING] The knowledge base is empty. Nothing to update.")
        return

    # Show all items so the user knows which ID to pick
    view_all_items() 
    
    id_to_update_input = input("Enter the ID of the item to update (or press Enter to cancel): ").strip()

    if not id_to_update_input:
        print("[INFO] Update cancelled.")
        return
    
    try:
        id_to_update = int(id_to_update_input)
    except ValueError:
        print("[ERROR] Invalid input. Please enter a valid number ID.")
        return

    # Find the item using a generator expression and next() for efficiency
    item_to_update = next((item for item in knowledge_items if item['id'] == id_to_update), None)

    if not item_to_update:
        print(f"[WARNING] Item with ID {id_to_update} not found.")
        return

    print(f"\nEditing item: '{item_to_update['title']}' (ID: {id_to_update})")
    print("--------------------------------------------------")
    print("💡 Tip: Leave a field blank to keep its current value.")
    
    # Get new values, using existing values as prompts/defaults
    
    # Prompt for Title
    new_title = input(f"New Title (Current: '{item_to_update['title']}'): ").strip()
    
    # Prompt for Content, showing only a preview of the current content
    content_preview = item_to_update['content'][:30] + '...' if len(item_to_update['content']) > 30 else item_to_update['content']
    new_content = input(f"New Content (Current: '{content_preview}'): ").strip()
    
    # Prompt for Category
    new_category = input(f"New Category (Current: '{item_to_update['category']}'): ").strip()

    # Apply updates only if the input is not empty
    if new_title:
        item_to_update['title'] = new_title
    
    if new_content:
        item_to_update['content'] = new_content
        
    if new_category:
        item_to_update['category'] = new_category

    save_data()
    print(f"\n[SUCCESS] Item ID {id_to_update} updated successfully.")


def delete_item():
    """Prompts user for an item ID and deletes the corresponding item."""
    print("\n--- Delete Knowledge Item ---")
    global knowledge_items

    if not knowledge_items:
        print("[WARNING] The knowledge base is empty. Nothing to delete.")
        return

    # Display items to help the user choose the ID
    view_all_items()
    
    id_to_delete_input = input("Enter the ID of the item to delete (or press Enter to cancel): ").strip()

    if not id_to_delete_input:
        print("[INFO] Deletion cancelled.")
        return
    
    try:
        id_to_delete = int(id_to_delete_input)
    except ValueError:
        print("[ERROR] Invalid input. Please enter a valid number ID.")
        return

    initial_length = len(knowledge_items)
    
    # Filter out the item with the matching ID
    knowledge_items = [item for item in knowledge_items if item['id'] != id_to_delete]

    if len(knowledge_items) < initial_length:
        print(f"[SUCCESS] Item with ID {id_to_delete} has been deleted.")
        
        # Re-index remaining items to ensure IDs are contiguous (1, 2, 3...)
        for index, item in enumerate(knowledge_items):
            item['id'] = index + 1
        
        save_data()
    else:
        print(f"[WARNING] Item with ID {id_to_delete} not found.")

# --- Menu Controller and Main Loop ---

def display_menu():
    """Prints the main menu options to the console."""
    print("\n" + "="*40)
    print("  LearnLyt - Knowledge Retention Tool   ")
    print("="*40)
    print("1. Add New Knowledge Item")
    print("2. View All Items")
    print("3. Search/Filter Items")
    print("4. Update Item")
    print("5. Delete Item")
    print("0. Exit and Save")
    print("="*40)

def main():
    """Main function that runs the application loop."""
    
    # 1. Load data first thing when the program starts
    load_data()

    while True:
        display_menu()
        choice = input("Enter your choice (0-5): ").strip()

        if choice == '1':
            add_item()
        elif choice == '2':
            view_all_items()
        elif choice == '3':
            search_filter_items()
        elif choice == '4':
            update_item() # Now calls the new update function
        elif choice == '5':
            delete_item() 
        elif choice == '0':
            print("\nExiting LearnLyt. Thank you for using the tool!")
            save_data()
            # Wait for user input so the console window doesn't close immediately in VS
            input("Press Enter to close the program...")
            break
        else:
            print("\n[WARNING] Invalid choice. Please enter a number between 0 and 5.")

if __name__ == "__main__":
    main()