import timeit
import struct

# data = b"\x3f\x80\x00\x00" * 1000000  # 生成1MB测试数据


# def test_list_comprehension():
#     return [struct.unpack(">f", data[i : i + 4])[0] for i in range(0, len(data), 4)]


# def test_single_unpack():
#     return list(struct.unpack(f">{len(data)//4}f", data))


# print(timeit.timeit(test_list_comprehension, number=100))
# print(timeit.timeit(test_single_unpack, number=100))

point_list = [0.1, 0.2, 0.3, 0.4, 0.5]


def test_unpack():
    """测试数据解包性能"""
    data = struct.pack(f">{len(point_list)}f", *point_list)
    unpacked = struct.unpack(f">{len(point_list)}f", data)
    return unpacked


data = struct.pack(f">{len(point_list)}f", *point_list)
print(data.hex(" "))
