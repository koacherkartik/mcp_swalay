from app.mongo import MongoDB


class CommandExecutor:

    def __init__(self):

        self.mongo = MongoDB()

    def execute(self, command):

        operation = command["operation"]

        collection = self.mongo.get_collection(
            command["collection"]
        )

        # ---------------- FIND ----------------

        if operation == "find":

            filter_data = command.get("filter", {})

            result = list(collection.find(filter_data, {"_id": 0}))

            return result

        # ---------------- INSERT ----------------

        elif operation == "insert":

            document = command["document"]

            collection.insert_one(document)

            return {
                "status": "Inserted Successfully"
            }

        # ---------------- UPDATE ----------------

        elif operation == "update":

            filter_data = command["filter"]

            update_data = command["update"]

            result = collection.update_one(
                filter_data,
                {
                    "$set": update_data
                }
            )

            return {
                "matched": result.matched_count,
                "modified": result.modified_count
            }

        # ---------------- DELETE ----------------

        elif operation == "delete":

            filter_data = command["filter"]

            result = collection.delete_one(filter_data)

            return {
                "deleted": result.deleted_count
            }

        else:

            return {
                "error": "Unsupported Operation"
            }