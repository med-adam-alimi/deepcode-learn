import json
from typing import List, Dict
import uuid

def generate_problems() -> List[Dict]:
    problems = []
    existing_titles = set()  # Track titles to ensure uniqueness
    existing_descriptions = set()  # Track descriptions to ensure uniqueness
    
    # Easy Problems (50 unique)
    easy_templates = generate_easy_templates()
    easy_count = 0
    template_index = 0
    while easy_count < 50:
        template = easy_templates[template_index % len(easy_templates)]
        title = f"Easy Problem {easy_count + 1}: {template['short_description']}"
        if title not in existing_titles and template['description'] not in existing_descriptions:
            problems.append(create_problem(
                id=f"easy-{easy_count + 1}",
                title=title,
                template=template,
                difficulty="Easy"
            ))
            existing_titles.add(title)
            existing_descriptions.add(template['description'])
            easy_count += 1
        template_index += 1
        if template_index >= len(easy_templates) * 2:  # Prevent infinite loop
            break
    
    # Medium Problems (50 unique)
    medium_templates = generate_medium_templates()
    medium_count = 0
    template_index = 0
    while medium_count < 50:
        template = medium_templates[template_index % len(medium_templates)]
        title = f"Medium Problem {medium_count + 1}: {template['short_description']}"
        if title not in existing_titles and template['description'] not in existing_descriptions:
            problems.append(create_problem(
                id=f"medium-{medium_count + 1}",
                title=title,
                template=template,
                difficulty="Medium"
            ))
            existing_titles.add(title)
            existing_descriptions.add(template['description'])
            medium_count += 1
        template_index += 1
        if template_index >= len(medium_templates) * 2:
            break
    
    # Hard Problems (50 unique)
    hard_templates = generate_hard_templates()
    hard_count = 0
    template_index = 0
    while hard_count < 50:
        template = hard_templates[template_index % len(hard_templates)]
        title = f"Hard Problem {hard_count + 1}: {template['short_description']}"
        if title not in existing_titles and template['description'] not in existing_descriptions:
            problems.append(create_problem(
                id=f"hard-{hard_count + 1}",
                title=title,
                template=template,
                difficulty="Hard"
            ))
            existing_titles.add(title)
            existing_descriptions.add(template['description'])
            hard_count += 1
        template_index += 1
        if template_index >= len(hard_templates) * 2:
            break
    
    print(f"Generated {easy_count} easy, {medium_count} medium, {hard_count} hard problems")
    return problems

def create_problem(id: str, title: str, template: Dict, difficulty: str) -> Dict:
    return {
        "id": id,
        "title": title,
        "short_description": template["short_description"],
        "description": template["description"],
        "difficulty": difficulty,
        "tests": template["tests"],
        "created_at": "2025-07-15"
    }

def generate_easy_templates() -> List[Dict]:
    return [
        {
            "short_description": "Reverse a String",
            "description": "Write a Python function called `reverse_string` that takes a string and returns it reversed without using built-in reverse functions.",
            "tests": [
                {"input": '"hello"', "output": '"olleh"'},
                {"input": '"world"', "output": '"dlrow"'},
                {"input": '"12345"', "output": '"54321"'},
                {"input": '""', "output": '""'},
                {"input": '"a"', "output": '"a"'}
            ]
        },
        {
            "short_description": "Check if Number is Even",
            "description": "Write a Python function called `is_even` that takes an integer and returns True if even, False otherwise.",
            "tests": [
                {"input": "4", "output": "True"},
                {"input": "7", "output": "False"},
                {"input": "0", "output": "True"},
                {"input": "-2", "output": "True"},
                {"input": "-3", "output": "False"}
            ]
        },
        {
            "short_description": "Sum of Array",
            "description": "Write a Python function called `array_sum` that returns the sum of all numbers in an array.",
            "tests": [
                {"input": "[1,2,3]", "output": "6"},
                {"input": "[]", "output": "0"},
                {"input": "[-1,1]", "output": "0"},
                {"input": "[10]", "output": "10"},
                {"input": "[1,-2,3]", "output": "2"}
            ]
        },
        {
            "short_description": "Find Maximum",
            "description": "Write a Python function called `find_max` that returns the maximum number in an array.",
            "tests": [
                {"input": "[1,2,3]", "output": "3"},
                {"input": "[-1,-2,-3]", "output": "-1"},
                {"input": "[5]", "output": "5"},
                {"input": "[0,0,0]", "output": "0"},
                {"input": "[10,-5,7]", "output": "10"}
            ]
        },
        {
            "short_description": "Count Characters",
            "description": "Write a Python function called `count_chars` that counts occurrences of a character in a string.",
            "tests": [
                {"input": '"hello", "l"', "output": "2"},
                {"input": '"world", "w"', "output": "1"},
                {"input": '"aaa", "a"', "output": "3"},
                {"input": '"test", "z"', "output": "0"},
                {"input": '"", "x"', "output": "0"}
            ]
        },
        {
            "short_description": "Palindrome Check",
            "description": "Write a Python function called `is_palindrome` that checks if a string is a palindrome (reads the same forward and backward).",
            "tests": [
                {"input": '"racecar"', "output": "True"},
                {"input": '"hello"', "output": "False"},
                {"input": '"a"', "output": "True"},
                {"input": '""', "output": "True"},
                {"input": '"abcba"', "output": "True"}
            ]
        },
        {
            "short_description": "Factorial",
            "description": "Write a Python function called `factorial` that computes the factorial of a non-negative integer.",
            "tests": [
                {"input": "5", "output": "120"},
                {"input": "0", "output": "1"},
                {"input": "1", "output": "1"},
                {"input": "3", "output": "6"},
                {"input": "7", "output": "5040"}
            ]
        }
    ]

