import itertools 
import re
from unidecode import unidecode

NAME = "My Name"
DOMAIN = "example.com"
DELIMITERS = ['.', '_', '-', '']
NON_EMPTY_DELIMITERS = [d for d in DELIMITERS if d != '']
TWO_DELIMITERS = list(itertools.product(*[NON_EMPTY_DELIMITERS, NON_EMPTY_DELIMITERS]))
DELIMITERS_TO_SKIP = [''.join(d) for d in TWO_DELIMITERS ]

def generate_name_combinations(name):
    # Normalize the name to ASCII and lowercase
    name = unidecode(name).strip().lower()
    # Split the name into parts
    parts = re.sub(r'\s+', ' ', name) \
            .replace('.', ' ') \
            .replace('_', ' ') \
            .replace('-', ' ') \
            .replace(',', ' ') \
            .split()

    combinations = []
    seen = set()

    # Consider every ordering of every non-empty subset of the name parts.
    # e.g. "A B C" -> A, B, C, A B, A C, B A, ..., A B C, ..., C B A
    for size in range(1, len(parts) + 1):
        for ordered_parts in itertools.permutations(parts, size):
            # Generate variations for each part of the ordering
            part_variations = []
            for index, part in enumerate(ordered_parts):
                part_variations.append([
                    part[0],     # First letter of the part
                    part[:2],    # Two first letters of the part
                    part,        # Full part
                    '',          # None
                ])

                # Add variations with delimiters if not the last part
                if index != len(ordered_parts) - 1:
                    part_variations.append(DELIMITERS)

            # Combine all the part variations for this ordering
            for combination in itertools.product(*part_variations):
                if combination not in seen:
                    seen.add(combination)
                    combinations.append(combination)

    return combinations

def generate_email_combinations(name, domain):
    domain = domain.lower()

    # Generate all combinations of the name parts
    combinations = generate_name_combinations(name)

    # Join the parts with delimiters and return as a list of email addresses
    email_addresses = []
    for combination in combinations:
        prefix = ''.join(combination) 

        # If prefix does not start or end with a delimiter, skip it
        if prefix == "" or prefix[0] in DELIMITERS or prefix[-1] in DELIMITERS:
             continue
        
        # If prefix contains a DELIMITERS_TO_SKIP, skip it
        if any(d in prefix for d in DELIMITERS_TO_SKIP):
            continue

        email_addresses.append(prefix + '@' + domain)

    return email_addresses

def main():
    email_combinations = generate_email_combinations(NAME, DOMAIN)
    for email in email_combinations:
        print(email)
    print(f"Generated {len(email_combinations)} email combinations for name '{NAME}' and domain '{DOMAIN}':")

if __name__ == "__main__":
    main()
