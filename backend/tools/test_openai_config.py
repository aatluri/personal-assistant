from app.config import settings


print("\n--- TEST: OPENAI CONFIGURATION ---")

assert settings.OPENAI_API_KEY
assert len(settings.OPENAI_API_KEY) > 10

print("PASS: OPENAI_API_KEY loaded successfully")

print("\n====================================")
print("OPENAI CONFIGURATION TEST PASSED")
print("====================================")