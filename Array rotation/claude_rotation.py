def rotate_list(numbers, rotations):
    if not numbers:
        return numbers
    rotations = rotations % len(numbers)
    return numbers[-rotations:] + numbers[:-rotations]

# Example usage
numbers = [1, 2, 3, 4, 5, 33, 35,76, 567, 763,3456]
rotations = 103
result = rotate_list(numbers, rotations)
print(f"Original list: {numbers}")
print(f"Rotated {rotations} times: {result}")