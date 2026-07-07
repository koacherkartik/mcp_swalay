from ai import LocalAI
from executor import CommandExecutor

ai = LocalAI()

executor = CommandExecutor()

command = input("Enter Command : ")

parsed = ai.generate(command)

print("\nGenerated JSON\n")

print(parsed)

print("\nExecuting...\n")

result = executor.execute(parsed)

print(result)