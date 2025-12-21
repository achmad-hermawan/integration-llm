import google.generativeai as genai

genai.configure(api_key="AIzaSyCJ86gE4-7S0FasMDm2MQLMuuRizxiy6NA")

models = genai.list_models()

for m in models:
    print(m.name, "=>", m.supported_generation_methods)
