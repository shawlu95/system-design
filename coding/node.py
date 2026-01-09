class MachineNode:
    def __init__(self, parent_id, node_id, children_ids):
        self.parent_id = parent_id
        self.node_id = node_id
        self.children_ids = children_ids

        self.descendent_count = 0
        self.children_response = set()

    def sendMessageAsync(self, recipient_id, message):
        # Simulate sending a message asynchronously
        # Assume this part is provided, no need to code
        pass

    def onMessageReceived(self, sender_id, message):
        parts = message.split(":")
        instruction = parts[0]
        data = int(parts[1])

        if instruction == "COUNT":
            for child_id in self.children_ids:
                self.sendMessageAsync(child_id, message)

            # reached leaf node (base case), call parent node
            if not self.children_ids:
                self.sendMessageAsync(self.parent_id, f"SUM:1")

        elif instruction == "SUM":
            self.children_response.add(sender_id)
            self.descendent_count += data

            if self.children_response == set(self.children_ids):
                total_count = self.descendent_count + 1  # include self
                if self.parent_id is not None:
                    self.sendMessageAsync(self.parent_id, f"SUM:{total_count}")
                    self.children_response.clear()
                else:
                    # program terminated here, root node
                    print(f"Total nodes in the tree: {total_count}")