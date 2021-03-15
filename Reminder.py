def twoSum(nums, target):
    """
    :type nums: List[int]
    :type target: int
    :rtype: List[int]
    """
    return_list = []
    print(return_list)
    check_val  = 0

    for i in range(len(nums)):
        check_val = check_val + nums[i]
        print(nums[i])
        remain = target - check_val
        
        if remain in nums:
            if nums.index(remain) != nums[i]:
                print(f'remin index  = {nums.index(remain)}')
                return_list.extend([i,nums.index(remain)])


twoSum([2,7,11,15], 9)