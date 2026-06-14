import re
import math

class NaiveBayesClassifier:
    """A lightweight Naive Bayes Classifier implemented from scratch for mistake classification."""
    
    def __init__(self):
        self.class_priors = {}
        self.feature_likelihoods = {}
        self.classes = []
        self.features = [
            "has_syntax_error",
            "has_index_error",
            "has_recursion_error",
            "has_logic_error",
            "potential_missing_base_case",
            "shadowing_builtin",
            "invalid_len_method",
            "invalid_keyword_elsif",
            "incorrect_none_comparison"
        ]
        self._train()

    def _train(self):
        # Representative training samples representing typical coding features and classifications
        training_data = [
            # Syntax Errors
            ({"has_syntax_error": True, "has_logic_error": True}, "syntax_error"),
            ({"has_syntax_error": True, "has_logic_error": True, "shadowing_builtin": True}, "syntax_error"),
            
            # Index Errors
            ({"has_index_error": True, "has_logic_error": True}, "index_error"),
            ({"has_index_error": True, "has_logic_error": True, "shadowing_builtin": True}, "index_error"),
            
            # Recursion Errors
            ({"has_recursion_error": True, "has_logic_error": True}, "recursion_error"),
            ({"has_recursion_error": True, "has_logic_error": True, "potential_missing_base_case": True}, "recursion_error"),
            
            # Missing base case
            ({"has_logic_error": True, "potential_missing_base_case": True}, "potential_missing_base_case"),
            
            # Shadowing Builtin
            ({"shadowing_builtin": True}, "shadowing_builtin"),
            ({"shadowing_builtin": True, "has_logic_error": True}, "shadowing_builtin"),
            
            # Invalid length method
            ({"invalid_len_method": True}, "invalid_len_method"),
            ({"invalid_len_method": True, "has_logic_error": True}, "invalid_len_method"),
            
            # Invalid keyword elsif
            ({"invalid_keyword_elsif": True, "has_syntax_error": True}, "invalid_keyword_elsif"),
            ({"invalid_keyword_elsif": True}, "invalid_keyword_elsif"),
            
            # Incorrect None comparison
            ({"incorrect_none_comparison": True}, "incorrect_none_comparison"),
            ({"incorrect_none_comparison": True, "has_logic_error": True}, "incorrect_none_comparison"),
            
            # Logic Errors (without other syntactic/structural patterns)
            ({"has_logic_error": True}, "logic_error"),
            
            # No mistake
            ({}, "no_mistake"),
        ]

        total_samples = len(training_data)
        class_counts = {}
        for _, label in training_data:
            class_counts[label] = class_counts.get(label, 0) + 1
            
        num_classes = len(class_counts)
        self.classes = list(class_counts.keys())
        
        # Prior P(C) with Laplace smoothing
        for label, count in class_counts.items():
            self.class_priors[label] = (count + 1) / (total_samples + num_classes)
            
        # Initialize likelihood counts
        self.feature_likelihoods = {c: {f: 0 for f in self.features} for c in self.classes}
        
        for feature_dict, label in training_data:
            for f in self.features:
                if feature_dict.get(f, False):
                    self.feature_likelihoods[label][f] += 1
                    
        # Likelihood P(F_i = 1 | C) with Laplace smoothing
        for label in self.classes:
            class_total = class_counts[label]
            for f in self.features:
                count_f_1 = self.feature_likelihoods[label][f]
                self.feature_likelihoods[label][f] = (count_f_1 + 1) / (class_total + 2)

    def predict(self, feature_dict: dict) -> str:
        if not self.classes:
            return "unknown"
            
        best_class = None
        best_prob = -float('inf')
        
        for label in self.classes:
            # log P(C)
            prob = math.log(self.class_priors.get(label, 1e-6))
            
            # log P(F_i | C)
            for f in self.features:
                val = feature_dict.get(f, False)
                p_f_1 = self.feature_likelihoods[label].get(f, 0.5)
                if val:
                    prob += math.log(p_f_1)
                else:
                    prob += math.log(1.0 - p_f_1)
                    
            if prob > best_prob:
                best_prob = prob
                best_class = label
                
        return best_class

# Instantiate classifier
classifier = NaiveBayesClassifier()

