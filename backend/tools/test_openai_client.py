from app.ai.openai_client import get_openai_client


print("\n--- TEST: OPENAI CLIENT ---")

client = get_openai_client()

response = client.responses.create(
    model="gpt-5-mini",
    input="Reply with exactly: OpenAI connection successful",
)

print("Response:", response.output_text)

assert "OpenAI connection successful" in response.output_text

print("\n==============================")
print("OPENAI CLIENT TEST PASSED")
print("==============================")