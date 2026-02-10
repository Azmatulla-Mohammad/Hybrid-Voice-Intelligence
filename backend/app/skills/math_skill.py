import re
import math

class MathSkill:
    @staticmethod
    def is_match(text: str) -> bool:
        # Check for math operators and numbers, but avoid common text confusion
        # Regex looks for: (digit) (op) (digit)
        # Or requests like "calculate", "what is" followed by math
        if re.search(r'\d+\s*[\+\-\*\/]\s*\d+', text):
            return True
        if "calculate" in text or "solve" in text:
            # Check if there are numbers
            return bool(re.search(r'\d+', text))
        return False

    @staticmethod
    def execute(text: str) -> str:
        try:
            # Clean text to extract just the math expression
            # Remove words, keep numbers and operators
            clean_expr = re.sub(r'[^\d\.\+\-\*\/\(\)\s\^]', '', text)
            clean_expr = clean_expr.replace('^', '**')
            
            if not clean_expr.strip():
                return "I couldn't find a valid math expression."

            # Safe evaluation
            # Only allow specific functions
            allowed_names = {"sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan, "log": math.log, "pi": math.pi, "e": math.e}
            code = compile(clean_expr, "<string>", "eval")
            
            # Check for unsafe codes
            for name in code.co_names:
                if name not in allowed_names:
                    return "Sorry, that math function is not supported for security reasons."

            result = eval(code, {"__builtins__": {}}, allowed_names)
            return f"The answer is {result}"
        except Exception as e:
            return f"I couldn't calculate that. Error: {str(e)}"