class MistakeDetector:
    """Detect common mistakes in Python code."""

    @staticmethod
    def analyze_code(code: str, execution_result: dict) -> dict:
        """
        Analyze code and execution to detect mistake types.
        execution_result contains: passed, results (each with 'status', 'error', etc.)
        Returns: {"mistakes": list of mistake types, "primary_mistake": str}
        """
        mistakes = set()

        # 1. Error Analysis: check for exceptions in any of the test case results
        results = execution_result.get("results", [])
        errors = [r.get("error") for r in results if r.get("error")]
        error_str = " ".join(errors) if errors else ""

        has_syntax_error = "SyntaxError" in error_str
        has_index_error = "IndexError" in error_str
        has_recursion_error = "RecursionError" in error_str

        if has_syntax_error:
            mistakes.add("syntax_error")
        if has_index_error:
            mistakes.add("index_error")
        if has_recursion_error:
            mistakes.add("recursion_error")

        # Logic error: code ran but failed some test cases, without any runtime/syntax error
        has_logic_error = not execution_result.get("passed", True) and not errors
        if has_logic_error:
            mistakes.add("logic_error")

        # 2. Preprocess Code: Strip comments and strings to avoid false positives in regex checking
        clean_code = re.sub(r'#.*', '', code)
        clean_code = re.sub(
            r'(\"\"\"[\s\S]*?\"\"\"|\'\'\'[\s\S]*?\'\'\'|"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')',
            '',
            clean_code
        )

        # 3. Pattern Matching (Regex Checks on cleaned code)
        # Check for missing base case in recursion (with proper function body parsing)
        potential_missing_base_case = False
        lines = clean_code.split('\n')
        for i, line in enumerate(lines):
            match = re.match(r'^(\s*)def\s+(\w+)\b', line)
            if match:
                indent = len(match.group(1))
                func_name = match.group(2)
                
                body_lines = []
                for next_line in lines[i+1:]:
                    if not next_line.strip():
                        continue
                    next_indent = len(next_line) - len(next_line.lstrip())
                    if next_indent <= indent:
                        break
                    body_lines.append(next_line)
                    
                body_code = '\n'.join(body_lines)
                if re.search(r'\b' + func_name + r'\s*\(', body_code):
                    if not re.search(r'\bif\b', body_code):
                        potential_missing_base_case = True
                        break
                        
        if potential_missing_base_case:
            mistakes.add("potential_missing_base_case")

        # Check for shadowing builtin functions
        shadowing_builtin = False
        assignment_pattern = r'\b(sum|list|dict|set|str|int|len|type|max|min)\s*=[^=]'
        param_pattern = r'def\s+\w+\s*\([^)]*\b(sum|list|dict|set|str|int|len|type|max|min)\b[^)]*\)'
        if re.search(assignment_pattern, clean_code) or re.search(param_pattern, clean_code):
            shadowing_builtin = True
            mistakes.add("shadowing_builtin")

        # Check for invalid length method
        invalid_len_method = False
        if re.search(r'\.\s*(length|size)\b', clean_code):
            invalid_len_method = True
            mistakes.add("invalid_len_method")

        # Check for invalid keyword elsif
        invalid_keyword_elsif = False
        if re.search(r'\b(elsif|elseif)\b', clean_code):
            invalid_keyword_elsif = True
            mistakes.add("invalid_keyword_elsif")

        # Check for incorrect None comparison
        incorrect_none_comparison = False
        if re.search(r'(==|!=)\s*None\b|\bNone\s*(==|!=)', clean_code):
            incorrect_none_comparison = True
            mistakes.add("incorrect_none_comparison")

        # 4. Machine Learning Classification
        features = {
            "has_syntax_error": has_syntax_error,
            "has_index_error": has_index_error,
            "has_recursion_error": has_recursion_error,
            "has_logic_error": has_logic_error,
            "potential_missing_base_case": potential_missing_base_case,
            "shadowing_builtin": shadowing_builtin,
            "invalid_len_method": invalid_len_method,
            "invalid_keyword_elsif": invalid_keyword_elsif,
            "incorrect_none_comparison": incorrect_none_comparison
        }

        primary_mistake = classifier.predict(features)
        
        # Ensure the classified primary mistake is included in the mistakes list
        if primary_mistake != "no_mistake" and primary_mistake != "unknown":
            mistakes.add(primary_mistake)

        return {
            "mistakes": list(mistakes),
            "primary_mistake": primary_mistake
        }

    @staticmethod
    def get_mistake_message(mistake_type: str) -> str:
        """Return a helpful message for a mistake type."""
        messages = {
            "syntax_error": "You have a syntax error. Check for missing colons, brackets, or indentation.",
            "index_error": "Index out of range. Check if you're accessing a valid index.",
            "logic_error": "Your code runs but produces wrong output. Check your algorithm.",
            "recursion_error": "Your recursion went too deep. Make sure you have a base case.",
            "potential_missing_base_case": "Recursive functions need a base case to stop the recursion. Ensure you have an 'if' statement checking for the base condition.",
            "shadowing_builtin": "You are shadowing a Python built-in name (like list, dict, sum, len, max, min). Rename your variable or parameter to avoid unexpected behavior.",
            "invalid_len_method": "Python uses the len(object) function to get the length/size of lists or strings, not .length() or .size().",
            "invalid_keyword_elsif": "In Python, use the 'elif' keyword for else-if statements, not 'elsif' or 'elseif'.",
            "incorrect_none_comparison": "Compare with None using the 'is' or 'is not' identity operators (e.g., 'x is None') rather than equality operators ('==')."
        }
        return messages.get(mistake_type, "Unexpected error")