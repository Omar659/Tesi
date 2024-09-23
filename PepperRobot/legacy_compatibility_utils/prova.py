from module_call.stt_recognition import STTRecognizer


sttr = STTRecognizer()
sttr.listen(device_index = 1, timeout=3)