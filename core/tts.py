import pyttsx4

engine = pyttsx4.init()  # 初始化语音引擎
engine.say("accelerate")  # 输入文字
engine.save_to_file("accelerate", "./temp/test.wav")
engine.runAndWait()      # 开始朗读（阻塞直到结束）