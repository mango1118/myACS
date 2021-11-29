

# ------------ 栈 ------------
class Stack(object):
    all_path = []

    def __init__(self, total, path_x_y):
        self.items = []
        self.total = total
        self.li = path_x_y
        self.total = total

    def push(self, item: int):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def isEmpty(self):
        if not self.items:
            return True
        return False

    def contains(self, i):
        if i in self.items:
            return True
        return False

    def printStack(self):
        temp = self.items.copy()
        self.all_path.append(temp)
        # print(self.items)

    def dfsStack(self, under, goal):
        all_path = []
        if self.isEmpty():
            return
        # 起点
        k = self.peek()
        if k == goal:
            return
        i = 0
        while i < self.total:
            # 起点到中间点有路径
            if self.li[k][i] == 1:
                # 排除环路
                if self.contains(i):
                    i += 1
                    continue
                if i == goal:
                    # print("路径")
                    self.push(goal)
                    self.printStack()
                    # all_path.append(self)
                    self.pop()
                    i += 1
                    continue

                self.push(i)
                self.dfsStack(k, goal)
            i += 1
        del self.items[-1]

