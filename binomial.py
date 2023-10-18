import math

class Node:
	def __init__(self, value):
		self.value = value
		self.parent = None
		self.children = []
		self.degree = 0
		self.marked = False

class BinomialHeap:
	def __init__(self):
		self.trees = []
		self.min_node = None
		self.count = 0

	def is_empty(self):
		return self.min_node is None

	def insert(self, value):
		node = Node(value)
		self.merge(BinomialHeap(node))

	def get_min(self):
		return self.min_node.value

	def extract_min(self):
		min_node = self.min_node
		self.trees.remove(min_node)
		self.merge(BinomialHeap(*min_node.children))
		self._find_min()
		self.count -= 1
		return min_node.value

	def merge(self, other_heap):
		self.trees.extend(other_heap.trees)
		self.count += other_heap.count
		self._find_min()

	def _find_min(self):
		self.min_node = None
		for tree in self.trees:
			if self.min_node is None or tree.value < self.min_node.value:
				self.min_node = tree

	def decrease_key(self, node, new_value):
		if new_value > node.value:
			raise ValueError("New value is greater than current value")
		node.value = new_value
		self._bubble_up(node)

	def delete(self, node):
		self.decrease_key(node, float('-inf'))
		self.extract_min()

	def _bubble_up(self, node):
		parent = node.parent
		while parent is not None and node.value < parent.value:
			node.value, parent.value = parent.value, node.value
			node, parent = parent, node

	def _link(self, tree1, tree2):
		if tree1.value > tree2.value:
			tree1, tree2 = tree2, tree1
		tree2.parent = tree1
		tree1.children.append(tree2)
		tree1.degree += 1

	def _consolidate(self):
		max_degree = int(math.log(self.count, 2))
		degree_to_tree = [None] * (max_degree + 1)

		while self.trees:
			current = self.trees.pop(0)
			degree = current.degree
			while degree_to_tree[degree] is not None:
				other = degree_to_tree[degree]
				degree_to_tree[degree] = None
				if current.value < other.value:
					self._link(current, other)
				else:
					self._link(other, current)
				degree += 1
			degree_to_tree[degree] = current

		self.min_node = None
		self.trees = [tree for tree in degree_to_tree if tree is not None]

	def __len__(self):
		return self.count
