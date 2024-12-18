class HandleText:
    def __init__(self):
        self.text_lines = 0
        self.text_liner = 0

    def print(self, text = ""):
        print(text)
        self.text_lines += 1

    def printr(self, text = ""):
        print(text)
        self.text_liner += 1
        
    def input(self, text):
        result = input(text)
        self.text_lines += 1
        self.delete_text()
        return result
    
    def delete_text(self):
        for _ in range(self.text_lines):
            print("\033[F\033[K", end= "")
        self.text_lines = 0

    def delete_textr(self):
        for _ in range(self.text_liner):
            print("\033[F\033[K", end= "")
        self.text_liner = 0

    def delete_all(self):
        self.delete_text()
        self.delete_textr()