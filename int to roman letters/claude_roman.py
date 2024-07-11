def int_to_roman(num):
    # Define the Roman numeral symbols and their values
    val_symbols = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]

    roman = ""

    # Iterate through the value-symbol pairs
    for value, symbol in val_symbols:
        # While the number is greater than or equal to the current value
        while num >= value:
            # Add the corresponding symbol to the result
            roman += symbol
            # Subtract the value from the number
            num -= value

    return roman


# Example usage
numbers = [4, 9, 14, 44, 99, 400, 944, 1994, 2024]
for num in numbers:
    print(f"{num} in Roman numerals is: {int_to_roman(num)}")