import tkinter as tk
from tkinter import ttk
import sv_ttk
import darkdetect


class TreeNode:
    """二叉树节点类"""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinaryTree:
    """二叉树实现"""

    def __init__(self):
        self.root = None

    def insert(self, value):
        """插入节点"""
        if not self.root:
            self.root = TreeNode(value)
        else:
            self._insert(self.root, value)

    def _insert(self, node, value):
        if value < node.value:
            if node.left:
                self._insert(node.left, value)
            else:
                node.left = TreeNode(value)
        elif value > node.value:
            if node.right:
                self._insert(node.right, value)
            else:
                node.right = TreeNode(value)

    def delete(self, value):
        """删除节点"""
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        if not node:
            return node
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete(node.right, temp.value)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def inorder_traversal(self):
        """中序遍历"""
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node, result):
        if not node:
            return
        self._inorder_traversal(node.left, result)
        result.append(node.value)
        self._inorder_traversal(node.right, result)

    def preorder_traversal(self):
        """前序遍历"""
        result = []
        self._preorder_traversal(self.root, result)
        return result

    def _preorder_traversal(self, node, result):
        if not node:
            return
        result.append(node.value)
        self._preorder_traversal(node.left, result)
        self._preorder_traversal(node.right, result)

    def postorder_traversal(self):
        """后序遍历"""
        result = []
        self._postorder_traversal(self.root, result)
        return result

    def _postorder_traversal(self, node, result):
        if not node:
            return
        self._postorder_traversal(node.left, result)
        self._postorder_traversal(node.right, result)
        result.append(node.value)


class BinaryTreeApp:
    """二叉树可视化应用"""

    def __init__(self, root):
        self.root = root
        self.tree = BinaryTree()
        self.node_positions = {}  # 存储节点位置信息
        self.build_ui()

        # 绑定画布点击事件
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def build_ui(self):
        self.root.title("二叉树可视化工具")
        self.root.geometry("800x600")

        # 顶部控制面板
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.entry_value = ttk.Entry(control_frame)
        self.entry_value.grid(row=0, column=0, padx=5)

        ttk.Button(control_frame, text="插入", command=self.insert_value).grid(
            row=0, column=1, padx=5
        )
        ttk.Button(control_frame, text="删除", command=self.delete_value).grid(
            row=0, column=2, padx=5
        )

        # 遍历结果显示区域
        self.info_label = ttk.Label(
            control_frame,
            text="说明：输入数值添加节点，点击选择一个节点",
            anchor="w",
        )
        self.info_label.grid(row=1, column=0, columnspan=3, sticky="w", padx=5)

        self.preorder_label = ttk.Label(
            control_frame, text="前序遍历结果：", anchor="w"
        )
        self.preorder_label.grid(row=2, column=0, columnspan=3, sticky="w", padx=5)

        self.inorder_label = ttk.Label(control_frame, text="中序遍历结果：", anchor="w")
        self.inorder_label.grid(row=3, column=0, columnspan=3, sticky="w", padx=5)

        self.postorder_label = ttk.Label(
            control_frame, text="后序遍历结果：", anchor="w"
        )
        self.postorder_label.grid(row=4, column=0, columnspan=3, sticky="w", padx=5)

        # 二叉树可视化面板
        self.canvas = tk.Canvas(self.root, bg="white", height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 设置主题
        self.set_theme()

    def set_theme(self):
        if darkdetect.isDark():
            sv_ttk.use_dark_theme()
            self.canvas.config(bg="#2e2e2e")
        else:
            sv_ttk.use_light_theme()
            self.canvas.config(bg="white")

    def insert_value(self):
        try:
            value = int(self.entry_value.get())
            self.tree.insert(value)
            self.update_ui()
        except ValueError:
            self.output_label.config(text="请输入有效的整数值！")

    def delete_value(self):
        try:
            value = int(self.entry_value.get())
            self.tree.delete(value)
            self.update_ui()
        except ValueError:
            self.output_label.config(text="请输入有效的整数值！")

    def update_ui(self):
        # 更新所有遍历结果
        self.preorder_label.config(
            text=f"前序遍历结果：{self.tree.preorder_traversal()}"
        )
        self.inorder_label.config(text=f"中序遍历结果：{self.tree.inorder_traversal()}")
        self.postorder_label.config(
            text=f"后序遍历结果：{self.tree.postorder_traversal()}"
        )

        self.canvas.delete("all")
        self.node_positions.clear()
        if self.tree.root:
            self.draw_tree(self.tree.root, 400, 20, 200)

    def draw_tree(self, node, x, y, offset):
        if node.left:
            self.canvas.create_line(x, y, x - offset, y + 80, fill="blue")
            self.draw_tree(node.left, x - offset, y + 80, offset // 2)
        if node.right:
            self.canvas.create_line(x, y, x + offset, y + 80, fill="blue")
            self.draw_tree(node.right, x + offset, y + 80, offset // 2)

        # 存储节点位置信息
        self.node_positions[(x, y)] = node.value

        # 绘制节点
        self.canvas.create_oval(
            x - 15, y - 15, x + 15, y + 15, fill="lightgreen", outline="black"
        )
        self.canvas.create_text(x, y, text=str(node.value), font=("Arial", 12))

    def on_canvas_click(self, event):
        """处理画布点击事件"""
        x, y = event.x, event.y
        # 检查是否点击了某个节点
        for node_pos, value in self.node_positions.items():
            node_x, node_y = node_pos
            # 检查点击位置是否在节点圆形范围内
            if (x - node_x) ** 2 + (y - node_y) ** 2 <= 15**2:
                # 更新输入框的值
                self.entry_value.delete(0, tk.END)
                self.entry_value.insert(0, str(value))
                return


if __name__ == "__main__":
    root = tk.Tk()
    app = BinaryTreeApp(root)
    root.mainloop()
