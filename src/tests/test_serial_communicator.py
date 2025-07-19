# import unittest
# from unittest.mock import MagicMock, patch
# from communicator.serial_communicator import SerialCommunicator


# class TestSerialCommunicator(unittest.TestCase):
#     def setUp(self):
#         patcher = patch("communicator.serial_communicator.serial.Serial")
#         self.addCleanup(patcher.stop)
#         self.mock_serial_class = patcher.start()
#         self.mock_serial = self.mock_serial_class.return_value
#         self.mock_serial.is_open = False
#         self.comm = SerialCommunicator(port="COM1")

#     def test_connect_success(self):
#         self.mock_serial.is_open = False
#         self.mock_serial.open = MagicMock()
#         result = self.comm.connect()
#         self.assertTrue(result)
#         self.mock_serial.open.assert_called_once()

#     def test_connect_already_open(self):
#         self.mock_serial.is_open = True
#         result = self.comm.connect()
#         self.assertTrue(result)

#     def test_connect_fail(self):
#         self.mock_serial.is_open = False
#         self.mock_serial.open.side_effect = Exception("fail")
#         result = self.comm.connect()
#         self.assertFalse(result)

#     def test_disconnect_success(self):
#         self.mock_serial.is_open = True
#         self.mock_serial.close = MagicMock()
#         result = self.comm.disconnect()
#         self.assertTrue(result)
#         self.mock_serial.close.assert_called_once()

#     def test_disconnect_not_open(self):
#         self.mock_serial.is_open = False
#         result = self.comm.disconnect()
#         self.assertTrue(result)

#     def test_send_data_success(self):
#         self.mock_serial.is_open = True
#         self.mock_serial.write.return_value = 4
#         result = self.comm.send_data(b"test")
#         self.assertTrue(result)
#         self.mock_serial.write.assert_called_once_with(b"test")

#     def test_send_data_not_bytes(self):
#         self.mock_serial.is_open = True
#         result = self.comm.send_data("not bytes")
#         self.assertFalse(result)

#     def test_send_data_empty(self):
#         self.mock_serial.is_open = True
#         result = self.comm.send_data(b"")
#         self.assertFalse(result)

#     def test_send_data_not_open(self):
#         self.mock_serial.is_open = False
#         result = self.comm.send_data(b"test")
#         self.assertFalse(result)

#     def test_send_data_write_length_mismatch(self):
#         self.mock_serial.is_open = True
#         self.mock_serial.write.return_value = 2
#         result = self.comm.send_data(b"test")
#         self.assertFalse(result)

#     def test_receive_data_success(self):
#         self.mock_serial.is_open = True
#         self.mock_serial.in_waiting = 4
#         self.mock_serial.read.return_value = b"data"
#         result = self.comm.receive_data()
#         self.assertEqual(result, b"data")

#     def test_receive_data_not_open(self):
#         self.mock_serial.is_open = False
#         result = self.comm.receive_data()
#         self.assertIsNone(result)

#     def test_receive_data_no_data(self):
#         self.mock_serial.is_open = True
#         self.mock_serial.in_waiting = 0
#         result = self.comm.receive_data()
#         self.assertIsNone(result)

#     def test_list_ports(self):
#         with patch(
#             "communicator.serial_communicator.serial.tools.list_ports.comports"
#         ) as mock_comports:
#             mock_comports.return_value = [
#                 MagicMock(device="COM1"),
#                 MagicMock(device="COM2"),
#             ]
#             ports = self.comm.list_ports()
#             self.assertEqual(ports, ["COM1", "COM2"])


# if __name__ == "__main__":
#     unittest.main()
