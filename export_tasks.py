#!/usr/bin/env python3
"""
TickTick Task Exporter

This script exports tasks from TickTick using the API.
It requires a valid access token in the .env file.

Usage:
    python export_tasks.py
"""

import os
import sys
import requests
import json
import re
import argparse
from datetime import datetime
from dotenv import load_dotenv


def get_access_token():
    """Get access token from environment variables or .env file"""
    load_dotenv()
    
    token = os.getenv('TICKTICK_ACCESS_TOKEN')
    if not token:
        print("Error: TICKTICK_ACCESS_TOKEN is required but not set")
        print("Please check your .env file")
        sys.exit(1)
    
    # Remove quotes if present
    return token.strip("'\"")


def get_projects(access_token):
    """Get all projects from TickTick API"""
    url = "https://api.ticktick.com/open/v1/project"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        print(f"Making request to: {url}")
        response = requests.get(url, headers=headers)
        
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            projects = response.json()
            print(f"Successfully retrieved {len(projects)} projects")
            return projects
        else:
            print(f"Error: {response.status_code}")
            print(f"Response body: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def get_project_data(access_token, project_id):
    """Get project data including tasks from TickTick API"""
    url = f"https://api.ticktick.com/open/v1/project/{project_id}/data"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        print(f"Getting tasks for project: {project_id}")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            tasks = data.get('tasks', [])
            print(f"Retrieved {len(tasks)} tasks")
            return data
        else:
            print(f"Error getting project data: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def format_date(date_str):
    """Format ISO date string to readable format"""
    if not date_str:
        return None
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return date_str


def create_task_markdown(task, project_name, project_dir, title_in_filename=False):
    """Create a markdown file for a task with frontmatter"""
    task_id = task.get('id', 'unknown')
    title = task.get('title', 'Untitled Task')
    
    # Create filename based on option
    if title_in_filename:
        sanitized_title = sanitize_folder_name(title)
        if len(sanitized_title) > 50:  # Limit filename length
            sanitized_title = sanitized_title[:50]
        filename = f"{sanitized_title}_{task_id}"
    else:
        filename = task_id
    
    filepath = os.path.join(project_dir, f"{filename}.md")
    
    # Determine status icon based on API definitions
    # Task: Normal: 0, Completed: 2
    status = task.get('status', 0)
    status_icon = "✅" if status == 2 else "⬜"
    
    # Determine priority emoji based on API definitions
    # Priority: None:0, Low:1, Medium:3, High:5
    priority = task.get('priority', 0)
    priority_emoji = {
        0: "⚪",  # None/No priority
        1: "🟢",  # Low
        3: "🟡",  # Medium
        5: "🔴"   # High
    }.get(priority, "⚪")  # Default to no priority if unknown value
    
    # Create frontmatter with minimal quotes
    frontmatter = "---\n"
    
    # Only quote title if it contains special characters or starts/ends with space
    title_needs_quotes = ('"' in title or ':' in title or 
                         title.strip() != title or 
                         title.startswith('#') or 
                         title in ['true', 'false', 'null'] or
                         title.replace('.', '').replace('-', '').isdigit())
    
    if title_needs_quotes:
        frontmatter += f'title: "{title}"\n'
    else:
        frontmatter += f"title: {title}\n"
    
    # Only quote project name if needed
    if '"' in project_name or ':' in project_name or project_name.strip() != project_name:
        frontmatter += f'project: "{project_name}"\n'
    else:
        frontmatter += f"project: {project_name}\n"
    frontmatter += f"icon: {status_icon}\n"
    frontmatter += f"priority: {priority_emoji}\n"
    
    # Add parent link if this is a subtask
    if task.get('parentId'):
        parent_id = task.get('parentId')
        # We need to determine the parent filename based on the title_in_filename option
        # For now, we'll use the parent ID, but we could enhance this later
        if title_in_filename:
            # We don't have access to parent task title here, so use ID for now
            parent_filename = parent_id
        else:
            parent_filename = parent_id
        frontmatter += f"parent: [[{parent_filename}]]\n"
    
    # Add dates if they exist
    if task.get('startDate'):
        frontmatter += f"startDate: {format_date(task.get('startDate'))}\n"
    if task.get('dueDate'):
        frontmatter += f"dueDate: {format_date(task.get('dueDate'))}\n"
    if task.get('completedTime'):
        frontmatter += f"completedTime: {format_date(task.get('completedTime'))}\n"
    
    # Add other useful fields
    if task.get('repeatFlag'):
        frontmatter += f'repeatFlag: "{task.get("repeatFlag")}"\n'
    if task.get('reminders'):
        frontmatter += f"reminders: {task.get('reminders')}\n"
    
    frontmatter += "---\n\n"
    
    # Create content
    content = frontmatter
    
    # Add description if exists
    if task.get('desc'):
        content += f"## Description\n{task.get('desc')}\n\n"
    
    # Add main content if exists
    if task.get('content'):
        content += f"## Content\n{task.get('content')}\n\n"
    
    # Add subtasks if they exist (both from items and child tasks)
    items = task.get('items', [])  # Legacy subtasks
    child_tasks = task.get('child_tasks', [])  # Hierarchical child tasks
    
    if items or child_tasks:
        content += "## Subtasks\n\n"
        
        # Add legacy subtasks (items) - these don't have separate files
        for item in items:
            # Subtask: Normal: 0, Completed: 1
            item_status_icon = "✅" if item.get('status') == 1 else "⬜"
            item_title = item.get('title', 'Untitled Subtask')
            content += f"- {item_status_icon} {item_title}\n"
        
        # Add hierarchical child tasks as wiki links
        for child_task in child_tasks:
            child_title = child_task.get('title', '').strip()
            child_id = child_task.get('id', '')
            
            # Create filename for the child task
            if title_in_filename:
                sanitized_title = sanitize_folder_name(child_title)
                if len(sanitized_title) > 50:
                    sanitized_title = sanitized_title[:50]
                child_filename = f"{sanitized_title}_{child_id}"
            else:
                child_filename = child_id
            
            # Create wiki link - only add pipe and title if title exists
            if child_title:
                wiki_link = f"[[{child_filename}|{child_title}]]"
            else:
                wiki_link = f"[[{child_filename}]]"
            
            content += f"- {wiki_link}\n"
        
        content += "\n"
    
    # Write file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created: {filepath}")
        return filepath
    except Exception as e:
        print(f"Error creating file {filepath}: {e}")
        return None


def export_project_tasks(access_token, project, title_in_filename=False):
    """Export all tasks for a project"""
    project_id = project.get('id')
    project_name = project.get('name', 'Unnamed Project')
    sanitized_name = sanitize_folder_name(project_name)
    project_dir = os.path.join("./tasks", sanitized_name)
    
    print(f"\n--- Exporting tasks for project: {project_name} ---")
    
    # Get project data with tasks
    project_data = get_project_data(access_token, project_id)
    if not project_data:
        print(f"Failed to get data for project: {project_name}")
        return
    
    all_tasks = project_data.get('tasks', [])
    if not all_tasks:
        print(f"No tasks found in project: {project_name}")
        return
    
    print(f"Found {len(all_tasks)} total tasks")
    
    # Create a map of child tasks by parent ID for easy lookup
    children_by_parent = {}
    for task in all_tasks:
        parent_id = task.get('parentId')
        if parent_id:
            if parent_id not in children_by_parent:
                children_by_parent[parent_id] = []
            children_by_parent[parent_id].append(task)
    
    # Create markdown files for ALL tasks (both main and sub)
    created_files = []
    for task in all_tasks:
        # Add child tasks to the task object for processing
        task_id = task.get('id')
        task['child_tasks'] = children_by_parent.get(task_id, [])
        
        filepath = create_task_markdown(task, project_name, project_dir, title_in_filename)
        if filepath:
            created_files.append(filepath)
    
    print(f"Created {len(created_files)} task files for project: {project_name}")


def main():
    """Main function to export TickTick tasks"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Export TickTick tasks to markdown files')
    parser.add_argument('--title-in-filename', action='store_true', 
                       help='Include task title in filename (default: only task ID)')
    args = parser.parse_args()
    
    print("TickTick Task Exporter")
    print("=" * 30)
    
    # Get access token
    access_token = get_access_token()
    print(f"Using access token: {access_token[:10]}...")
    
    # Get projects
    projects = get_projects(access_token)
    
    if projects:
        display_projects(projects)
        create_project_directories(projects)
        
        # Export tasks for each project
        print(f"\n{'='*50}")
        print("EXPORTING TASKS")
        print(f"{'='*50}")
        
        for project in projects:
            export_project_tasks(access_token, project, args.title_in_filename)


def sanitize_folder_name(name):
    """Sanitize project name to be safe for folder names"""
    if not name:
        return "unnamed_project"
    
    # Replace invalid characters with underscores
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', name)
    # Remove leading/trailing whitespace and dots
    sanitized = sanitized.strip(' .')
    # Replace multiple consecutive underscores with single underscore
    sanitized = re.sub(r'_+', '_', sanitized)
    
    return sanitized or "unnamed_project"


def create_project_directories(projects):
    """Create directory structure for each project"""
    base_dir = "./tasks"
    
    # Create base tasks directory if it doesn't exist
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        print(f"Created base directory: {base_dir}")
    
    created_dirs = []
    
    for project in projects:
        project_name = project.get('name', 'Unnamed Project')
        sanitized_name = sanitize_folder_name(project_name)
        project_dir = os.path.join(base_dir, sanitized_name)
        
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
            created_dirs.append(project_dir)
            print(f"Created directory: {project_dir}")
        else:
            print(f"Directory already exists: {project_dir}")
    
    if created_dirs:
        print(f"\nSuccessfully created {len(created_dirs)} project directories")
    else:
        print("\nAll project directories already exist")
    
    return created_dirs


def display_projects(projects):
    """Display projects in a simple list format"""
    if not projects:
        print("No projects found")
        return
    
    print(f"\nFound {len(projects)} projects:")
    print("-" * 60)
    
    for i, project in enumerate(projects, 1):
        print(f"{i}. {project.get('name', 'Unnamed Project')}")
        print(f"   ID: {project.get('id', 'N/A')}")
        print(f"   Color: {project.get('color', 'N/A')}")
        print(f"   View Mode: {project.get('viewMode', 'N/A')}")
        print(f"   Permission: {project.get('permission', 'N/A')}")
        print(f"   Kind: {project.get('kind', 'N/A')}")
        print(f"   Closed: {project.get('closed', False)}")
        if project.get('groupId'):
            print(f"   Group ID: {project.get('groupId')}")
        print()


def main():
    """Main function to export TickTick tasks"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Export TickTick tasks to markdown files')
    parser.add_argument('--title-in-filename', action='store_true', 
                       help='Include task title in filename (default: only task ID)')
    args = parser.parse_args()
    
    print("TickTick Task Exporter")
    print("=" * 30)
    
    # Get access token
    access_token = get_access_token()
    print(f"Using access token: {access_token[:10]}...")
    
    # Get projects
    projects = get_projects(access_token)
    
    if projects:
        display_projects(projects)
        create_project_directories(projects)
        
        # Export tasks for each project
        print(f"\n{'='*50}")
        print("EXPORTING TASKS")
        print(f"{'='*50}")
        
        for project in projects:
            export_project_tasks(access_token, project, args.title_in_filename)
    else:
        print("Failed to retrieve projects")
        sys.exit(1)


if __name__ == "__main__":
    main()