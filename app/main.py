import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!

def matcher(input_line, pattern):
    if not input_line and not pattern:
        return True
    if not input_line:
        return False
    if not pattern:
        return True

    if pattern.startswith("\\d") and input_line[0].isdigit():
        return matcher(input_line[1:], pattern[2:])
    elif pattern.startswith("\\w") and input_line[0].isalnum():
        return matcher(input_line[1:], pattern[2:])
    elif len(pattern) > 1 and pattern[1] == "+":
        char = pattern[0]
        ptr = 0
        # Match at least one occurrence of char
        while ptr < len(input_line) and input_line[ptr] == char:
            ptr += 1
        if ptr == 0:
            return False
        # Try matching the rest of the pattern after the "+"
        return matcher(input_line[ptr:], pattern[2:])
    elif len(pattern) > 1 and pattern[1] == "?":
        char = pattern[0]
        # Match zero occurrence
        if matcher(input_line, pattern[2:]):
            return True
        # Match one occurrence if available
        if len(input_line) > 0 and input_line[0] == char:
            return matcher(input_line[1:], pattern[2:])
        return False
    elif pattern[0] == ".":
        return matcher(input_line[1:], pattern[1:])
    elif input_line[0] == pattern[0]:
        return matcher(input_line[1:], pattern[1:])
    
    return matcher(input_line[1:], pattern)

def match_pattern(input_line, pattern):
    if len(pattern) == 1:
        return pattern in input_line
    elif pattern[0] == "^":
        return input_line.startswith(pattern[1:])
    elif pattern.endswith("$"):
        return input_line.endswith(pattern[:-1])    
    elif pattern == "\\d":
        return any(c.isdigit() for c in input_line)
    elif pattern == "\w":
        return any(c.isalnum() for c in input_line)
    elif pattern[0] == "[" and pattern[-1] == "]":
        if pattern[1] == "^":
            return not any(char in pattern[1:-1] for char in input_line)
        return any(c in pattern[1:-1] for c in input_line)
    else:
        # raise RuntimeError(f"Unhandled pattern: {pattern}")
        return matcher(input_line, pattern)


def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
