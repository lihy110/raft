# 废弃
# import Server
# class Channel():
#     def __init__(self, name):
#         self._exit_program = True
#         self.name = name
#         self.subscribers = []

#     def recevice_channel(self, msg):
#         while self.exit_program:
#             try:
#                 data = Server.receive()
                
#             except Exception as e:
#                 print(f"Receive error: {e}")
#                 break

#     def stop_event(self):
#         self._exit_program = False