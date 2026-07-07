from ai import LocalAI

ai = LocalAI()

command = "Delete soldier Rahul"

result = ai.generate(command)

print("=" * 60)
print("USER COMMAND")
print("=" * 60)
print(command)

print()

print("=" * 60)
print("GENERATED JSON")
print("=" * 60)

print(result)