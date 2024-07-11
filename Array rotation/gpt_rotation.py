def rotate_list(nums, k):
    # Ensure k is within the bounds of the list's length
    k = k % len(nums) if nums else 0

    # Slice the list and concatenate
    rotated_list = nums[-k:] + nums[:-k]
    return rotated_list


# Example usage
numbers = [1, 2, 3, 4, 5, 66, 23, 44, 61234, 66]
rotations = 55
result = rotate_list(numbers, rotations)
print(f"Original list: {numbers}")
print(f"Rotated list: {result}")