def generate_medium_templates() -> List[Dict]:
    return [
        {
            "short_description": "Validate Binary Search Tree",
            "description": "Write a Python function `is_valid_bst` that checks if a binary tree is a valid BST (left < parent < right for all nodes).",
            "tests": [
                {"input": "{'val':2,'left':{'val':1},'right':{'val':3}}", "output": "True"},
                {"input": "{'val':5,'left':{'val':1},'right':{'val':4,'left':{'val':3},'right':{'val':6}}}", "output": "False"},
                {"input": "{'val':10,'left':{'val':5},'right':{'val':15}}", "output": "True"},
                {"input": "{'val':10,'left':{'val':5},'right':{'val':10}}", "output": "False"},
                {"input": "{'val':1}", "output": "True"}
            ]
        },
        {
            "short_description": "Longest Substring",
            "description": "Write a Python function `length_of_longest_substring` that finds the length of the longest substring without repeating characters.",
            "tests": [
                {"input": '"abcabcbb"', "output": "3"},
                {"input": '"bbbbb"', "output": "1"},
                {"input": '"pwwkew"', "output": "3"},
                {"input": '""', "output": "0"},
                {"input": '"dvdf"', "output": "3"}
            ]
        },
        {
            "short_description": "Two Sum",
            "description": "Write a Python function `two_sum` that finds indices of two numbers that add up to a target.",
            "tests": [
                {"input": "[2,7,11,15], 9", "output": "[0,1]"},
                {"input": "[3,2,4], 6", "output": "[1,2]"},
                {"input": "[3,3], 6", "output": "[0,1]"},
                {"input": "[1,2,3], 10", "output": "[]"},
                {"input": "[0,0], 0", "output": "[0,1]"}
            ]
        },
        {
            "short_description": "Group Anagrams",
            "description": "Write a Python function `group_anagrams` that groups an array of strings by their anagrams.",
            "tests": [
                {"input": '["eat","tea","tan","ate","nat","bat"]', "output": "[['eat','tea','ate'],['tan','nat'],['bat']]"},
                {"input": '[""]', "output": "[['']]"},
                {"input": '["a"]', "output": "[['a']]"},
                {"input": '["abc","cba","bac"]', "output": "[['abc','cba','bac']]"},
                {"input": '["rat","tar","art","tra"]', "output": "[['rat','tar','art','tra']]"}
            ]
        },
        {
            "short_description": "Spiral Matrix",
            "description": "Write a Python function `spiral_order` that returns all elements of a matrix in spiral order.",
            "tests": [
                {"input": "[[1,2,3],[4,5,6],[7,8,9]]", "output": "[1,2,3,6,9,8,7,4,5]"},
                {"input": "[[1,2],[3,4]]", "output": "[1,2,4,3]"},
                {"input": "[[1]]", "output": "[1]"},
                {"input": "[[1,2,3,4]]", "output": "[1,2,3,4]"},
                {"input": "[[1],[2],[3]]", "output": "[1,2,3]"}
            ]
        }
    ]

def generate_hard_templates() -> List[Dict]:
    return [
        {
            "short_description": "Regular Expression Matching",
            "description": "Implement regular expression matching with support for '.' and '*' where '.' matches any single character and '*' matches zero or more of the preceding element.",
            "tests": [
                {"input": '"aa", "a"', "output": "False"},
                {"input": '"aa", "a*"', "output": "True"},
                {"input": '"ab", ".*"', "output": "True"},
                {"input": '"aab", "c*a*b"', "output": "True"},
                {"input": '"mississippi", "mis*is*p*."', "output": "False"}
            ]
        },
        {
            "short_description": "Median of Two Sorted Arrays",
            "description": "Write a Python function `find_median_sorted_arrays` that finds the median of two sorted arrays.",
            "tests": [
                {"input": "[1,3], [2]", "output": "2.0"},
                {"input": "[1,2], [3,4]", "output": "2.5"},
                {"input": "[], [1]", "output": "1.0"},
                {"input": "[1], []", "output": "1.0"},
                {"input": "[1,2,3], [4,5,6]", "output": "3.5"}
            ]
        },
        {
            "short_description": "N-Queens",
            "description": "Write a Python function `solve_n_queens` that returns all valid placements of queens on an NxN chessboard.",
            "tests": [
                {"input": "4", "output": "[['.Q..','...Q','Q...','..Q.'],['..Q.','Q...','...Q','.Q..']]"},
                {"input": "1", "output": "[['Q']]"},
                {"input": "2", "output": "[]"},
                {"input": "3", "output": "[]"},
                {"input": "5", "output": "10"}  # Number of solutions
            ]
        },
        {
            "short_description": "Trapping Rain Water",
            "description": "Write a Python function `trap` that calculates how much water can be trapped between bars of given heights.",
            "tests": [
                {"input": "[0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6"},
                {"input": "[4,2,0,3,2,5]", "output": "9"},
                {"input": "[]", "output": "0"},
                {"input": "[1]", "output": "0"},
                {"input": "[2,0,2]", "output": "2"}
            ]
        }
    ]

def save_to_json(data: List[Dict], filename: str = "problems_dataset.json"):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Saved {len(data)} problems to {filename}")
    except Exception as e:
        print(f"❌ Error saving to JSON: {str(e)}")

if __name__ == "__main__":
    try:
        problems = generate_problems()
        save_to_json(problems)
    except Exception as e:
        print(f"❌ Error generating problems: {str(e)}")