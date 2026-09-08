

import numpy as np

arr = np.array([1, 2, 3, 4, 5])

print(arr)
print(type(arr))

#0차원
arr0 = np.array(200)
#1차원
arr1 = np.array([1, 2, 3, 4, 5])
#2차원(행, 열)
arr2 = np.array([[1, 2, 3], [4, 5, 6]])
#3차원(면, 행, 열)
arr3 = np.array([[[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6]]])

print(arr3)

#배열의 차원 확인
print(arr0.ndim)
print(arr1.ndim)
print(arr2.ndim)
print(arr3.ndim)

import numpy as np
arr = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
print('Last element from 2nd dim:', arr[1, -1])

import numpy as np
arr = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
print(arr[1, 1, 0])

