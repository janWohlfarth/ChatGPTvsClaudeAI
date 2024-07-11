def int_to_roman(num):
    # Define the Roman numeral symbols and their corresponding values
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
        ]
    syms = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
        ]
    roman_num = ''
    i = 0
    # Loop through each symbol, stopping if num becomes 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syms[i]
            num -= val[i]
        i += 1
    return roman_num

# Example usage
number = 2024
roman_numeral = int_to_roman(number)
print(f"The Roman numeral for {number} is {roman_numeral}")
